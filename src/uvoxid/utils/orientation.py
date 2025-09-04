# src/uvoxid/utils/orientation.py

from uvoxid import decode_uvoxid

def spherical_delta(uv1: int, uv2: int) -> dict:
    """
    Compute differences between two UVoxID positions.

    Args:
        uv1 (int): first UVoxID (192-bit integer).
        uv2 (int): second UVoxID (192-bit integer).

    Returns:
        dict with:
          - dr_um: radial change in micrometers
          - dlat_deg: latitude delta in degrees
          - dlon_deg: longitude delta in degrees (normalized to [-180, 180])
    """
    r1, lat1, lon1 = decode_uvoxid(uv1)
    r2, lat2, lon2 = decode_uvoxid(uv2)

    dr_um = r2 - r1
    dlat_deg = (lat2 - lat1) / 1e6
    dlon_deg = (lon2 - lon1) / 1e6

    # Normalize longitude delta into [-180, 180]
    if dlon_deg > 180:
        dlon_deg -= 360
    elif dlon_deg < -180:
        dlon_deg += 360

    return {
        "dr_um": dr_um,
        "dlat_deg": dlat_deg,
        "dlon_deg": dlon_deg,
    }

# Example usage
if __name__ == "__main__":
    from uvoxid import encode_uvoxid

    EARTH_RADIUS_UM = 6_371_000_000_000

    # Miami vs. NYC
    miami = encode_uvoxid(EARTH_RADIUS_UM, int(25.76 * 1e6), int(-80.19 * 1e6))
    nyc   = encode_uvoxid(EARTH_RADIUS_UM, int(40.71 * 1e6), int(-74.01 * 1e6))

    delta = spherical_delta(miami, nyc)
    print(delta)
    # → {'dr_um': 0, 'dlat_deg': 14.95, 'dlon_deg': 6.18}
