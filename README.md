# Blender Godot Curve3D Exporter

A lightweight Blender add-on that exports **Bezier curves** directly to Godot 4's native `Curve3D` resource format (`.tres` files).

This tool makes it much easier to create complex paths, roads, rails, orbits, or procedural tracks in Blender and bring them into Godot without manual point placement.

## Features

- Export Bezier curves to Godot 4 `.tres` format (native `Curve3D`)
- **Batch export** support — export all selected curves at once (each gets its own `.tres` file named after the object)
- **Apply Object Transform** — bakes location, rotation, and scale into the curve (recommended)
- **Apply Modifiers** — applies modifiers non-destructively before export (Array, Mirror, Curve, etc.)
- Automatic Blender Z-up → Godot Y-up axis conversion
- Preserves control handles (left/right) and **tilt** values
- Supports closed/cyclic curves (`use_cyclic_u`)
- Simple File → Export menu integration

## Installation

1. Download `curve_exporter.py` from the repository (or the latest release)
2. In Blender go to **Edit → Preferences → Add-ons → Install…**
3. Select the `curve_exporter.py` file
4. Enable the add-on (search for "Godot Curve3D")

## Usage

### Single Curve Export (default)
1. Select a single **Bezier Curve** object
2. Go to **File → Export → Export Curve3D (.tres)**
3. Adjust options if needed:
   - **Apply Object Transform** (default: On)
   - **Apply Modifiers** (default: Off)
4. Choose filename and export

### Batch Export
1. Select multiple Curve objects
2. Go to **File → Export → Export Curve3D (.tres)**
3. Check the box **"Export All Selected Curves"**
4. Choose a destination **folder**
5. Click Export — each curve will be saved as `ObjectName.tres`

### In Godot 4
- Create a `Path3D` node
- Drag the exported `.tres` file onto the `curve` property
- Use with `PathFollow3D` for animation, procedural generation, etc.

## Options

| Option                    | Default | Description |
|---------------------------|---------|-----------|
| Apply Object Transform    | On      | Bakes location/rotation/scale into the curve data |
| Apply Modifiers           | Off     | Applies all modifiers before exporting |
| Export All Selected Curves| Off     | Batch mode — exports every selected curve to a folder |

## Limitations

- Only **Bezier** curves are supported (NURBS and Poly curves are skipped)
- Exports only the **first spline** of each curve object
- Axis remapping includes a Z-flip to better match common Godot expectations (can be adjusted if needed)

## License

MIT License  
See [LICENSE](LICENSE) for full text.

---

Made with :heart: for the Blender â†” Godot community  
Questions / issues ↔ open an issue or ping [@zecona](https://x.com/zecona) on X
