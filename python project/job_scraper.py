import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SEARCH_TERM = "python developer"
LOCATION = "New Delhi"
PAGES = 2  # Number of pages to scrape
CSV_FILE = "jobs.csv"

def scrape_jobs():
    jobs = []
    for page in range(PAGES):
        start = page * 10
        url = (f"https://www.indeed.com/jobs?q={SEARCH_TERM.replace(' ', '+')}"
               f"&l={LOCATION.replace(' ', '+')}&start={start}")
        print(f"Scraping page {page+1}: {url}")
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        cards = soup.find_all("div", class_="job_seen_beacon")
        for card in cards:
            title = card.find("h2", class_="jobTitle")
            link = title.find("a", href=True)["href"] if title else None
            jobs.append({
                "Job Title": title.get_text(strip=True) if title else None,
                "Company": card.find("span", {"data-testid":"company-name"}).get_text(strip=True)
                           if card.find("span", {"data-testid":"company-name"}) else None,
                "Location": card.find("div", {"data-testid":"text-location"}).get_text(strip=True)
                            if card.find("div", {"data-testid":"text-location"}) else None,
                "URL": f"https://www.indeed.com{link}" if link else None
            })
        time.sleep(random.uniform(1, 3))
    return jobs

def load_previous():
    return pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else pd.DataFrame()

def save_jobs(df):
    df.to_csv(CSV_FILE, index=False)

def main():
    print("Starting job scraping...")
    new_data = pd.DataFrame(scrape_jobs())
    old_data = load_previous()
    if not old_data.empty:
        merged = new_data.merge(old_data, on="URL", how="left", indicator=True)
        new_jobs = merged[merged["_merge"]=="left_only"]
    else:
        new_jobs = new_data

    if not new_jobs.empty:
        print(f"Found {len(new_jobs)} new job(s):")
        print(new_jobs[["Job Title", "Company", "Location", "URL"]])
    else:
        print("No new jobs found.")

    save_jobs(new_data)
    print("Done. Data saved to", CSV_FILE)

if __name__ == "__main__":
    main()
