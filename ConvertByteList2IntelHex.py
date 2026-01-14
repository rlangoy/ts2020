def to_intel_hex_little_endian(input_lines, start_address=0x0000, record_size=16):
    """
    Convert 32-bit hex words to Intel HEX format (little-endian).
    """

    # Convert words into byte array (little-endian)
    data = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue

        word = int(line, 16)
        data.extend([
            word & 0xFF,
            (word >> 8) & 0xFF,
            (word >> 16) & 0xFF,
            (word >> 24) & 0xFF,
        ])

    hex_lines = []
    addr = start_address

    for i in range(0, len(data), record_size):
        chunk = data[i:i + record_size]
        byte_count = len(chunk)
        address = addr & 0xFFFF
        record_type = 0x00

        record = [byte_count, address >> 8, address & 0xFF, record_type] + chunk
        checksum = (-sum(record)) & 0xFF

        hex_line = ":" + "".join(f"{b:02X}" for b in record) + f"{checksum:02X}"
        hex_lines.append(hex_line)

        addr += byte_count

    # End-of-file record
    hex_lines.append(":00000001FF")

    return hex_lines


if __name__ == "__main__":
    input_data = [
        "00500113",
        "00C00193",
        "FF718393",
        "0023E233",
        "0041F2B3",
        "004282B3",
        "02728863",
        "0041A233",
        "00020463",
        "00000293",
        "0023A233",
        "005203B3",
        "402383B3",
        "0471AA23",
        "06002103",
        "005104B3",
        "008001EF",
        "00100113",
        "00910133",
        "0221A023",
        "00210063",
    ]

    for line in to_intel_hex_little_endian(input_data):
        print(line)
