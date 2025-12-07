# Custom Columnar File Format (CCF)

This project implements a simple binary columnar storage format.  
It includes tools to convert CSV files into the custom format and back.

The format supports:
- Columnar storage
- Per-column compression using zlib
- Selective column reading
- Efficient string storage using offsets

The full technical format description is in `SPEC.md`.

---

## Files in This Project

- `SPEC.md` – Format specification  
- `writer.py` – Writes CSV data into the custom columnar format  
- `reader.py` – Reads data back from the custom columnar format  
- `csv_to_custom.py` – Command-line tool for converting CSV to CCF  
- `custom_to_csv.py` – Command-line tool for converting CCF to CSV  
- `sample.csv` – Example input file  

---

## Requirements

Python 3.8 or higher.

No external libraries are needed besides Python’s built-in modules:
- csv
- struct
- zlib

---

## Usage

### Convert CSV to CCF


Example:

python csv_to_custom.py input.csv output.ccf


Example:



python csv_to_custom.py sample.csv sample.ccf


---

### Convert CCF back to CSV



python custom_to_csv.py input.ccf output.csv


Example:



python custom_to_csv.py sample.ccf restored.csv


---

## How It Works

1. The writer reads a CSV file.
2. Each column is encoded according to its data type:
   - int32
   - float64
   - UTF-8 string (with offsets)
3. Each encoded column is compressed with zlib.
4. Offsets to each column block are written in the header.
5. The reader seeks directly to each column offset and decompresses only that column.

This allows column pruning and efficient reads.

---

## Testing

1. Run csv_to_custom.py to generate a CCF file.
2. Run custom_to_csv.py on the generated file.
3. Compare the restored CSV with the original CSV.

They should match exactly.

---

## Author

This project was created as part of an assignment on designing a custom binary columnar storage format.
