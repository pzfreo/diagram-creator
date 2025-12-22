
import re

# Access the files
geo_file = 'src/instrument_geometry.py'
params_file = 'src/instrument_parameters.py'

# 1. Parse definitions from parameters file
defined_params = set()
with open(params_file, 'r') as f:
    content = f.read()
    # Regex to find keys in INSTRUMENT_PARAMETERS dict
    # Look for patterns like 'some_key': NumericParameter( or 'some_key': EnumParameter(
    matches = re.findall(r"'([a-zA-Z0-9_]+)':\s*[A-Z][a-zA-Z]+Parameter", content)
    defined_params.update(matches)

# 2. Parse usage from geometry file
used_params = set()
with open(geo_file, 'r') as f:
    content = f.read()
    # Regex to find params.get('key') or params['key']
    matches_get = re.findall(r"params\.get\(['\"]([a-zA-Z0-9_]+)['\"]", content)
    matches_bracket = re.findall(r"params\['([a-zA-Z0-9_]+)'\]", content)
    
    used_params.update(matches_get)
    used_params.update(matches_bracket)

# 3. Find missing
missing = used_params - defined_params

print("Defined Parameters:")
print(sorted(list(defined_params)))
print("\nUsed Parameters:")
print(sorted(list(used_params)))

print("\nMISSING PARAMETERS (Used but not defined):")
for p in sorted(list(missing)):
    print(f"- {p}")
