import argparse
import sys
from tech_samachar.db.session import SessionLocal
from tech_samachar.ingestion.seed import seed_all
from tech_samachar.ingestion.pipeline import run_pipeline
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Tech Samachar Ingestion Commands")
    parser.add_argument("--seed", action="store_true", help="Seed topics and initial sources")
    parser.add_argument("--ingest", action="store_true", help="Run one ingestion cycle")
    parser.add_argument("--briefing", action="store_true", help="Generate the daily briefing")
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.seed:
            print("Seeding database...")
            seed_all(db)
            print("Seeding complete.")
            
        if args.ingest:
            print("Starting ingestion pipeline...")
            stats = run_pipeline(db)
            print("Ingestion Report:")
            print(f"Sources processed: {stats['processed_sources']}")
            print(f"Sources failed: {stats['failed_sources']}")
            print(f"Articles saved: {stats['saved_articles']}")
            print(f"Duplicates skipped: {stats['duplicate_articles']}")
            
        if args.briefing:
            print("Generating daily briefing...")
            from tech_samachar.services.briefing_service import BriefingService
            service = BriefingService(db)
            briefing = service.generate_briefing()
            if briefing:
                print(f"Briefing generated successfully for {briefing.briefing_date}")
                print(f"Included {len(briefing.articles)} top articles.")
            else:
                print("No briefing could be generated (possibly no news today).")
            
        if not (args.seed or args.ingest or args.briefing):
            parser.print_help()
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
