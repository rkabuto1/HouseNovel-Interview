import os
import json
import re
# ========================================================================================
# Psuedocode:
# 1. Loads a manually OCR text file for a given page of the city directory.
# 2. Filters out junk lines 
# 3. Joins multi line entries into complete resident records using regex heuristics.
# 4. Uses regular expressions to extract structured fields
#     - Full name 
#     - Spouse name 
#     - Home address 
#     - Occupation and Company 
# 5. Handle ditto marked last names from previous entries
# 6. Outputs structured data as a list of JSON objects
# ========================================================================================
TXT_FILE = "ocr/txt-files/page_105_pg113.txt"
OUTPUT_FILE = "structured_residents.json"
DIRECTORY_NAME = "Minneapolis 1900"
PAGE_NUMBER = 105

entry_pattern = re.compile(r'^([A-Z][a-zA-Z\'".&-]+(?: [A-Z][a-zA-Z\'".&-]+)*),?\s+(.*)$')
spouse_pattern = re.compile(r'\b(?:wife|wid(?:ow)? of|wid)\s+([A-Z][a-zA-Z. ]+)', re.IGNORECASE)
address_pattern = re.compile(r'\b(\d{3,5})\s+([A-Za-z0-9 .]+?)(?:[,.]|$)')
home_hint = re.compile(r'\b(h|r)\b', re.IGNORECASE)

def is_junk_line(line):
    if not line.strip():
        return True
    if line.strip().isupper():
        return True
    ad_words = ['directory', 'tackle', 'furnished', 'trunks', 'messengers', 'butter', 'store', 'laundry', 'tel']
    if any(word in line.lower() for word in ad_words):
        return True
    if "see also" in line.lower():
        return True
    return False

def split_name(name):
    parts = name.strip().split()
    if len(parts) >= 2:
        return " ".join(parts[1:]), parts[0]
    return name.strip(), None

def parse_entry(line, last_lastname):
    if not line:
        return None, last_lastname
    if line[0] in ('"', '“', '”'):
        line = last_lastname + " " + line[1:].lstrip()
    match = entry_pattern.match(line)
    if not match:
        return None, last_lastname
    full_name, rest = match.groups()
    if ',' in full_name:
        last, first = [p.strip() for p in full_name.split(',', 1)]
    else:
        first, last = split_name(full_name)

    last_lastname = last or last_lastname
    spouse_match = spouse_pattern.search(rest)
    spouse = spouse_match.group(1).strip() if spouse_match else None
    addr_match = address_pattern.search(rest)
    home_address = None
    if addr_match:
        home_address = {
            "StreetNumber": addr_match.group(1),
            "StreetName": addr_match.group(2).strip().rstrip('.'),
            "ApartmentOrUnit": None,
            "ResidenceIndicator": "h" if home_hint.search(rest) else None
        }
    occ_chunk = rest.split(',')[0].strip()
    occupation, company = None, None
    if ' at ' in occ_chunk:
        occupation, company = [p.strip() for p in occ_chunk.split(' at ', 1)]
    else:
        occupation = occ_chunk

    return {
        "FirstName": first,
        "LastName": last_lastname,
        "Spouse": spouse,
        "Occupation": occupation,
        "CompanyName": company,
        "HomeAddress": home_address,
        "WorkAddress": None,
        "Telephone": None,
        "DirectoryName": DIRECTORY_NAME,
        "PageNumber": PAGE_NUMBER
    }, last_lastname

def join_multiline_entries(lines):
    entries = []
    buffer = ''
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^[A-Z"]', line): 
            if buffer:
                entries.append(buffer)
            buffer = line
        else:
            buffer += ' ' + line
    if buffer:
        entries.append(buffer)
    return entries

def main():
    results = []
    last_lastname = ""

    with open(TXT_FILE, 'r') as f:
        raw_lines = f.readlines()

    entries = join_multiline_entries(raw_lines)
    for line in entries:
        if is_junk_line(line):
            continue
        parsed, last_lastname = parse_entry(line, last_lastname)
        if parsed:
            results.append(parsed)

    with open(OUTPUT_FILE, 'w') as out:
        json.dump(results, out, indent=2)
    print(f"Extracted {len(results)} residents from page {PAGE_NUMBER} into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
