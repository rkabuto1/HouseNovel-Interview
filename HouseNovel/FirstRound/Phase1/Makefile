.PHONY: all run clean

all: run

run:
	@echo "Running OCR parser"
	python3 parse_directory.py
	@echo "Running post-processing and cleanup"
	python3 clean_json.py
	@echo "Phase 1 complete. Cleaned output saved to cleaned_residents_1912.json"

clean:
	rm -f structured_residents_1912.json cleaned_residents_1912.json rejected_entries.txt
