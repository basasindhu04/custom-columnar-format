import sys
import csv
from reader import read_custom_file

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python custom_to_csv.py input.ccf output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    table = read_custom_file(input_file)

    columns = list(table.keys())
    num_rows = len(table[columns[0]])

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        for i in range(num_rows):
            row = [table[col][i] for col in columns]
            writer.writerow(row)

    print("Created:", output_csv)
