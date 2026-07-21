import os

# =====================================================
# Input and output filenames
# =====================================================
BIT_FILE = "red_pitaya_top.bit"
BIN_FILE = "fpga.bin"

# Xilinx sync word
SYNC = b'\xFF\xFF\xFF\xFF\xAA\x99\x55\x66'

# -----------------------------------------------------
# Read the .bit file
# -----------------------------------------------------
with open(BIT_FILE, "rb") as f:
    data = f.read()

# Locate the start of the FPGA bitstream
sync_index = data.find(SYNC)

if sync_index == -1:
    raise RuntimeError("ERROR: Xilinx sync word not found.")

print(f"Sync word found at byte: {sync_index}")

# Extract the raw bitstream
bitstream = data[sync_index:]

print(f"Extracted bitstream size: {len(bitstream)} bytes")

# -----------------------------------------------------
# Swap bytes within every 32-bit word
# Example:
# 11 22 33 44  --> 44 33 22 11
# -----------------------------------------------------
swapped = bytearray()

for i in range(0, len(bitstream), 4):

    word = bitstream[i:i+4]

    if len(word) == 4:
        swapped.extend(word[::-1])
    else:
        # Copy any remaining bytes unchanged
        swapped.extend(word)

# -----------------------------------------------------
# Save fpga.bin
# -----------------------------------------------------
with open(BIN_FILE, "wb") as f:
    f.write(swapped)

print("\nConversion completed successfully.")
print(f"Input : {os.path.abspath(BIT_FILE)}")
print(f"Output: {os.path.abspath(BIN_FILE)}")
print(f"Output size: {len(swapped)} bytes")