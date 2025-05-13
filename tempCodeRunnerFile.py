import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_internships(skill, pages=1):
    base_url = f"https://internshala.com/internships/{skill}-internship"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    internships = []

    for page in range(pages):
        url = f"{base_url}/page-{page + 1}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"[✗] Failed to fetch page {page + 1}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", class_="individual_internship")

        for item in listings:
            # Extracting the title
            title = item.find("a", class_="job-title-href")
            title = title.get_text(strip=True) if title else "Not Available"
            
            # Extracting the company
            company = item.find("p", class_="company-name")
            company = company.get_text(strip=True) if company else "Not Available"

            # Extracting the location
            location = item.find("div", class_="locations")
            if location:
                location = location.get_text(strip=True).replace("\n", "").replace("\r", "")
            else:
                location = "Not Available"

            # Extracting the stipend
            stipend = item.find("span", class_="stipend")
            stipend = stipend.get_text(strip=True) if stipend else "Not Available"

            # Extracting the date (posted time)
            date = item.find("span", class_="status-inactive")
            if date:
                date = date.get_text(strip=True)
                # Remove unwanted texts like "Job offer post internship" or "Be an early applicant"
                if "Job offer" in date or "Be an early applicant" in date:
                    date = "Not Available"
            else:
                # Fallback: check if there's another date element, like "duration"
                date = item.find("div", class_="detail-row-2")
                if date:
                    date = date.get_text(strip=True).replace("\n", "").replace("\r", "")
                else:
                    date = "Not Available"

            internships.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Stipend": stipend,
                "Date": date
            })

        time.sleep(1)  # be polite to the server

    if internships:
        df = pd.DataFrame(internships)
        filename = f"{skill.lower()}_internships.csv"
        df.to_csv(filename, index=False)
        print(f"[✓] Saved to {filename}")
    else:
        print("[!] No internships found. Try again or check if Internshala blocked scraping.")

if __name__ == "__main__":
    fetch_internships("python", pages=2)
