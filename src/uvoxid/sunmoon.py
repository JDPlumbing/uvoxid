# sunmoon.py
from datetime import datetime, timezone
from uvoxid import decode_uvoxid
from sunmoon import sun_position, moon_position  # assuming you saved your code in sunmoon.py

def sun_position_uvoxid(ssc: int, when: datetime):
    """
    Compute Sun position for a voxel given by SSC-64.
    Returns (altitude_deg, azimuth_deg)
    """
    r_um, lat_microdeg, lon_microdeg = decode_uvoxid(ssc)
    lat_deg = lat_microdeg / 1e6
    lon_deg = lon_microdeg / 1e6
    return sun_position(lat_deg, lon_deg, when)

def moon_position_uvoxid(ssc: int, when: datetime):
    """
    Compute Moon position for a voxel given by SSC-64.
    Returns (altitude_deg, azimuth_deg)
    """
    r_um, lat_microdeg, lon_microdeg = decode_uvoxid(ssc)
    lat_deg = lat_microdeg / 1e6
    lon_deg = lon_microdeg / 1e6
    return moon_position(lat_deg, lon_deg, when)

# --- Example usage ---
if __name__ == "__main__":
    from uvoxid import encode_uvoxid

    EARTH_RADIUS_UM = 6_371_000_000_000
    now = datetime.now(timezone.utc)

    # Equator / Prime Meridian
    ssc_code = encode_uvoxid(EARTH_RADIUS_UM, 0, 0)

    sun_alt, sun_az = sun_position_uvoxid(ssc_code, now)
    moon_alt, moon_az = moon_position_uvoxid(ssc_code, now)

    print(f"Sun:  alt={sun_alt:.2f}°, az={sun_az:.2f}°")
    print(f"Moon: alt={moon_alt:.2f}°, az={moon_az:.2f}°")
