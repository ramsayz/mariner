for f in os.listdir(folder_path):
    full_path = os.path.join(folder_path, f)
    
    if os.path.isfile(full_path) and not f.lower().endswith(".pdf"):
        os.remove(full_path)
        print(f"Deleted: {f}")

print("Cleanup complete ✅")

import re

def generate_fund_code(file_name):
    # Remove extension
    name = re.sub(r"\.pdf\s*$", "", file_name, flags=re.IGNORECASE)
    
    # Take only part before "NAV"
    name = re.split(r"nav", name, flags=re.IGNORECASE)[0]
    
    # Remove spaces and punctuation
    name = re.sub(r"[^A-Za-z0-9]", "", name)
    
    # Standardize case (upper recommended)
    return name.upper()

results = []

for f in os.listdir(folder_path):
    if f.lower().endswith(".pdf"):
        
        fund_code = generate_fund_code(f)
        
        results.append({
            "Original File Name": f,
            "Fund Code": fund_code
        })

import pandas as pd
df = pd.DataFrame(results)
print(df)



import re

def generate_fund_code(file_name):
    name = re.sub(r"\.pdf\s*$", "", file_name, flags=re.IGNORECASE)
    name = re.split(r"nav", name, flags=re.IGNORECASE)[0]
    name = re.sub(r"[^A-Za-z0-9]", "", name)
    return name.upper()
