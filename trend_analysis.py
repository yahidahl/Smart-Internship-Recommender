import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime, timedelta

# 1) Load data
df = pd.read_csv("cleaned_internships.csv")

# 2) Top 5 Cities
top_locations = df["Location"].value_counts().head(5)
top_locations.plot(kind='bar', color='skyblue')
plt.title("Top 5 Cities with Most Internships")
plt.ylabel("Number of Internships")
plt.xlabel("City")
plt.xticks(rotation=45)
plt.show()
plt.close()

# 3) Average stipend
avg = df["Stipend_cleaned"].mean()
print(f"Average stipend: ₹ {avg:,.2f}")

# 4) Top companies
top_companies = df["Company"].value_counts().head(5)
top_companies.plot(kind='bar', color='lightgreen')
plt.title("Top 5 Companies with Most Internships")
plt.ylabel("Number of Internships")
plt.xlabel("Company")
plt.xticks(rotation=45)
plt.show()
plt.close()

# 5) All locations bar plot
loc_counts = df["Location"].value_counts()
loc_counts.plot(kind='bar', figsize=(10,6), color='lightcoral')
plt.title("Internships in Different Locations")
plt.ylabel("Number of Internships")
plt.xlabel("City")
plt.xticks(rotation=90)
plt.show()
plt.close()

# 6) Parse relative dates
def parse_relative_date(s):
    s = str(s)
    if re.search(r'\bToday\b', s):
        return datetime.today()
    m = re.search(r'(\d+)\s+day', s)
    if m: return datetime.today() - timedelta(days=int(m.group(1)))
    m = re.search(r'(\d+)\s+week', s)
    if m: return datetime.today() - timedelta(weeks=int(m.group(1)))
    m = re.search(r'(\d+)\s+month', s)
    if m: return datetime.today() - timedelta(days=30*int(m.group(1)))
    return pd.NaT

df['Date_parsed'] = df['Date'].apply(parse_relative_date)
df = df.dropna(subset=['Date_parsed'])

# 7) Line plot over time
df['Week'] = df['Date_parsed'].dt.isocalendar().week
postings_per_week = df.groupby('Week').size()

postings_per_week.plot(kind='line', marker='o', color='teal')
plt.title("Internship Postings Over Time")
plt.ylabel("Number of Postings")
plt.xlabel("ISO Week Number")
plt.grid(True)
plt.show()
plt.close()
