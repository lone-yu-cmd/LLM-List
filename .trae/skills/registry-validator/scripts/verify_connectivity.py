import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

def load_registry():
    """Load the registry file."""
    # Located at .trae/skills/registry-validator/scripts/verify_connectivity.py
    # Root is 4 levels up
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, '../../../../'))
    registry_path = os.path.join(root_dir, 'llm_registry.json')
    
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {registry_path} not found. Please run 'npm run build' first.")
        sys.exit(1)

def verify_provider(provider):
    """Verify connectivity for a single provider."""
    pid = provider.get('id')
    name = provider.get('name')
    api_config = provider.get('api_config', {})
    
    print(f"\n--- Verifying {name} ({pid}) ---")
    
    # Check for API Key
    auth_config = api_config.get('auth', {})
    env_var_name = auth_config.get('env_var_suggestion')
    
    if not env_var_name:
        print(f"⚠️  Skipping: No environment variable suggestion found for auth.")
        return False
        
    api_key = os.environ.get(env_var_name)
    if not api_key:
        print(f"⚠️  Skipping: Environment variable {env_var_name} is not set.")
        return False
        
    base_url = api_config.get('base_url')
    if not base_url:
        print(f"❌ Failed: No base_url defined.")
        return False

    # Construct request
    # Try the 'models' endpoint first as it's usually a lightweight GET request
    models_endpoint = api_config.get('endpoints', {}).get('models', {})
    path = models_endpoint.get('path', '/models')
    method = models_endpoint.get('method', 'GET')
    
    target_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add Auth Header
    header_key = auth_config.get('header_key', 'Authorization')
    token_prefix = auth_config.get('token_prefix', 'Bearer')
    headers[header_key] = f"{token_prefix} {api_key}".strip()

    print(f"Testing URL: {target_url}")
    
    try:
        req = urllib.request.Request(target_url, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            if 200 <= status < 300:
                print(f"✅ Success: Connection established (Status {status})")
                return True
            else:
                print(f"❌ Failed: HTTP Status {status}")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: HTTP Error {e.code} - {e.reason}")
        # Try to read error body
        try:
            error_body = e.read().decode('utf-8')
            print(f"   Response: {error_body[:200]}...")
        except:
            pass
        return False
    except urllib.error.URLError as e:
        print(f"❌ Failed: Network Error - {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Failed: Unexpected Error - {str(e)}")
        return False

def main():
    registry = load_registry()
    providers = registry.get('providers', [])
    
    print(f"Loaded {len(providers)} providers from registry.")
    
    results = {"success": [], "skipped": [], "failed": []}
    
    for provider in providers:
        # Verify if we have credentials
        if verify_provider(provider):
            results["success"].append(provider['id'])
        else:
            # Simple heuristic: if we had an env var but failed, it's a failure. 
            # If we skipped due to missing env var, it's a skip.
            # Rerunning logic slightly to classify
            env_var = provider.get('api_config', {}).get('auth', {}).get('env_var_suggestion')
            if env_var and os.environ.get(env_var):
                results["failed"].append(provider['id'])
            else:
                results["skipped"].append(provider['id'])
                
    print("\n=== Summary ===")
    print(f"✅ Successful: {len(results['success'])} ({', '.join(results['success'])})")
    print(f"⚠️  Skipped (No Key): {len(results['skipped'])} ({', '.join(results['skipped'])})")
    print(f"❌ Failed: {len(results['failed'])} ({', '.join(results['failed'])})")
    
    if results['failed']:
        sys.exit(1)

if __name__ == "__main__":
    main()
