# sun.py
"""
Voxelized Sun model for uvoxid.
All distances are in micrometers (µm).
"""

# --- Solar constants ---
R_SUN_UM = 696_340_000_000_000  # Sun mean radius (µm)

# Approximate layer boundaries (scaled from solar physics)
# Fractions of solar radius (rounded for simulation use)
solar_layers = [
    {"name": "Core", 
     "r_min": 0, 
     "r_max": int(0.25 * R_SUN_UM)},  # ~25% radius
    {"name": "Radiative Zone", 
     "r_min": int(0.25 * R_SUN_UM), 
     "r_max": int(0.70 * R_SUN_UM)},  # ~25%–70%
    {"name": "Convective Zone", 
     "r_min": int(0.70 * R_SUN_UM), 
     "r_max": int(1.00 * R_SUN_UM)},  # ~70%–100%
    {"name": "Photosphere", 
     "r_min": int(0.999 * R_SUN_UM), 
     "r_max": R_SUN_UM},             # thin ~500 km skin
    {"name": "Corona (approx)", 
     "r_min": R_SUN_UM, 
     "r_max": int(2.00 * R_SUN_UM)}, # extends well beyond surface
]

def classify_sun_r(r_um: int) -> str:
    """
    Return solar layer name for a given radius in µm.
    """
    for layer in solar_layers:
        if layer["r_min"] <= r_um <= layer["r_max"]:
            return layer["name"]
    return "Interplanetary Space"

def is_inside_sun(r_um: int) -> bool:
    """
    Check if a radius is inside the solar body (≤ mean radius).
    """
    return r_um <= R_SUN_UM


# --- Example usage ---
if __name__ == "__main__":
    test_radii = [
        0,
        int(0.2 * R_SUN_UM),   # Core
        int(0.5 * R_SUN_UM),   # Radiative
        int(0.8 * R_SUN_UM),   # Convective
        int(0.9995 * R_SUN_UM),# Photosphere
        int(1.5 * R_SUN_UM),   # Corona
        int(3.0 * R_SUN_UM),   # Outside
    ]
    for r in test_radii:
        print(r, "→", classify_sun_r(r))
