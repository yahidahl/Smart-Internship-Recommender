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
            title_tag = item.find("a", class_="job-title-href")
            title = title_tag.get_text(strip=True) if title_tag else "Not Available"
            
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
                if "Job offer" in date or "Be an early applicant" in date:
                    date = "Not Available"
            else:
                date = item.find("div", class_="detail-row-2")
                if date:
                    date = date.get_text(strip=True).replace("\n", "").replace("\r", "")
                else:
                    date = "Not Available"

            # Extracting skills from the internship details page
            internship_url = "https://internshala.com" + title_tag['href'] if title_tag else ""
            skills = "Not Available"
            if internship_url:
                response_internship = requests.get(internship_url, headers=headers)
                if response_internship.status_code == 200:
                    soup_internship = BeautifulSoup(response_internship.content, "html.parser")
                    skills_container = soup_internship.find("div", class_="round_tabs_container")
                    if skills_container:
                        skills = ", ".join([skill.get_text(strip=True) for skill in skills_container.find_all("span", class_="round_tabs")])
                    else:
                        print(f"[Debug] Skills container not found for internship: {title}")
                else:
                    print(f"[✗] Failed to fetch internship details for {title}")

            internships.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Stipend": stipend,
                "Date": date,
                "Skills": skills,
                "Link": internship_url
            })

        time.sleep(1)  # Be polite to the server

    if internships:
        df = pd.DataFrame(internships)
        filename = f"{skill.lower()}_internships.csv"
        df.to_csv(filename, index=False)
        print(f"[✓] Saved to {filename}")
    else:
        print("[!] No internships found. Try again or check if Internshala blocked scraping.")

if __name__ == "__main__":
    fetch_internships("python", pages=2)
