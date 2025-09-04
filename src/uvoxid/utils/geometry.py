"""
Geometry utilities for UVoxID.
Pure voxel math: no materials, no mass, just counts and volumes.
"""

VOXEL_SIZE_M = 1e-6  # each radial step = 1 µm
VOXEL_VOLUME_M3 = VOXEL_SIZE_M**3  # ~1e-18 m³

def voxel_volume_m3() -> float:
    """Return the volume of a single voxel in cubic meters."""
    return VOXEL_VOLUME_M3

def cube_voxels(side_m: float) -> int:
    """
    Return number of voxels in a cube of given side length (meters).
    """
    return int((side_m / VOXEL_SIZE_M) ** 3)

def sphere_voxels(radius_m: float) -> int:
    """
    Return number of voxels in a sphere of given radius (meters).
    """
    volume_m3 = (4/3) * 3.141592653589793 * (radius_m**3)
    return int(volume_m3 / VOXEL_VOLUME_M3)

def cylinder_voxels(radius_m: float, height_m: float) -> int:
    """
    Return number of voxels in a cylinder.
    """
    volume_m3 = 3.141592653589793 * (radius_m**2) * height_m
    return int(volume_m3 / VOXEL_VOLUME_M3)
