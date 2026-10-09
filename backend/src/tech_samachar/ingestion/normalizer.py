import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from email.utils import parsedate_to_datetime

class Normalizer:
    @staticmethod
    def normalize_entry(entry: Dict[str, Any], source_id: int) -> Dict[str, Any]:
        """Normalizes a raw feed/API entry into internal schema."""
        title = entry.get("title", "").strip()
        url = entry.get("link", entry.get("url", "")).strip()
        
        # Author extraction
        author = entry.get("author", entry.get("creator", None))
        
        # Description extraction
        description = entry.get("description", entry.get("summary", None))
        
        # Date parsing
        published_time = Normalizer.parse_date(entry)
        
        # Content Hash
        content_hash = Normalizer.generate_hash(title, url)

        return {
            "title": title,
            "canonical_url": url,
            "source_id": source_id,
            "author": author,
            "published_time": published_time,
            "description": description,
            "content_hash": content_hash
        }

    @staticmethod
    def parse_date(entry: Dict[str, Any]) -> Optional[datetime]:
        date_str = entry.get("published", entry.get("updated", None))
        if not date_str:
            return None
        try:
            # feedparser usually provides parsed times
            if "published_parsed" in entry and entry["published_parsed"]:
                from time import mktime
                dt = datetime.fromtimestamp(mktime(entry["published_parsed"]))
                return dt.replace(tzinfo=timezone.utc)
            # fallback string parse
            dt = parsedate_to_datetime(date_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None

    @staticmethod
    def generate_hash(title: str, url: str) -> str:
        s = f"{title}-{url}".encode("utf-8")
        return hashlib.sha256(s).hexdigest()
