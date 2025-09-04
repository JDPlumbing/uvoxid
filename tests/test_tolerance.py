import pytest
from datetime import datetime
from uvoxid.core import encode_uvoxid
from uvoxid.utils.tolerance import (
    truncate_to_tolerance,
    equal_within_tolerance,
    snap_to_tolerance,
)

EARTH_RADIUS_UM = 6_371_000_000_000


@pytest.fixture
def nearby_voxels():
    """Two nearly identical UVoxIDs, slightly offset in lat/lon."""
    uv1 = encode_uvoxid(EARTH_RADIUS_UM, int(25.76 * 1e6), int(-80.19 * 1e6))
    uv2 = encode_uvoxid(EARTH_RADIUS_UM, int(25.760001 * 1e6), int(-80.190001 * 1e6))
    return uv1, uv2


def test_truncate_to_tolerance_bits(nearby_voxels):
    uv1, _ = nearby_voxels
    truncated = truncate_to_tolerance(uv1, 6)  # keep 6 chars = 30 bits
    assert isinstance(truncated, int)
    assert truncated.bit_length() <= 192


def test_equal_within_tolerance_true(nearby_voxels):
    uv1, uv2 = nearby_voxels
    # At low precision, they should be equal
    assert equal_within_tolerance(uv1, uv2, 6)


def test_equal_within_tolerance_false(nearby_voxels):
    uv1, uv2 = nearby_voxels
    # At very high precision, tiny differences show up
    assert not equal_within_tolerance(uv1, uv2, 38)



def test_snap_to_tolerance_format(nearby_voxels):
    uv1, _ = nearby_voxels
    snapped = snap_to_tolerance(uv1, 6)
    assert snapped.startswith("uvoxid:")
    assert len(snapped.replace("uvoxid:", "").replace("-", "")) == 39
    assert "A" in snapped  # padding


def test_snap_consistency(nearby_voxels):
    uv1, uv2 = nearby_voxels
    snap1 = snap_to_tolerance(uv1, 6)
    snap2 = snap_to_tolerance(uv2, 6)
    assert snap1 == snap2
