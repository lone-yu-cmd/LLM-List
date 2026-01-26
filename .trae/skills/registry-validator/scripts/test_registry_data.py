import json
import os
import sys
import unittest

class TestRegistryData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Locate the root directory and llm_registry.json
        # NOTE: This script is now running from .trae/skills/registry-validator/resources/
        # so root_dir is ../../../../
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cls.root_dir = os.path.abspath(os.path.join(current_dir, '../../../../'))
        cls.registry_path = os.path.join(cls.root_dir, 'llm_registry.json')
        
        if not os.path.exists(cls.registry_path):
            raise FileNotFoundError(f"llm_registry.json not found at {cls.registry_path}. Run build first.")
            
        with open(cls.registry_path, 'r', encoding='utf-8') as f:
            cls.data = json.load(f)
            
        print(f"\nLoaded registry with {len(cls.data.get('providers', []))} providers for validation.")

    def test_structure_basics(self):
        """Validate basic JSON structure."""
        self.assertIn('providers', self.data, "Root 'providers' field missing")
        self.assertIn('version', self.data, "Root 'version' field missing")
        self.assertIsInstance(self.data['providers'], list, "'providers' must be a list")

    def test_critical_providers_exist(self):
        """Ensure all source providers from registry/providers/ are present in the build artifact."""
        # Dynamically find expected providers from source directory
        providers_dir = os.path.join(self.root_dir, 'registry', 'providers')
        if not os.path.exists(providers_dir):
            self.fail(f"Source directory not found: {providers_dir}")
            
        source_providers = set()
        for filename in os.listdir(providers_dir):
            if filename.endswith('.json'):
                source_providers.add(filename[:-5]) # remove .json extension
        
        if not source_providers:
            self.fail("No source provider files found in registry/providers/")

        existing_providers = {p['id'] for p in self.data['providers']}
        
        missing = source_providers - existing_providers
        self.assertEqual(len(missing), 0, f"Missing source providers in artifact: {missing}")
        print(f"✓ All {len(source_providers)} source providers found in artifact.")

    def test_provider_completeness(self):
        """Validate each provider has essential fields."""
        for provider in self.data['providers']:
            pid = provider.get('id', 'unknown')
            with self.subTest(provider=pid):
                self.assertIn('name', provider, f"Provider {pid} missing 'name'")
                self.assertIn('models', provider, f"Provider {pid} missing 'models'")
                self.assertGreater(len(provider['models']), 0, f"Provider {pid} has 0 models")
                
                # Check API config
                if 'api_config' in provider:
                    self.assertIn('base_url', provider['api_config'], f"Provider {pid} missing base_url")

    def test_model_completeness(self):
        """Validate individual models have required fields."""
        for provider in self.data['providers']:
            pid = provider['id']
            for model in provider['models']:
                mid = model.get('id', 'unknown')
                with self.subTest(provider=pid, model=mid):
                    self.assertIn('id', model)
                    self.assertIn('name', model)
                    self.assertIn('type', model)
                    
                    # Check context window if present (it's crucial for LLM list)
                    if 'context_window' in model:
                        self.assertIsInstance(model['context_window'], int, f"Context window for {mid} must be int")
                        self.assertGreater(model['context_window'], 0, f"Context window for {mid} must be positive")

    def test_critical_models_presence(self):
        """Ensure all models defined in source files exist in the build artifact."""
        providers_dir = os.path.join(self.root_dir, 'registry', 'providers')
        
        # Build expected model map from source files
        expected_models_map = {} # {provider_id: {model_id1, model_id2}}
        
        for filename in os.listdir(providers_dir):
            if not filename.endswith('.json'):
                continue
                
            provider_id = filename[:-5]
            file_path = os.path.join(providers_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_data = json.load(f)
                    if 'models' in source_data:
                        expected_models_map[provider_id] = {
                            m['id'] for m in source_data['models'] if 'id' in m
                        }
            except json.JSONDecodeError:
                self.fail(f"Failed to decode source file: {filename}")

        # Verify against build artifact
        for pid, expected_models in expected_models_map.items():
            provider = next((p for p in self.data['providers'] if p['id'] == pid), None)
            
            # Provider existence is checked in test_critical_providers_exist, 
            # but we check here to be safe and specific
            if not provider:
                continue 
                
            artifact_model_ids = {m['id'] for m in provider['models']}
            
            missing_models = expected_models - artifact_model_ids
            self.assertEqual(len(missing_models), 0, 
                             f"Provider {pid} missing models in artifact: {missing_models}")
            
        print(f"✓ Verified models for {len(expected_models_map)} providers against source files.")

    def test_sdk_sync_status(self):
        """Verify that the registry has been synced to SDK directories."""
        sdk_paths = [
            os.path.join(self.root_dir, 'sdks', 'js', 'llm_registry.json'),
            os.path.join(self.root_dir, 'sdks', 'python', 'llm_list', 'llm_registry.json'),
            os.path.join(self.root_dir, 'sdks', 'go', 'llm_registry.json')
        ]
        
        for path in sdk_paths:
            self.assertTrue(os.path.exists(path), f"SDK sync failed: {path} missing")
            
            # Optional: verify content matches
            with open(path, 'r', encoding='utf-8') as f:
                sdk_data = json.load(f)
            self.assertEqual(len(sdk_data['providers']), len(self.data['providers']), 
                             f"SDK data at {path} seems out of sync (provider count mismatch)")
        print("✓ SDK file sync verified.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
