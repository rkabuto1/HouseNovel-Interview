import json
INPUT_FILE = "structured_residents.json"  
OUTPUT_FILE = INPUT_FILE  
# =======================================================================================
# 1. Loads the existing structured JSON resident data.
# 2. Iterates through each resident entry and checks if the Occupation field for single letter
# 3. If the occupation is a single letter, sets the Occupation field to `None`.
# =======================================================================================

def is_single_letter(occupation):
    return isinstance(occupation, str) and len(occupation.strip()) == 1 and occupation.isalpha()

def main():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    for entry in data:
        if is_single_letter(entry.get("Occupation", "")):
            entry["Occupation"] = None

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print("Filtered Finished.")

if __name__ == "__main__":
    main()
