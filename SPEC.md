SPEC.md — Custom Binary Columnar Format Specification
Custom Columnar Storage Format (CCF) Specification

This document describes the structure of a custom binary columnar file format designed for efficient storage and selective column access.

1. Magic Number

Every file begins with this 4-byte magic number to identify the format:

0x43434601     // "CCF" version 1


Stored in little-endian.

2. File Layout Overview

A file consists of:

+-----------------------+
| Header                |
+-----------------------+
| Schema Section        |
+-----------------------+
| Column 1 Block        |
+-----------------------+
| Column 2 Block        |
+-----------------------+
| ...                   |
+-----------------------+
| Column N Block        |
+-----------------------+

3. Header Structure (Fixed Size)

The header contains metadata needed to read the file.

Field	Type	Size	Description
magic_number	uint32	4	Must equal 0x43434601
num_columns	uint16	2	Number of columns
num_rows	uint32	4	Number of rows
schema_size	uint32	4	Size of the schema section in bytes
column_offsets	uint64[]	8 × N	Byte offsets to each column block

➡ Offsets allow column pruning — only required columns are read.

4. Schema Section

Defines column names and data types.

For each column:

Field	Type	Description
name_length	uint16	Length of column name
name	bytes	UTF-8 encoded column name
dtype	uint8	1=int32, 2=float64, 3=utf8 string
5. Column Block Format

Each column is stored separately for efficient reads.

A column block contains:

+---------------------------+
| uncompressed_size (u32)   |
+---------------------------+
| compressed_size (u32)     |
+---------------------------+
| zlib_compressed_data      |
+---------------------------+


Compression uses zlib.

5.1 Integer and Float Columns

Values are packed in little-endian binary format:

int32 → struct.pack("<i")

float64 → struct.pack("<d")

Then compressed.

5.2 String Columns

String columns are stored using two parts:

(A) Offsets Array

An array of uint32 values:

offsets[i] = ending position of string i in the data buffer


Example:

["cat", "dog", "lion"]
offsets = [3, 6, 10]

(B) Data Buffer

Concatenated UTF-8 bytes:

"catdoglion"


Both parts together are compressed.

6. Endianness

All numeric fields use little-endian encoding.

7. Advantages of This Format

Columnar layout → faster selective access

Compression → reduced file size

Offsets → efficient variable-length string decoding

Simple header → easy to parse

END OF SPECIFICATION
