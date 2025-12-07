import struct
import zlib

DTYPE_INT = 1
DTYPE_FLOAT = 2
DTYPE_STRING = 3


def read_header(f):
    magic = struct.unpack("<I", f.read(4))[0]
    if magic != 0x43434601:
        raise ValueError("Invalid file format")

    num_columns = struct.unpack("<H", f.read(2))[0]
    num_rows = struct.unpack("<I", f.read(4))[0]
    schema_size = struct.unpack("<I", f.read(4))[0]

    offsets = []
    for _ in range(num_columns):
        offsets.append(struct.unpack("<Q", f.read(8))[0])

    return num_columns, num_rows, schema_size, offsets


def read_schema(f, schema_size):
    schema_data = f.read(schema_size)

    pos = 0
    schema = []

    while pos < schema_size:
        name_len = struct.unpack("<H", schema_data[pos:pos+2])[0]
        pos += 2

        name = schema_data[pos:pos+name_len].decode("utf-8")
        pos += name_len

        dtype = schema_data[pos]
        pos += 1

        schema.append((name, dtype))

    return schema


def decode_column(f, offset, dtype, num_rows):
    f.seek(offset)

    uncompressed_size = struct.unpack("<I", f.read(4))[0]
    compressed_size = struct.unpack("<I", f.read(4))[0]

    compressed = f.read(compressed_size)
    raw = zlib.decompress(compressed)

    values = []

    if dtype == DTYPE_INT:
        for i in range(num_rows):
            v = struct.unpack("<i", raw[i*4:(i+1)*4])[0]
            values.append(v)

    elif dtype == DTYPE_FLOAT:
        for i in range(num_rows):
            v = struct.unpack("<d", raw[i*8:(i+1)*8])[0]
            values.append(v)

    elif dtype == DTYPE_STRING:
        offsets = []
        pos = 0

        for i in range(num_rows):
            end = struct.unpack("<I", raw[pos:pos+4])[0]
            offsets.append(end)
            pos += 4

        data = raw[pos:]

        prev = 0
        for end in offsets:
            values.append(data[prev:end].decode("utf-8"))
            prev = end

    else:
        raise ValueError("Unknown dtype")

    return values


def read_custom_file(path):
    with open(path, "rb") as f:
        num_columns, num_rows, schema_size, offsets = read_header(f)
        schema = read_schema(f, schema_size)

        table = {}
        for (name, dtype), offset in zip(schema, offsets):
            table[name] = decode_column(f, offset, dtype, num_rows)

        return table


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python reader.py input.ccf")
        exit(1)

    table = read_custom_file(sys.argv[1])
    for col, values in table.items():
        print(col, values)
