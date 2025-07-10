EXTRACT = extract_residents.py
FILTER = filter_occupations.py
OUTPUT = structured_residents.json

.PHONY: all run clean

all: run

run:
	@echo "Finding the residents"
	python3 $(EXTRACT)
	@echo "Filtering Occupations"
	python3 $(FILTER)

clean:
	@echo "Output Cleaned"
	rm -f $(OUTPUT)
