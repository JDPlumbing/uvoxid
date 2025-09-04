"""
tolerance.py — utilities for handling tolerances in UVoxID space.

In UVoxID, each Base32 character = 5 bits of resolution.
Tolerances are applied by truncating the UVoxID to a certain
number of significant Base32 characters (sig_chars).
"""

from ..formats import uvoxid_to_b32, b32_to_uvoxid


TOTAL_BITS = 192
BITS_PER_CHAR = 5


def truncate_to_tolerance(uvoxid: int, sig_chars: int) -> int:
    """
    Truncate a UVoxID integer to a given number of significant Base32 characters.

    Args:
        uvoxid (int): 192-bit UVoxID integer.
        sig_chars (int): Number of significant Base32 characters to preserve (1–39).

    Returns:
        int: truncated UVoxID integer with lower bits zeroed out.
    """
    keep_bits = sig_chars * BITS_PER_CHAR
    if keep_bits > TOTAL_BITS:
        raise ValueError(f"sig_chars too large, max is {TOTAL_BITS // BITS_PER_CHAR}")

    mask = ((1 << keep_bits) - 1) << (TOTAL_BITS - keep_bits)
    return uvoxid & mask


def equal_within_tolerance(a: int, b: int, sig_chars: int) -> bool:
    """
    Check if two UVoxIDs are equal within a given tolerance.

    Args:
        a (int): first UVoxID integer
        b (int): second UVoxID integer
        sig_chars (int): tolerance level (number of Base32 chars to match)

    Returns:
        bool: True if equal within tolerance, False otherwise.
    """
    return truncate_to_tolerance(a, sig_chars) == truncate_to_tolerance(b, sig_chars)


def snap_to_tolerance(uvoxid: int, sig_chars: int) -> str:
    """
    Convert a UVoxID to its Base32 string snapped at given tolerance.

    Args:
        uvoxid (int): 192-bit UVoxID integer.
        sig_chars (int): tolerance level (number of Base32 chars to keep).

    Returns:
        str: truncated Base32 string with padding 'A's.
    """
    truncated = truncate_to_tolerance(uvoxid, sig_chars)
    b32 = uvoxid_to_b32(truncated)
    prefix = b32.replace("uvoxid:", "").replace("-", "")[:sig_chars]
    return f"uvoxid:{prefix}{'A' * (39 - sig_chars)}"


# --- Example usage ---
if __name__ == "__main__":
    from ..core import encode_uvoxid

    EARTH_RADIUS_UM = 6_371_000_000_000
    uv1 = encode_uvoxid(EARTH_RADIUS_UM, int(25.76 * 1e6), int(-80.19 * 1e6))
    uv2 = encode_uvoxid(EARTH_RADIUS_UM, int(25.760001 * 1e6), int(-80.190001 * 1e6))

    print("Exact equal:", uv1 == uv2)
    print("Equal at 6 sig chars (~mm scale):", equal_within_tolerance(uv1, uv2, 6))
    print("Snapped uv1 @ 6 chars:", snap_to_tolerance(uv1, 6))
    print("Snapped uv2 @ 6 chars:", snap_to_tolerance(uv2, 6))
