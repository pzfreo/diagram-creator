# Instrument Presets

This directory contains preset configurations for different instruments. Each preset is a JSON file that defines all the parameters for a specific instrument setup.

## Adding a New Preset

1. Create a new JSON file in this directory (e.g., `my_viola.json`)
2. Add the filename to the `presets.json` manifest file
3. Use the same format as the existing presets:

```json
{
  "metadata": {
    "version": "1.0",
    "timestamp": "2025-01-01T00:00:00.000Z",
    "description": "Description of this preset",
    "generator": "Instrument Neck Geometry Generator"
  },
  "parameters": {
    "instrument_name": "Display Name in Dropdown",
    "vsl": 328.5,
    "body_stop": 195.0,
    "neck_stop": 130.0,
    "body_length": 355.0,
    "rib_height": 30.0,
    "fingerboard_length": 270.0,
    "arching_height": 15.0,
    "belly_edge_thickness": 3.5,
    "bridge_height": 33.0,
    "overstand": 12.0,
    "fb_thickness_at_nut": 5.0,
    "fb_thickness_at_join": 7.0,
    "string_height_nut": 0.6,
    "string_height_eof": 4.0,
    "fingerboard_width_at_nut": 24.0,
    "fingerboard_width_at_end": 30.0,
    "show_measurements": true
  }
}
```

3. The preset will automatically appear in the dropdown menu with the name specified in `parameters.instrument_name`

## Preset Manifest

The `presets.json` file lists all available presets. When you add a new preset file, update this manifest:

```json
{
  "presets": [
    "basic_violin.json",
    "modern_viola.json",
    "your_new_preset.json"
  ]
}
```

## File Format

- The filename (without `.json`) is used as the preset ID
- The `instrument_name` parameter is used as the display name in the dropdown
- All parameters in the `parameters` object should match the available instrument parameters

## Tips

- You can save your current parameters from the web UI using the "Save" button to create a properly formatted JSON file
- Copy and modify existing presets to create new ones
- Keep filenames simple and descriptive (e.g., `basic_violin.json`, `modern_cello.json`)
