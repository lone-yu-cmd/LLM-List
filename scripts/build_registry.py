import json
import os
import glob
import shutil
import subprocess
import sys
from datetime import datetime
try:
    from generate_schema import generate_schema
except ImportError:
    # Handle case where script is run from root
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    from generate_schema import generate_schema

def resolve_refs(data, base_dir):
    """
    Recursively resolves $ref fields in the JSON data.
    """
    if isinstance(data, dict):
        if "$ref" in data:
            ref_path = os.path.join(base_dir, data["$ref"])
            try:
                with open(ref_path, 'r', encoding='utf-8') as f:
                    # Load the referenced content
                    ref_content = json.load(f)
                    # Merge it with the original dict (excluding $ref)
                    merged = data.copy()
                    del merged["$ref"]
                    merged.update(ref_content)
                    return resolve_refs(merged, base_dir)
            except Exception as e:
                print(f"Error resolving ref {ref_path}: {e}")
                return data
        else:
            return {k: resolve_refs(v, base_dir) for k, v in data.items()}
    elif isinstance(data, list):
        return [resolve_refs(item, base_dir) for item in data]
    else:
        return data

def merge_registry():
    """
    Scans the registry/providers directory for JSON files and merges them
    into a single llm_registry.json file.
    """
    
    # Base structure
    registry = {
        "$schema": "./schema/llm_registry_schema.json",
        "version": "1.0.0",
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
        "description": "Registry of LLM providers, their API configurations, and supported models.",
        "providers": []
    }

    # Path to project root
    root_dir = os.path.dirname(os.path.dirname(__file__))
    # Path to providers directory
    providers_dir = os.path.join(root_dir, 'registry', 'providers')
    
    # 0. Generate Schema first
    print("Generating updated JSON Schema...")
    try:
        generate_schema()
    except Exception as e:
        print(f"Warning: Schema generation failed: {e}")

    # Check if directory exists
    if not os.path.exists(providers_dir):
        print(f"Directory not found: {providers_dir}")
        return

    # Iterate over all JSON files in the providers directory
    json_files = glob.glob(os.path.join(providers_dir, '*.json'))
    json_files.sort() # Ensure consistent order

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                provider_data = json.load(f)
                # Basic validation: check if 'id' and 'name' exist
                if 'id' not in provider_data or 'name' not in provider_data:
                    print(f"Warning: Skipping {os.path.basename(file_path)} - missing 'id' or 'name'")
                    continue
                
                # Resolve $ref dependencies
                resolved_data = resolve_refs(provider_data, root_dir)
                
                registry["providers"].append(resolved_data)
                print(f"Loaded provider: {provider_data.get('name')} ({os.path.basename(file_path)})")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error reading {file_path}: {e}")

    # Write the merged registry to the root directory
    output_path = os.path.join(root_dir, 'llm_registry.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully generated {output_path}")

        # Distribute to SDKs
        # Target map: registry_path -> schema_dir
        # We now output registry to 'data/' subdirectory in each SDK
        sdk_targets = {
            os.path.join(root_dir, 'sdks', 'js', 'data', 'llm_registry.json'): 
                os.path.join(root_dir, 'sdks', 'js', 'schema'),
            
            os.path.join(root_dir, 'sdks', 'python', 'llm_list', 'data', 'llm_registry.json'):
                os.path.join(root_dir, 'sdks', 'python', 'llm_list', 'schema'),
                
            os.path.join(root_dir, 'sdks', 'go', 'data', 'llm_registry.json'):
                os.path.join(root_dir, 'sdks', 'go', 'schema')
        }
        
        schema_source = os.path.join(root_dir, 'schema', 'llm_registry_schema.json')

        for target_path, schema_dir in sdk_targets.items():
            # Ensure the directory exists
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # 1. Sync Registry JSON
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            
            # 2. Sync Schema JSON
            if os.path.exists(schema_source):
                os.makedirs(schema_dir, exist_ok=True)
                shutil.copy2(schema_source, os.path.join(schema_dir, 'llm_registry_schema.json'))
                print(f"Successfully synced registry and schema to {os.path.relpath(os.path.dirname(target_path), root_dir)}")
            else:
                print(f"Warning: Schema source not found at {schema_source}")
            
            # 3. Cleanup old files (if they exist in the parent directory)
            # target_path is like .../sdks/js/data/llm_registry.json
            # parent is .../sdks/js/data
            # grand_parent is .../sdks/js
            # We want to delete .../sdks/js/llm_registry.json
            grand_parent = os.path.dirname(os.path.dirname(target_path))
            old_file = os.path.join(grand_parent, 'llm_registry.json')
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                    print(f"Cleaned up old file: {os.path.relpath(old_file, root_dir)}")
                except Exception as e:
                    print(f"Failed to delete old file {old_file}: {e}")

        # 4. Verify SDKs
        print("\nRunning SDK Verification...")
        
        # JS Verification
        print("\n[JS SDK] Verifying...")
        try:
            subprocess.run(["npm", "test"], cwd=os.path.join(root_dir, 'sdks', 'js'), check=True)
            print("✓ JS SDK Verified")
        except subprocess.CalledProcessError:
            print("✗ JS SDK Verification Failed")
            # Don't exit yet, try others
        
        # Python Verification
        print("\n[Python SDK] Verifying...")
        try:
            subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], cwd=os.path.join(root_dir, 'sdks', 'python'), check=True)
            print("✓ Python SDK Verified")
        except subprocess.CalledProcessError:
            print("✗ Python SDK Verification Failed")

        # Go Verification
        print("\n[Go SDK] Verifying...")
        try:
            subprocess.run(["go", "test", "./..."], cwd=os.path.join(root_dir, 'sdks', 'go'), check=True)
            print("✓ Go SDK Verified")
        except subprocess.CalledProcessError:
            print("✗ Go SDK Verification Failed")

    except Exception as e:
        print(f"Error writing output file: {e}")


        print(f"Total providers: {len(registry['providers'])}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    merge_registry()
