# uvoxid.py
import base64
import textwrap

# --- SSC-64 Encoding / Decoding ---
def encode_uvoxid(r_um: int, lat_microdeg: int, lon_microdeg: int) -> int:
    """
    Encode spherical coordinates into a 192-bit SSC-64 integer.
    Fixed units:
      - r_um: radius in micrometers (µm)
      - lat_microdeg: latitude in millionths of a degree (-90e6 to +90e6)
      - lon_microdeg: longitude in millionths of a degree (-180e6 to +180e6)
    Returns: 192-bit integer SSC code
    """
    lat_enc = lat_microdeg + 90_000_000
    lon_enc = lon_microdeg + 180_000_000

    # Pack fields: [ r (64b) | lat (64b) | lon (64b) ]
    return (r_um << (64 + 64)) | (lat_enc << 64) | lon_enc


def decode_uvoxid(ssc: int):
    """
    Decode a 192-bit SSC-64 integer back into spherical coordinates.
    Returns (r_um, lat_microdeg, lon_microdeg)
    """
    mask64 = (1 << 64) - 1

    lon_enc = ssc & mask64
    lat_enc = (ssc >> 64) & mask64
    r_um = (ssc >> (64 + 64)) & mask64

    lat_microdeg = lat_enc - 90_000_000
    lon_microdeg = lon_enc - 180_000_000

    return r_um, lat_microdeg, lon_microdeg


# --- Binary / String Helpers ---
def uvoxid_to_bin(ssc: int) -> bytes:
    """Convert 192-bit int → 24-byte binary for storage."""
    return ssc.to_bytes(24, byteorder="big")

def bin_to_uvoxid(b: bytes) -> int:
    return int.from_bytes(b, "big")

def uvoxid_to_hex(ssc: int) -> str:
    """Convert to 48-hex-char string (3 chunks of 16 chars)."""
    raw_hex = f"{ssc:048x}"
    return f"{raw_hex[:16]}-{raw_hex[16:32]}-{raw_hex[32:]}"

def uvoxid_to_b32(ssc: int) -> str:
    """
    Convert to Base32 string grouped by field:
      uvoxid:RRRRRRRRRRRRR-LLLLLLLLLLLLL-MMMMMMMMMMMMM
    Each field (64 bits) -> 13 Base32 chars (unpadded).
    """
    raw = ssc.to_bytes(24, "big")
    r_bytes, lat_bytes, lon_bytes = raw[:8], raw[8:16], raw[16:24]

    r_b32 = base64.b32encode(r_bytes).decode("ascii").rstrip("=")
    lat_b32 = base64.b32encode(lat_bytes).decode("ascii").rstrip("=")
    lon_b32 = base64.b32encode(lon_bytes).decode("ascii").rstrip("=")

    return f"uvoxid:{r_b32}-{lat_b32}-{lon_b32}"


def b32_to_uvoxid(s: str) -> int:
    """
    Decode from 3-field Base32 string back into 192-bit SSC.
    Accepts uvoxid:RRR-LLL-MMM format.
    """
    clean = s.replace("uvoxid:", "")
    r_b32, lat_b32, lon_b32 = clean.split("-")

    # Pad each field back to a multiple of 8 chars (for Base32 decoder)
    def pad_b32(field: str) -> str:
        padlen = (8 - len(field) % 8) % 8
        return field + "=" * padlen

    r_bytes = base64.b32decode(pad_b32(r_b32))
    lat_bytes = base64.b32decode(pad_b32(lat_b32))
    lon_bytes = base64.b32decode(pad_b32(lon_b32))

    raw = r_bytes + lat_bytes + lon_bytes
    return int.from_bytes(raw, "big")



def str_to_uvoxid(s: str) -> int:
    clean = s.replace("uvoxid:", "").replace("-", "")
    padlen = (8 - len(clean) % 8) % 8
    b = base64.b32decode(clean + "="*padlen)
    return int.from_bytes(b, "big")


# --- Example Usage ---
if __name__ == "__main__":
    EARTH_RADIUS_UM = 6_371_000_000_000  # Earth mean radius in µm

    # Equator / Prime Meridian
    ssc_code = encode_uvoxid(EARTH_RADIUS_UM, 0, 0)
    decoded = decode_uvoxid(ssc_code)

    print("Encoded SSC-64 (hex):", uvoxid_to_hex(ssc_code))
    print("Encoded SSC-64 (b32):", uvoxid_to_b32(ssc_code))
    print("Decoded coords:", decoded)
