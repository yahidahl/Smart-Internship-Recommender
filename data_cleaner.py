import pandas as pd

# Load the scraped CSV file
df = pd.read_csv("python_internships.csv")

# Step 1: Drop duplicates
df.drop_duplicates(inplace=True)

# Step 2: Fill missing values (NaN) with 'N/A'
df.fillna("N/A", inplace=True)

# Step 3: Clean stipend data (remove ₹, handle ranges, lump sums, and non-standard values)
def clean_stipend(stipend):
    if "Unpaid" in stipend:  # Handling "Unpaid" internships
        return 0
    if "Not Available" in stipend or "Not provided" in stipend:  # Handle missing values
        return 0
    try:
        # Handle $ currency (convert to ₹)
        if "$" in stipend:
            stipend = stipend.replace("$", "₹")
        
        # Handle range stipend (e.g., ₹ 8,000 - 10,000 /month)
        if " - " in stipend and "₹" in stipend:
            amount_range = stipend.split(" - ")
            min_amount = int(''.join(filter(str.isdigit, amount_range[0])))
            max_amount = int(''.join(filter(str.isdigit, amount_range[1].split(" /")[0])))
            return (min_amount + max_amount) // 2  # Take the average
        
        # Handle lump sum stipend (e.g., ₹ 1,00,000 - 1,10,000 lump sum)
        elif "lump sum" in stipend:
            amount_range = stipend.split(" - ")
            min_amount = ''.join(filter(str.isdigit, amount_range[0].replace("₹", "").strip()))
            max_amount = ''.join(filter(str.isdigit, amount_range[1].split(" ")[0].replace("₹", "").strip()))
            
            # Convert to integers after removing non-numeric characters
            min_amount = int(min_amount)
            max_amount = int(max_amount)
            
            return (min_amount + max_amount) // 2  # Take the average
        
        # Handle other formats like ₹ 5,000 /month
        else:
            amount = ''.join(filter(str.isdigit, stipend.split(" /")[0].replace("₹", "").strip()))  # Remove ₹ and extra text
            return int(amount)  # Convert to integer
    except Exception as e:
        print(f"Error processing stipend: {stipend} -> {e}")
        return 0  # If stipend is not properly formatted

df["Stipend_cleaned"] = df["Stipend"].apply(clean_stipend)

# Step 4: Save cleaned data to a new CSV
df.to_csv("cleaned_internships.csv", index=False)

print("✅ Cleaned data saved as cleaned_internships.csv")
