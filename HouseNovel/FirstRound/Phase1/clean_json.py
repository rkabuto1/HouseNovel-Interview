# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-
# This script performs post-processing and quality assurance on the output of a prior OCR-parsed JSON file 
# ('structured_residents_1912.json') generated from a 1912 Minneapolis city directory. Its goal is to clean and validate 
# the structured entries before final submission.
# The script applies several validation and transformation rules:
#
# 1. It detects and removes invalid entries where the first or last name contains terms that typically indicate a 
#   non-resident record, such as "hotel", "building", "flats", or "company".
# 2. It filters out entries with incomplete or malformed addresses — for example, an address that only includes a number 
#   without a street name.
# 3. It post-processes occupation fields to extract spouse names from widow notations. If the occupation field contains 
#   a pattern like '(wid John)', the string 'John' is reassigned to the 'spouse_name' field and the occupation is cleared.
#
# Cleaned and valid entries are written to 'cleaned_residents_1912.json'. Rejected entries are logged for transparency 
# and further inspection in 'rejected_entries.txt'. The script also prints a summary of how many entries were cleaned 
# and rejected.
# This script helps ensure that the final structured data meets the accuracy expectations outlined in the assignment — 
# particularly the 98–100% accuracy target when manual QA or corrective logic is applied to OCR output.
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-

import json
import re

INPUT_FILE = "structured_residents_1912.json"
OUTPUT_FILE = "cleaned_residents_1912.json"
REJECTED_FILE = "rejected_entries.txt"

JUNK_TERMS = {"hotel", "building", "flats", "apartments", "realty", "company", "co"}

def is_junk_name(name: str) -> bool:
    return any(term in name.lower() for term in JUNK_TERMS)

def is_incomplete_address(address: str) -> bool:
    return address.strip().isdigit() or len(address.strip().split()) < 2

def clean_entry(entry):
    occupation = entry["occupation"]
    spouse = entry["spouse_name"]
    wid_match = re.match(r"\(wid\s+(.+?)\)", occupation or "")
    if wid_match:
        entry["spouse_name"] = wid_match.group(1)
        entry["occupation"] = None

    return entry

def is_valid(entry):
    if is_junk_name(entry["first_name"]) or is_junk_name(entry["last_name"]):
        return False
    if is_incomplete_address(entry["home_address"]):
        return False
    return True

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []
rejected = []

for entry in data:
    cleaned_entry = clean_entry(entry)
    if is_valid(cleaned_entry):
        cleaned.append(cleaned_entry)
    else:
        rejected.append(entry)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2)

with open(REJECTED_FILE, "w", encoding="utf-8") as f:
    for entry in rejected:
        f.write(json.dumps(entry, indent=2) + "\n\n")

print(f"Cleaned {len(cleaned)} entries")
print(f"Rejected {len(rejected)} entries (see {REJECTED_FILE})")
print(f"Output written to {OUTPUT_FILE}")
