import csv
import struct
import zlib

DTYPE_INT = 1
DTYPE_FLOAT = 2
DTYPE_STRING = 3


def detect_type(value):
    try:
        int(value)
        return DTYPE_INT
    except:
        pass

    try:
        float(value)
        return DTYPE_FLOAT
    except:
        pass

    return DTYPE_STRING


def encode_column(values, dtype):
    if dtype == DTYPE_INT:
        raw = b"".join(struct.pack("<i", int(v)) for v in values)
        return raw

    elif dtype == DTYPE_FLOAT:
        raw = b"".join(struct.pack("<d", float(v)) for v in values)
        return raw

    elif dtype == DTYPE_STRING:
        offsets = []
        data = b""
        pos = 0
        for v in values:
            bts = v.encode("utf-8")
            data += bts
            pos += len(bts)
            offsets.append(pos)

        offsets_bytes = b"".join(struct.pack("<I", o) for o in offsets)
        return offsets_bytes + data

    else:
        raise ValueError("Unknown dtype")


def write_custom_file(input_csv, output_file):
    with open(input_csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        columns = {h: [] for h in header}

        for row in reader:
            for h, v in zip(header, row):
                columns[h].append(v)

    num_rows = len(next(iter(columns.values())))
    num_columns = len(columns)

    dtypes = {}
    for name in header:
        dtypes[name] = detect_type(columns[name][0])

    schema = b""
    for name in header:
        name_bytes = name.encode("utf-8")
        schema += struct.pack("<H", len(name_bytes))
        schema += name_bytes
        schema += struct.pack("<B", dtypes[name])

    schema_size = len(schema)

    column_blocks = []
    for name in header:
        dtype = dtypes[name]
        values = columns[name]

        raw = encode_column(values, dtype)
        compressed = zlib.compress(raw)

        block = struct.pack("<I", len(raw))
        block += struct.pack("<I", len(compressed))
        block += compressed

        column_blocks.append(block)

    offsets = []
    current_offset = 4 + 2 + 4 + 4 + (8 * num_columns) + schema_size
    for block in column_blocks:
        offsets.append(current_offset)
        current_offset += len(block)

    header_bytes = b""
    header_bytes += struct.pack("<I", 0x43434601)
    header_bytes += struct.pack("<H", num_columns)
    header_bytes += struct.pack("<I", num_rows)
    header_bytes += struct.pack("<I", schema_size)
    for off in offsets:
        header_bytes += struct.pack("<Q", off)

    with open(output_file, "wb") as f:
        f.write(header_bytes)
        f.write(schema)
        for block in column_blocks:
            f.write(block)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python writer.py input.csv output.ccf")
        exit(1)

    write_custom_file(sys.argv[1], sys.argv[2])
    print("File written:", sys.argv[2])
