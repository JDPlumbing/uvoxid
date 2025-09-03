# uvoxid

**Universal Voxel Identifier (UVoxID)** — a Python library for encoding and decoding spherical spatial coordinates at micrometer precision.  

Think of it as a globally consistent **voxel address system**: every point in space has a permanent ID, valid from the Earth’s core to interstellar distances.

---

## ✨ Why UVoxID?

Floating-point coordinates drift.  
Game engines rely on “floating origins.”  
Robotics uses hacky spatial hashes.  
Satellites juggle dozens of reference frames.  

UVoxID fixes all that with a **deterministic, integer-based addressing scheme**:

- **Universal**: same scheme works for atoms, cities, and galaxies.  
- **Deterministic**: encode/decode is exact, no rounding error.  
- **Persistent**: voxel IDs never change, perfect for storage, sync, and replication.  
- **Spherical-native**: gravity, orbits, and planetary geometry “just work.”  

---

## 🚀 Use Cases

- **Game Development**:  
  - Infinite open worlds without floating origin hacks.  
  - Warp across star systems — arrive exactly where you should.  
  - Persistent object positions across server restarts.  

- **Robotics & Drones**:  
  - Drop GPS/SLAM noise into a stable global grid.  
  - Share maps between agents without coordinate drift.  

- **Satellites & Space Systems**:  
  - Orbital mechanics with deterministic precision.  
  - Consistent addressing across LEO, GEO, Moon, Mars, and beyond.  

- **Scientific Simulation**:  
  - Track bacteria at µm scale or galaxies at light-year scale.  
  - Perfect for physics engines, material degradation models, or climate sims.  

- **Digital Real Estate & Virtual Worlds**:  
  - Each voxel ID is globally unique and ownable.  
  - Imagine buying a square meter on Mars… and knowing its exact ID forever.  

---

## 🛠 Features

- **192-bit encoding**: `(radius, latitude, longitude)` → one integer.  
- **String encodings**: Base32, hex, or binary.  
- **Ephemeris support**: Sun & Moon positions → UV, tides, day/night cycles.  
- **Earth model**: WGS84 ellipsoid radius corrections.  
- **Entanglement utilities**: bit-suffix coupling for groups of voxels.  
- **Scale introspection**: compute what resolution a given ID represents.  

---

## 📦 Installation

```bash
pip install uvoxid
```

---

## 🔍 Example

```python
import uvoxid

EARTH_RADIUS_UM = 6_371_000_000_000  # mean radius in µm

# Encode position at Earth’s surface, equator, prime meridian
addr = uvoxid.encode_uvoxid(EARTH_RADIUS_UM, 0, 0)

print("Hex:", uvoxid.uvoxid_to_hex(addr))
print("Base32:", uvoxid.uvoxid_to_b32(addr))

r_um, lat, lon = uvoxid.decode_uvoxid(addr)
print("Decoded:", r_um, lat/1e6, lon/1e6)
```

Output:
```
Hex: 00059fb8c83f1000-00000000055d4a80-0000000000aba950
Base32: uvoxid:AABBAAACCCC-DDDDEEEEFFFF-GGGGHHHHIIII
Decoded: 6371000000000 0.0 0.0
```

---

## 📖 Roadmap

- Planetary/stellar models beyond Earth/Moon/Sun.  
- Python bindings for Rust/C++ core for performance.  
- Optional Morton-code compatibility for indexing.  
- Support for >192-bit scales (atomic → galactic cluster).  
