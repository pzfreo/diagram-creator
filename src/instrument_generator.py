"""
Main Generator Orchestrator

This file coordinates between parameters, validation, and geometry generation.
You rarely need to modify this - it's the "glue" code.
"""

from typing import Dict, Any, List, Tuple
import json


def generate_violin_neck(params_json: str) -> str:
    """
    Main entry point called from JavaScript.

    Args:
        params_json: JSON string of parameter values

    Returns:
        JSON string containing:
        {
            "success": bool,
            "views": {
                "side": str,
                "top": str,
                "cross_section": str
            } | null,
            "errors": List[str]
        }
    """
    try:
        # Parse parameters
        params = json.loads(params_json)

        # Import here to ensure modules are loaded
        from instrument_parameters import validate_parameters
        from instrument_geometry import generate_multi_view_svg

        # Validate parameters
        is_valid, errors = validate_parameters(params)

        if not is_valid:
            return json.dumps({
                "success": False,
                "views": None,
                "errors": errors
            })

        # Generate geometry (all 3 views)
        try:
            views = generate_multi_view_svg(params)

            return json.dumps({
                "success": True,
                "views": views,
                "errors": []
            })

        except Exception as e:
            return json.dumps({
                "success": False,
                "views": None,
                "errors": [f"Geometry generation failed: {str(e)}"]
            })

    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "views": None,
            "errors": [f"Invalid parameter JSON: {str(e)}"]
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "views": None,
            "errors": [f"Unexpected error: {str(e)}"]
        })


def get_derived_values(params_json: str) -> str:
    """
    Calculate derived values for the frontend.
    
    Args:
        params_json: JSON string of parameter values
        
    Returns:
        JSON string containing derived values dictionary
    """
    try:
        from instrument_geometry import calculate_derived_values
        
        params = json.loads(params_json)
        derived = calculate_derived_values(params)
        
        return json.dumps({
            "success": True,
            "values": derived
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


def get_parameter_definitions() -> str:
    """
    Get parameter definitions for UI generation.
    
    Returns:
        JSON string of parameter definitions
    """
    try:
        from instrument_parameters import get_parameters_as_json
        return get_parameters_as_json()
    except Exception as e:
        return json.dumps({
            "error": f"Failed to load parameters: {str(e)}"
        })


def get_presets() -> str:
    """
    Get available parameter presets from the presets directory.

    Returns:
        JSON string of presets dictionary: { preset_id: { name: str, parameters: dict } }
    """
    try:
        import os
        presets = {}

        # Get path to presets directory (relative to this file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        presets_dir = os.path.join(current_dir, '..', 'presets')

        # Check if presets directory exists
        if not os.path.exists(presets_dir):
            return json.dumps({})

        # Load all JSON files from presets directory
        for filename in os.listdir(presets_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(presets_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        preset_data = json.load(f)

                    # Extract parameters and instrument name
                    if 'parameters' in preset_data:
                        params = preset_data['parameters']
                        instrument_name = params.get('instrument_name', filename.replace('.json', ''))

                        # Use filename without extension as preset ID
                        preset_id = filename.replace('.json', '')
                        presets[preset_id] = {
                            'name': instrument_name,
                            'parameters': params
                        }
                except Exception as e:
                    print(f"Warning: Failed to load preset {filename}: {str(e)}")
                    continue

        return json.dumps(presets)
    except Exception as e:
        return json.dumps({
            "error": f"Failed to load presets: {str(e)}"
        })


if __name__ == '__main__':
    # Test the generator
    from instrument_parameters import get_default_values
    import json
    
    print("Testing violin neck generator...")
    print("=" * 50)
    
    # Get defaults
    defaults = get_default_values()
    params_json = json.dumps(defaults)
    
    print("\n1. Testing parameter definitions...")
    param_defs = get_parameter_definitions()
    print(f"✓ Loaded {len(json.loads(param_defs)['parameters'])} parameters")
    
    print("\n2. Testing generation...")
    result = generate_violin_neck(params_json)
    result_data = json.loads(result)

    if result_data['success']:
        print(f"✓ Generation successful!")
        views = result_data['views']
        print(f"  Side view: {len(views['side'])} bytes")
        print(f"  Top view: {len(views['top'])} bytes")
        print(f"  Cross-section: {len(views['cross_section'])} bytes")
    else:
        print(f"✗ Generation failed:")
        for error in result_data['errors']:
            print(f"  - {error}")
    
    print("\n3. Testing presets...")
    presets = get_presets()
    preset_data = json.loads(presets)
    print(f"✓ Loaded {len(preset_data)} presets")
    
    print("\n" + "=" * 50)
    print("All tests complete!")
