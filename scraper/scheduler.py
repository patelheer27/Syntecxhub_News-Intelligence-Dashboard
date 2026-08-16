import schedule
import time

from scraper import run_scraper


def job():
    print("\n" + "=" * 60)
    print("Automatic scraping started...")
    print("=" * 60)

    try:
        run_scraper()
        print("Automatic scraping completed successfully.")

    except Exception as e:
        print(f"Scheduler error: {e}")


# Run once immediately when scheduler starts
job()

# Run every 30 minutes
schedule.every(30).minutes.do(job)

print("\nScheduler is running...")
print("Next scraping will happen after 30 minutes.")
print("Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)