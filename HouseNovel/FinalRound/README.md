# HouseNovel Spot Check: Final Round

This repository contains a full OCR-to-JSON pipeline for extracting structured resident data from printed pages 104–108 of the **1900 Minneapolis city directory**.

- Demo Recording:  
  [Loom Video Walkthrough](https://www.loom.com/share/cca10d088cf7485ebe0e24d471f658e8?sid=322b6b9d-cd5b-4585-87f2-46016eec6e00)

### WorkFlow

---
### 1. Downloading the PDF Pages

I began by locating pages 104 through 108 of the 1900 Minneapolis city directory using the internal scan page numbers (pg_seq=112–116). These were originally presented as high resolution web images. I saved each page locally as a PDF to preserve the image clarity for offline processing.

---

### 2. Converting PDFs to High-Resolution JPEGs

Next, I used ImageMagick’s magick CLI tool to convert each PDF page into a JPEG file. This resolution is ideal for text recognition. Each command took a PDF like Page104.pdf and generated a corresponding page_104_pg112.jpg image.

---

### 3. Extracting Text via Tesseract OCR

With the images ready, I ran Tesseract OCR on each JPEG file. This step transformed the scanned images into raw, searchable text files like page_104_pg112.txt. I ran five Tesseract commands, and all output files were successfully created and saved in the ocr/ folder. These text files are the input for the next phase: parsing the structured resident data into JSON.

---

### 4. Reviewing the OCR Output

After completing the Tesseract OCR conversion on the scanned pages of the 1900 Minneapolis city directory, I began by manually inspecting the resulting .txt files, starting with page_104_pg112.txt. I examined how the OCR output structured each resident’s entry and identified consistent patterns such as names appeared first, followed by occupations, addresses, and occasionally spouse names or company references.

---

### 5. Parsing with `extract_residents.py`

Next, I designed a Python script called extract_residents.py to transform this semi structured text into structured JSON data. I used regular expressions and pattern recognition to segment each line into fields like FirstName, LastName, Spouse, Occupation, CompanyName, and a nested HomeAddress dictionary with subfields like StreetNumber, StreetName, ApartmentOrUnit, and ResidenceIndicator. I also included DirectoryName and PageNumber metadata in each record to maintain traceability. I encoded logical assumptions into the script. For example, treating any line that included "wid" as a widow reference and extracting the spouse name accordingly.

---

### 6. Automating with `Makefile`

To automate the extraction and cleanup process, I created a Makefile with defined targets for each step. The run target first executed extract_residents.py, which generated the structured output as structured_residents.json. Immediately after, it invoked a second script called filter_occupations.py, which scanned for invalid Occupation values, specifically any that were just single letter OCR artifacts, and nullified them. This script then overwrote the original output file with the cleaned version.
