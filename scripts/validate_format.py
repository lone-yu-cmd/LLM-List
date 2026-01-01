import json
import os
import sys

def check_format(data, path, file_path, errors):
    if isinstance(data, dict):
        # Check if 'type' is present and is a valid schema type definition (str or list)
        # This prevents confusion with properties named 'type'
        if "type" in data and isinstance(data["type"], (str, list)):
            if "format" not in data:
                # Construct a readable path to the field
                field_path = " -> ".join(path)
                errors.append(f"{file_path}: Missing 'format' for field '{field_path}' (type: {data['type']})")
        
        for key, value in data.items():
            check_format(value, path + [key], file_path, errors)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            check_format(item, path + [str(i)], file_path, errors)

def validate_schemas():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    schemas_dir = os.path.join(root_dir, 'registry', 'schemas')
    
    errors = []
    
    for root, dirs, files in os.walk(schemas_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        check_format(data, [], file_path, errors)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if errors:
        print("Found missing 'format' fields:")
        for error in errors:
            print(error)
        sys.exit(1)
    else:
        print("All schema fields have 'format' defined.")
        sys.exit(0)

if __name__ == "__main__":
    validate_schemas()
