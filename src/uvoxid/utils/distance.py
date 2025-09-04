"""
Distance utilities for UVoxID.
"""

import math
from uvoxid.core import decode_uvoxid

VOXEL_SIZE_M = 1e-6  # 1 µm

def linear_distance(voxid1: int, voxid2: int) -> float:
    """
    Euclidean distance between two voxels in meters.
    Assumes small-scale (Cartesian approximation).
    """
    r1, lat1, lon1 = decode_uvoxid(voxid1)
    r2, lat2, lon2 = decode_uvoxid(voxid2)

    # Convert µm → m, microdegrees → radians
    x1 = (r1 * 1e-6) * math.cos(math.radians(lat1/1e6)) * math.cos(math.radians(lon1/1e6))
    y1 = (r1 * 1e-6) * math.cos(math.radians(lat1/1e6)) * math.sin(math.radians(lon1/1e6))
    z1 = (r1 * 1e-6) * math.sin(math.radians(lat1/1e6))

    x2 = (r2 * 1e-6) * math.cos(math.radians(lat2/1e6)) * math.cos(math.radians(lon2/1e6))
    y2 = (r2 * 1e-6) * math.cos(math.radians(lat2/1e6)) * math.sin(math.radians(lon2/1e6))
    z2 = (r2 * 1e-6) * math.sin(math.radians(lat2/1e6))

    return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def haversine_distance(voxid1: int, voxid2: int) -> float:
    """
    Great-circle (surface) distance in meters.
    Uses decoded lat/lon and radius of each voxel.
    """
    r1, lat1, lon1 = decode_uvoxid(voxid1)
    r2, lat2, lon2 = decode_uvoxid(voxid2)

    # Assume both are on surface of same sphere (use average radius)
    R = ((r1 + r2) / 2) * 1e-6

    lat1 = math.radians(lat1/1e6)
    lat2 = math.radians(lat2/1e6)
    dlat = lat2 - lat1
    dlon = math.radians((lon2 - lon1) / 1e6)

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
