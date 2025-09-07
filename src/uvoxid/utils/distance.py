"""
Distance utilities for UVoxID.
"""

import math
from uvoxid.core import decode_uvoxid

VOXEL_SIZE_M = 1e-6  # 1 µm


def linear_distance(voxid1: int, voxid2: int) -> float:
    """
    Straight-line (chord) distance between two voxels in meters.

    Uses spherical law of cosines on (r, lat, lon). This avoids Cartesian
    conversion and keeps everything in spherical-native UVoxID space.

    Note:
        - For small distances (<1 km), this matches human "straightness"
          within a few µm when applying tolerance rounding.
        - For large scales, this is the actual Euclidean chord through space.
    """
    r1, lat1, lon1 = decode_uvoxid(voxid1)
    r2, lat2, lon2 = decode_uvoxid(voxid2)

    # Convert to meters and radians
    r1_m, r2_m = r1 * 1e-6, r2 * 1e-6
    lat1, lon1 = math.radians(lat1 / 1e6), math.radians(lon1 / 1e6)
    lat2, lon2 = math.radians(lat2 / 1e6), math.radians(lon2 / 1e6)

    # Central angle between points
    cos_gamma = (
        math.sin(lat1) * math.sin(lat2) +
        math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    )
    cos_gamma = max(-1.0, min(1.0, cos_gamma))  # clamp

    gamma = math.acos(cos_gamma)

    # Law of cosines for chord distance
    return math.sqrt(r1_m**2 + r2_m**2 - 2 * r1_m * r2_m * cos_gamma)


def haversine_distance(voxid1: int, voxid2: int) -> float:
    """
    Great-circle (surface) distance in meters.

    Assumes both voxels lie on the surface of the same sphere,
    using the average radius of r1 and r2.
    """
    r1, lat1, lon1 = decode_uvoxid(voxid1)
    r2, lat2, lon2 = decode_uvoxid(voxid2)

    R = ((r1 + r2) / 2) * 1e-6  # mean radius in meters

    lat1, lon1 = math.radians(lat1 / 1e6), math.radians(lon1 / 1e6)
    lat2, lon2 = math.radians(lat2 / 1e6), math.radians(lon2 / 1e6)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
