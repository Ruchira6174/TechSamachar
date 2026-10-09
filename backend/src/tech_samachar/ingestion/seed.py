from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tech_samachar.db.models.article import Topic
from tech_samachar.db.models.source import Source
import logging

logger = logging.getLogger(__name__)

INITIAL_TOPICS = [
    {"name": "Quantum Computing", "slug": "quantum-computing", "default_priority": 100},
    {"name": "Cloud Computing", "slug": "cloud-computing", "default_priority": 100},
    {"name": "Generative AI", "slug": "generative-ai", "default_priority": 100},
    {"name": "Artificial Intelligence and Machine Learning", "slug": "ai-ml", "default_priority": 50},
    {"name": "Cybersecurity", "slug": "cybersecurity", "default_priority": 50},
    {"name": "Software Engineering", "slug": "software-engineering", "default_priority": 50},
    {"name": "Developer Tools", "slug": "developer-tools", "default_priority": 50},
    {"name": "Data Science and Big Data", "slug": "data-science", "default_priority": 50},
    {"name": "Semiconductors and Computer Architecture", "slug": "semiconductors", "default_priority": 50},
    {"name": "Robotics and Automation", "slug": "robotics", "default_priority": 50},
    {"name": "Databases and Networking", "slug": "databases-networking", "default_priority": 50},
    {"name": "Open Source", "slug": "open-source", "default_priority": 50},
    {"name": "Startups and Technology Business", "slug": "startups", "default_priority": 50},
    {"name": "Emerging Research", "slug": "emerging-research", "default_priority": 50},
    {"name": "Other Technology News", "slug": "other-news", "default_priority": 10},
]

INITIAL_SOURCES = [
    {
        "name": "AWS News Blog",
        "url": "https://aws.amazon.com/blogs/aws/",
        "feed_url": "https://aws.amazon.com/blogs/aws/feed/",
        "source_type": "rss",
        "quality_score": 90,
    },
    {
        "name": "Google AI Blog",
        "url": "https://ai.googleblog.com/",
        "feed_url": "https://ai.googleblog.com/feeds/posts/default?alt=rss",
        "source_type": "rss",
        "quality_score": 90,
    },
    {
        "name": "Hacker News - Best",
        "url": "https://news.ycombinator.com/best",
        "feed_url": "https://hnrss.org/best",
        "source_type": "rss",
        "quality_score": 80,
    }
]

def seed_topics(db: Session):
    for topic_data in INITIAL_TOPICS:
        topic = db.query(Topic).filter(Topic.slug == topic_data["slug"]).first()
        if not topic:
            try:
                new_topic = Topic(**topic_data)
                db.add(new_topic)
                db.commit()
                logger.info(f"Created topic: {topic_data['name']}")
            except IntegrityError:
                db.rollback()
        else:
            logger.info(f"Topic {topic.name} already exists")

def seed_sources(db: Session):
    for source_data in INITIAL_SOURCES:
        source = db.query(Source).filter(Source.feed_url == source_data["feed_url"]).first()
        if not source:
            try:
                new_source = Source(**source_data)
                db.add(new_source)
                db.commit()
                logger.info(f"Created source: {source_data['name']}")
            except IntegrityError:
                db.rollback()
        else:
            logger.info(f"Source {source.name} already exists")

def seed_all(db: Session):
    seed_topics(db)
    seed_sources(db)
