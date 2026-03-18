# Blender → Godot Curve3D Exporter

Export Blender **Bezier curves** directly to Godot 4's `Curve3D` resource format (`.tres`).

This add-on lets you quickly turn Blender curve objects into usable paths for `Path3D`, `PathFollow3D`, ropes, roads, animation tracks, etc. in Godot 4.

## Features

- Exports **Bezier curves** (only) to Godot 4 `.tres` format
- Correctly remaps Blender Z-up → Godot Y-up coordinates
- Preserves **handle positions** (left/right) and **tilt** values
- Simple one-click export from File → Export menu
- Single-spline export (one curve object → one `.tres` file)

## Installation

1. Download the latest release or clone this repository
2. In Blender:  
   **Edit → Preferences → Add-ons → Install…**  
   → select `curve_exporter.py`
3. Search for “Godot Curve3D” and enable the add-on

## Usage

1. In Blender, create or select a **Curve** object (must be Bezier type)
2. Go to **File → Export → Export Curve3D (.tres)**
3. Choose save location and export
4. In Godot 4:
   - Create a `Path3D` node
   - Drag the exported `.tres` file onto the `curve` property  
     (or assign it via the inspector)

Done! The curve should appear correctly oriented in Godot.

## Limitations & Notes

- Only **Bezier** curves are supported (no NURBS, no Poly)
- Exports only the **first spline** of a curve object (multi-spline curves export only spline[0])
- No scale/rotation/location baked in — the curve uses local object-space points (usually what you want for `Path3D`)
- Tilt values are preserved (useful for banked roads, twisting ropes, etc.)

Contributions welcome!

## License

MIT License  
See [LICENSE](LICENSE) for full text.

---

Made with :heart: for the Blender ↔ Godot community  
Questions / issues → open an issue or ping [@zecona](https://x.com/zecona) on X
