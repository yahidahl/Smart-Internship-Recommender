# scheduler.py

import schedule
import time
from scraper import fetch_internships

def job():
    print(f"[Scheduler] Job started at {time.strftime('%Y-%m-%d %H:%M')}")
    fetch_internships("python", pages=2)
    print(f"[Scheduler] Job finished at {time.strftime('%Y-%m-%d %H:%M')}")

# Schedule the job every Sunday at 10:00 AM
schedule.every().sunday.at("10:00").do(job)

print("=== Scheduler running. Press Ctrl+C to exit. ===")
while True:
    schedule.run_pending()
    time.sleep(30)
