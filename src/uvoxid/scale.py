import math

def uvoxid_scale(ssc_str: str) -> str:
    """
    Estimate the spatial resolution (in meters) for an uvoxid Base32 string.
    Resolution is derived from how many significant Base32 characters remain
    after stripping leading 'A's.
    """
    # Remove prefix and dashes
    clean = ssc_str.replace("uvoxid:", "").replace("-", "")

    # Count leading 'A's
    leading_as = len(clean) - len(clean.lstrip("A"))
    total_len = len(clean)

    # Significant characters = total minus leading As
    sig_chars = total_len - leading_as

    # --- Compute resolution ---
    # Each Base32 char = 5 bits
    bits_used = sig_chars * 5
    bits_unused = (total_len * 5) - bits_used

    # Base resolution at Earth’s surface: ~1 µm
    base_res_m = 1e-6  

    # Effective resolution grows by factor of 2 for each unused bit
    res_m = base_res_m * (2 ** bits_unused)

    # Human-readable scaling
    if res_m >= 1_000:
        scale = f"{res_m/1000:.2f} km"
    elif res_m >= 1:
        scale = f"{res_m:.2f} m"
    elif res_m >= 0.001:
        scale = f"{res_m*100:.2f} cm"
    elif res_m >= 1e-6:
        scale = f"{res_m*1e6:.2f} µm"
    elif res_m >= 1e-9:
        scale = f"{res_m*1e9:.2f} nm"
    else:
        scale = f"{res_m:.2e} m"

    return f"Resolution ≈ {scale} [{sig_chars} sig chars, {bits_used} bits used]"


# --- Example usage ---
if __name__ == "__main__":
    examples = [
        "uvoxid:AAAAAAAAAAAAAAAA",
        "uvoxid:AAAAAAAAAAAAAAAF",
        "uvoxid:AAAAAAAAAAAAAAFL",
        "uvoxid:AAAAAAAAAAAAAFLV",
        "uvoxid:AAAAAAAAAAAAFLVF",
        "uvoxid:AAAAAAAAAAAFLVFI",
        "uvoxid:AAAAAAAAAAFLVFIA",
        "uvoxid:AAAAAAAAAFLVFIAB",
        "uvoxid:AAAAAAAAFLVFIABC",
        "uvoxid:AAAAAAAFLVFIABCD",
        "uvoxid:AAAAAAFLVFIABCDC",
        "uvoxid:AAAAAFLVFIABCDBC",
        "uvoxid:AAAAFLVFIABCDBCD",
        "uvoxid:AAAFVFIABCDBCDBD",
        "uvoxid:AAFLVFIABCDBCDBD",
        "uvoxid:AFLVFIABCDBCDBCD",
        "uvoxid:FLVFIABCDBCDBCDB"
    ]

    for ex in examples:
        print(ex, "→", uvoxid_scale(ex))
