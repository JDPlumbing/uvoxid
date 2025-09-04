# src/uvoxid/utils/area.py
"""
Area utilities for UVoxID.

These functions work with decoded UVoxIDs (r, lat, lon)
to compute surface areas on spheres and planar patches.
"""

import math
from uvoxid.core import decode_uvoxid


def spherical_patch_area(r_um: int, lat1_deg: float, lat2_deg: float,
                         lon1_deg: float, lon2_deg: float) -> float:
    """
    Compute the area (in m²) of a spherical quadrilateral patch on a sphere
    bounded by lat/lon coordinates.

    Args:
        r_um (int): radius in micrometers
        lat1_deg, lat2_deg (float): latitude bounds in degrees
        lon1_deg, lon2_deg (float): longitude bounds in degrees

    Returns:
        float: area in square meters
    """
    # Convert radius to meters
    r_m = r_um * 1e-6

    # Convert to radians
    lat1 = math.radians(lat1_deg)
    lat2 = math.radians(lat2_deg)
    lon1 = math.radians(lon1_deg)
    lon2 = math.radians(lon2_deg)

    # Spherical patch area formula:
    # A = R² * (Δλ) * (sin φ2 − sin φ1)
    delta_lon = abs(lon2 - lon1)
    area = (r_m ** 2) * delta_lon * abs(math.sin(lat2) - math.sin(lat1))
    return area


def area_between_voxels(uv1: int, uv2: int) -> float:
    """
    Approximate area (in m²) spanned between two UVoxIDs on the same sphere.
    Useful for bounding box checks.

    Args:
        uv1 (int): UVoxID integer
        uv2 (int): UVoxID integer

    Returns:
        float: surface patch area in square meters
    """
    r1, lat1_micro, lon1_micro = decode_uvoxid(uv1)
    r2, lat2_micro, lon2_micro = decode_uvoxid(uv2)

    if r1 != r2:
        raise ValueError("Both voxels must be on the same spherical shell (same radius).")

    lat1, lat2 = lat1_micro / 1e6, lat2_micro / 1e6
    lon1, lon2 = lon1_micro / 1e6, lon2_micro / 1e6

    return spherical_patch_area(r1, lat1, lat2, lon1, lon2)


# --- Example ---
if __name__ == "__main__":
    EARTH_RADIUS_UM = 6_371_000_000_000
    # 1° by 1° patch at equator
    area = spherical_patch_area(EARTH_RADIUS_UM, 0, 1, 0, 1)
    print(f"1°x1° patch at equator ≈ {area:.2e} m²")
