import json
import os
import pkg_resources

class LLMRegistry:
    def __init__(self, data=None):
        if data:
            self.registry = data
        else:
            self.registry = self._load_registry()

    def _load_registry(self):
        """
        Load the LLM registry data.
        """
        try:
            # Try loading from package data first
            data_path = pkg_resources.resource_filename('llm_list', 'data/llm_registry.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            # Fallback to local file if not installed as package
            current_dir = os.path.dirname(__file__)
            local_path = os.path.join(current_dir, 'data', 'llm_registry.json')
            if os.path.exists(local_path):
                with open(local_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            # Return empty structure if not found
            return {"providers": []}

    def get_providers(self):
        """Get all providers."""
        return self.registry.get('providers', [])

    def get_provider(self, provider_id):
        """Get a provider by ID."""
        for provider in self.get_providers():
            if provider.get('id') == provider_id:
                return provider
        return None

    def get_models(self, provider_id):
        """Get all models for a specific provider."""
        provider = self.get_provider(provider_id)
        if provider:
            return provider.get('models', [])
        return []

    def get_model(self, provider_id, model_id):
        """Get a specific model by ID from a provider."""
        models = self.get_models(provider_id)
        for model in models:
            if model.get('id') == model_id:
                return model
        return None

    def get_all_chat_models(self):
        """Get all chat models across all providers."""
        all_models = []
        for provider in self.get_providers():
            provider_id = provider.get('id')
            provider_name = provider.get('name')
            for model in provider.get('models', []):
                if model.get('type') == 'chat':
                    # Create a copy to avoid modifying the original registry
                    model_copy = model.copy()
                    model_copy['provider_id'] = provider_id
                    model_copy['provider_name'] = provider_name
                    all_models.append(model_copy)
        return all_models

# Create a default instance
_default_registry = LLMRegistry()

# Expose methods from the default instance for easy access
get_providers = _default_registry.get_providers
get_provider = _default_registry.get_provider
get_models = _default_registry.get_models
get_model = _default_registry.get_model
get_all_chat_models = _default_registry.get_all_chat_models
