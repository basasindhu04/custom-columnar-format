import sys
from writer import write_custom_file

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_custom.py input.csv output.ccf")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_file = sys.argv[2]

    write_custom_file(input_csv, output_file)
    print("Created:", output_file)
