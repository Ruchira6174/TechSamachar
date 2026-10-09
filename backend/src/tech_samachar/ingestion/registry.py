from tech_samachar.ingestion.connectors.rss import RSSConnector
from tech_samachar.ingestion.connectors.api_source import APISourceConnector

def get_connector(source_type: str, url: str):
    if source_type.lower() == "rss":
        return RSSConnector(url)
    elif source_type.lower() == "api":
        return APISourceConnector(url)
    else:
        raise ValueError(f"Unknown source type: {source_type}")
