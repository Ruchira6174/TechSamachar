# Tech Samachar Architecture

## Ingestion Flow
1. **Scheduler/CLI**: Triggers the ingestion pipeline periodically or manually.
2. **Pipeline**: Loads enabled sources from the database.
3. **Connectors**: Fetches articles using specific protocols (RSS/API).
4. **Normalizer**: Converts external data to an internal unified structure (validating URLs, parsing dates).
5. **Deduplicator**: Prevents duplicate insertions by checking the `canonical_url` and `content_hash`.
6. **Database**: Saves the valid and unique articles into PostgreSQL using SQLAlchemy.

## Database Schema Flow
- `Source`: Stores feed details and metadata.
- `Article`: Stores aggregated news.
- `Topic`: Stores hierarchical technology categories.
- `ArticleTopic`: Association table linking articles to topics with a classification confidence score.
- `ArticleSummary`: AI-generated summaries linked 1-to-1 with an article.
