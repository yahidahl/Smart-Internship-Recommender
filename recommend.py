import pandas as pd

def recommend_internships(csv_file, skill=None, location=None, min_stipend=0):
    # Load CSV
    df = pd.read_csv(csv_file)

    # Clean stipend to extract numeric value
    def clean_stipend(stipend):
        try:
            if "Unpaid" in stipend:
                return 0
            elif "₹" in stipend:
                stipend = stipend.replace("₹", "").replace(",", "").strip()
                parts = stipend.split(" /")
                return int(parts[0])
            else:
                return 0
        except:
            return 0

    df["Stipend_cleaned"] = df["Stipend"].apply(clean_stipend)

    # Apply filters
    if location:
        df = df[df["Location"].str.contains(location, case=False, na=False)]

    if min_stipend > 0:
        df = df[df["Stipend_cleaned"] >= min_stipend]

    # Show top 5 matches
    recommendations = df.head(5)

    if recommendations.empty:
        print("No internships found matching the criteria.")
    else:
        print("\n🎯 Top Internship Recommendations:\n")
        for i, row in recommendations.iterrows():
            print(f"{i+1}. {row['Title']} at {row['Company']}")
            print(f"   Location: {row['Location']}")
            print(f"   Stipend: {row['Stipend']}")
            print(f"   Posted On: {row['Date']}")
            print("-" * 50)

# Example usage
if __name__ == "__main__":
    recommend_internships("python_internships.csv", location="Work from home", min_stipend=5000)
