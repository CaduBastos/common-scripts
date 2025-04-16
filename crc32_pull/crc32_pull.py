import zlib
import sys

if len(sys.argv) < 2:
    print("Error to execute file! Use: python3 crc32_gen.py <file>")
    sys.exit(1)

file_in = sys.argv[1]
with open(file_in, "rb") as file:
    crc = zlib.crc32(file.read())
    print(f"CRC32: 0x{crc:08X}")
