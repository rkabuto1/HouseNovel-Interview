import re
import json
from typing import List, Dict
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-
# This script reads OCR processed text from a historical city directory file specifically, the 1912 Minneapolis directory,
# extracts structured resident data, and outputs the results in JSON format.
# The script uses a regular expression to identify and parse entries that follow the pattern:
# Last Name, First Name , optional Middle Name , optional spouse name, occupation, 
# residence indicator, and home address.
# It assigns parsed values into a structured dictionary with fields such as first_name, last_name, spouse_name, 
# residence_indicator, home_address, occupation, employer, business_address, and year. Fields for employer and 
# business_address are left as None in this version.
# The resulting entries are written to a JSON file called 'structured_residents_1912.json', and the first five entries 
# are printed to the console for preview.
#
# This script assumes that the input OCR text is stored in a file named 'ocr_output.txt'. It also assumes a relatively 
# clean OCR output with consistent formatting and is designed to be extended with additional post-processing logic 
# as needed 
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
with open("ocr_output.txt", "r", encoding="utf-8") as f:
    ocr_text = f.read()

directory_year = 1912

res_entry_pattern = re.compile(
    r"""
    ^(?P<last>[A-Z][a-z]+)                     
    \s+(?P<first>[A-Z][a-zA-Z\.]*)              
    (?:\s+(?P<middle>[A-Z][a-zA-Z\.]*))?        
    (?:\s+\((?P<spouse>[^)]+)\))?               
    \s+(?P<occupation>.*?)                      
    \s+(?P<residence_indicator>rms?|b|h|res\.?) 
    \s+(?P<home_address>[\d]+.*?)$              
    """, re.VERBOSE | re.MULTILINE
)

def parse_match_to_entry(match) -> Dict:
    return {
        "first_name": match.group("first"),
        "last_name": match.group("last"),
        "spouse_name": match.group("spouse") or None,
        "residence_indicator": match.group("residence_indicator"),
        "home_address": match.group("home_address"),
        "occupation": match.group("occupation").strip() or None,
        "employer": None,
        "business_address": None,
        "year": directory_year
    }

entries: List[Dict] = []
for match in res_entry_pattern.finditer(ocr_text):
    entry = parse_match_to_entry(match)
    entries.append(entry)

with open("structured_residents_1912.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2)

print(json.dumps(entries[:5], indent=2))
