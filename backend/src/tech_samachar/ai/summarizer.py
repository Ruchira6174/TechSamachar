
import logging
import re

import httpx
import trafilatura
from sqlalchemy.orm import Session

from tech_samachar.db.models.article import Article, ArticleSummary
from tech_samachar.ai.provider_factory import (
    DummyProvider,
    get_ai_provider,
    MODEL_NAME,
)
from tech_samachar.config import settings

logger = logging.getLogger(__name__)

MIN_ARTICLE_WORDS = 80
MAX_ARTICLE_CHARS = 30_000
REQUEST_TIMEOUT = 20.0


def extract_article_text(url: str) -> str | None:
    """Fetch and extract readable article text from a canonical URL."""
    if not url:
        return None

    try:
        with httpx.Client(
            timeout=REQUEST_TIMEOUT,
            follow_redirects=True,
            headers={
                "User-Agent": "TechSamachar/1.0 (technology news reader)"
            },
        ) as client:
            response = client.get(url)
            response.raise_for_status()

            # Avoid trying to parse obviously non-HTML responses.
            content_type = response.headers.get("content-type", "").lower()
            if "html" not in content_type:
                logger.info("Skipping non-HTML article URL: %s", url)
                return None

            text = trafilatura.extract(
                response.text,
                url=str(response.url),
                include_comments=False,
                include_tables=True,
                favor_precision=True,
            )

        if not text:
            return None

        text = re.sub(r"\n{3,}", "\n\n", text).strip()

        if len(text.split()) < MIN_ARTICLE_WORDS:
            logger.info("Extracted article text is too short: %s", url)
            return None

        return text[:MAX_ARTICLE_CHARS]

    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Article extraction failed for %s: %s", url, exc)
        return None
    except Exception:
        logger.exception("Unexpected extraction error for %s", url)
        return None


class SummarizerService:
    def __init__(self, db: Session):
        self.db = db
        self.provider = get_ai_provider()

    @staticmethod
    def _is_dummy_summary(summary: ArticleSummary) -> bool:
        text = (summary.summary_text or "").lower()
        return (
            summary.provider == "none"
            or "ai summary unavailable for:" in text
            or (
                summary.model_name == "default"
                and summary.provider in (None, "", "none")
            )
        )

    def summarize_article(self, article: Article) -> bool:
        """
        Generate a summary from extracted article text when possible.

        Returns True only when a new summary was saved successfully.
        Existing real summaries are preserved.
        """
        existing = article.summary

        if existing and not self._is_dummy_summary(existing):
            return False

        if isinstance(self.provider, DummyProvider):
            logger.warning(
                "Skipping article %s because the dummy AI provider is active.",
                article.id,
            )
            return False

        article_text = extract_article_text(article.canonical_url)

        # Fall back to the RSS description only when it contains enough text.
        if not article_text:
            description = (article.description or "").strip()
            if len(description.split()) < MIN_ARTICLE_WORDS:
                logger.warning(
                    "No usable article text or description for article %s.",
                    article.id,
                )
                return False
            article_text = description[:MAX_ARTICLE_CHARS]

        try:
            summary_text = self.provider.generate_summary(
                article.title,
                article_text,
            )

            if not isinstance(summary_text, str):
                raise ValueError("AI provider returned a non-string summary.")

            summary_text = summary_text.strip()

            # Reject empty or placeholder-like output.
            if (
                not summary_text
                or len(summary_text.split()) < 10
                or "ai summary unavailable for:" in summary_text.lower()
            ):
                raise ValueError("AI provider returned an invalid summary.")

            provider_name = settings.AI_PROVIDER.strip().lower()
            model_name = getattr(self.provider, "model", MODEL_NAME)

            if existing:
                # Update the existing row; do not delete or recreate it.
                existing.summary_text = summary_text
                existing.provider = provider_name
                existing.model_name = model_name
            else:
                self.db.add(
                    ArticleSummary(
                        article_id=article.id,
                        summary_text=summary_text,
                        provider=provider_name,
                        model_name=model_name,
                    )
                )

            self.db.commit()
            return True

        except Exception as exc:
            logger.error(
                "Summarization failed for article %s: %s",
                article.id,
                exc,
            )
            self.db.rollback()
            return False