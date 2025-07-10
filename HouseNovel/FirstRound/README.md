# 🗂️ HouseNovel Final Round Assignment: README

---

## Phase One: OCR + Structured Data Extraction (1900–1950)

Using scanned Minneapolis city directories from 1900 to 1950, extract and structure the following data for each resident entry:  
https://box2.nmtvault.com/Hennepin2/jsp/RcWebBrowse.jsp

• First and last name  
• Spouse name (if listed)  
• Home address  
• Residence indicator (e.g., h., res.)  
• Occupation  
• Employer/business name and address (if applicable)  
• Year of directory  

**Output format:** JSON  
Please include notes on any formatting challenges and how you addressed them.

---

## Phase Two: Real-World Application – 1807 Dupont Ave S (built 1902)

Apply your workflow to the following address to create a timeline of past residents between 1902 and 1950:

**Address:**  
1807 Dupont Ave S, Minneapolis, MN 55403  

**Zillow listing:**  
https://www.zillow.com/homedetails/1807-Dupont-Ave-S-Minneapolis-MN-55403/1951320_zpid  

For each year the home is listed, include:  
• Resident full name(s)  
• Spouse name (if listed)  
• Occupation and employer  
• Business address (if listed)  
• Any formatting inconsistencies, gaps, or assumptions  
• Notes on how you validated or cross-referenced the accuracy  

This simulates how we use directory data in actual home history reports.

---

## Accuracy Expectations

We recognize OCR accuracy will vary by decade and layout. As a general benchmark:

- 1850s–1870s: ~50–65% OCR-only accuracy; 90–100% with AI + manual QA  
- 1880s–1899: ~65–80% OCR-only accuracy; 95–100% with AI + manual QA  
- 1900–1950: ~85–95% OCR-only accuracy; 98–100% with AI + manual QA  

---

## Additional Question

Many of our future datasets involve handwritten records from the 1800s. Do you have any experience with handwriting OCR or manual transcription, and would you feel comfortable working with handwritten materials?

---

## Phase 1  
### Thought Process Behind Each Step

I approached Phase 1 as a data extraction and quality assurance pipeline, where OCR text from historical directories needed to be parsed, structured, and validated with high accuracy. I broke the problem into three logical phases: parsing, cleaning, and output generation.

Throughout the process, I assumed that perfect OCR text could not be guaranteed, so I treated this as a fault tolerant system favoring clear logic, validation, and explainability over fragile overfitting. This structure also prepares the codebase for future enhancements like employer extraction, multi-line entry stitching, or handwriting model integration.

---

### OCR Text as Input (`ocr_output.txt`)

I assumed the OCR engine would produce line by line text closely resembling the original directory layout. To maximize parsing accuracy, I manually reviewed a few pages across different years to identify recurring patterns like name, occupation, residence marker (r, b, rms), and address.

---

### Parsing with `parse_residents.py`

I wrote a regular expression to capture the structural components of each entry. My assumption was that names start the line, followed by occupation and then a residence indicator and address. I included optional fields like middle name and spouse, anticipating variants like “(wid John)” that carry semantic meaning. The output is structured JSON, which makes it easy to work with programmatically and scalable for downstream use.

---

### Cleaning with `clean_json.py`

I treated the initial parsed data as a raw layer that still required filtering and post processing. I applied logic to reclassify widow information into the spouse field and eliminate junk records based on name keywords like “Hotel” or “Flats.” I also filtered out incomplete addresses, which would degrade data quality in real applications. This separation of concerns ensures parsing and QA are independently testable.

---

### Final Outputs

I split valid data into `cleaned_residents_1912.json` and logged problematic rows in `rejected_entries.txt`. This was intentional as I wanted to preserve transparency, identify edge cases for future rule tuning, and show a pipeline mindset.

---

### Automation with Makefile

To streamline execution, I created a `Makefile` that runs everything in sequence.

---

### Explanation

The script processes OCR derived text from the 1912 Minneapolis city directory to extract structured resident data in JSON format. Each output entry includes first and last name, spouse name if listed, residence indicator (such as “r” for resides, “b” for boards, or “rms” for rooms), home address, occupation, and placeholders for employer and business address. The year of the directory is manually specified.  
The parsing logic assumes that entries begin with a last name followed by a first name and, optionally, a middle initial. If the line contains a pattern like “(wid Geo W)”, it is interpreted as widow status, and “Geo W” is assigned to the `spouse_name` field. The occupation is considered to be the text immediately following the name up to the residence indicator. Any entries with names that include terms such as “Hotel,” “Flats,” or “Building” are rejected, as these are more likely commercial listings or OCR errors. Entries with incomplete addresses—such as those containing only a number without a street name—are also filtered out to preserve data integrity.  
Several formatting challenges were encountered. Many entries were wrapped or broken across lines due to OCR artifacts, making employer extraction and address parsing inconsistent. Additionally, abbreviations like "salon" (salesman) or “elk” (clerk) were common and required contextual inference. Some addresses were partially mangled by OCR, such as “4th a? S” instead of “4th av S.”  
For example, “Remsan Katharine (wid Geo W) b 3113” was originally parsed with the widow notation incorrectly assigned to the occupation field. This was corrected by post processing logic. Another error involved “Hotel Berkeley” being parsed as a resident, which was later filtered using keyword-based rejection. Employer and business address extraction remain as future improvements.

---

## How to run my code

1. Ensure you have Python 3 installed.  
2. Place your OCR text file in the project directory as `ocr_output.txt`  
3. Run the full pipeline using:

This will:
    - Parse ocr_output.txt into structured_residents_1912.json
    - Clean and validate the data
    - Output the final result to cleaned_residents_1912.json
    - Log rejected entries to rejected_entries.txt

To remove all generated files, run:
make clean

1. ocr_output.txt – Raw OCR text extracted from a scanned city directory page.
2. parse_residents.py – Parses the OCR text and extracts resident data into structured JSON format.
3. structured_residents_1912.json – Output file containing all parsed entries, including unfiltered data.
4. clean_json.py – Filters and cleans the parsed data by removing invalid entries and correcting field assignments.
5. cleaned_residents_1912.json – Final, cleaned JSON output ready for submission.
6. rejected_entries.txt – Log of entries that were rejected during the cleaning step for QA review.
7. Makefile – Automates the entire Phase 1 pipeline, from parsing to cleaning and output generation.

Phase 2 - https://www.zillow.com/homedetails/1807-Dupont-Ave-S-Minneapolis-MN-55403/1951320_zpid
1807 Dupont Ave S (built 1902)

Apply your workflow to the following address to create a timeline of past residents between 1902 and 1950:

In Phase 2, I focused on systematically constructing a reliable historical timeline of residents at 1807 Dupont Ave S using a combination of OCR processing, manual verification, and prompt-based information extraction. The following steps were completed:

### Targeted OCR Keyword Detection
I wrote a Python script that parsed OCR-scanned city directory text files and automatically searched for instances of the address “1807 Dupont”. The script highlighted relevant lines containing the address, allowing me to quickly locate and isolate potential resident entries across years.

### Validation and Archive Collection (1902–1950)
After identifying hits from the OCR output, I manually confirmed the legitimacy of each entry by verifying that the page referenced the correct address and included resident-level information. I continued this process until I had coverage from 1902 through 1950, with each page manually validated and archived for accuracy.

### Handling Non-Listings and Missing Data
For years in which no valid references to 1807 Dupont Ave S existed, I confirmed this both through OCR and direct page inspection. I clearly marked these entries in the final JSON output using a standardized “Directory not available or address not found in listings” message, ensuring transparency and completeness.

### Prompt-Based Structured Extraction (Prompt Engineering)
Using the validated OCR text from each relevant year, I crafted carefully constructed prompts and applied prompt engineering to extract structured data in JSON format, including fields such as full_name, spouse_name, occupation, employer, and home_address. This allowed me to maintain consistency across decades of historical records despite variation in formatting and terminology.

