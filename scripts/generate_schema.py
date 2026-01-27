import json
import os
from datetime import date
from typing import List, Dict, Optional, Any, Union
try:
    from pydantic import BaseModel, Field, HttpUrl, EmailStr
except ImportError:
    print("Pydantic is not installed. Please install it with: pip install pydantic")
    exit(1)

# Define Pydantic models for the registry

class AuthConfig(BaseModel):
    type: str = Field(..., description="Authentication type (e.g., api_key)")
    header_key: Optional[str] = Field(None, description="Header key for the token")
    token_prefix: Optional[str] = Field(None, description="Prefix for the token (e.g., Bearer)")
    env_var_suggestion: Optional[str] = Field(None, description="Suggested environment variable name")

class EndpointConfig(BaseModel):
    path: str = Field(..., description="API endpoint path")
    method: str = Field(..., description="HTTP method")
    supports_stream: Optional[bool] = Field(False, description="Whether streaming is supported")

class ErrorCode(BaseModel):
    code: str = Field(..., description="HTTP status code or error code")
    description: str = Field(..., description="Description of the error")

class ApiConfig(BaseModel):
    protocol: str = Field(..., description="API protocol (e.g., rest)")
    protocol_format: Optional[str] = Field(None, description="Format style (e.g., openai, anthropic)")
    base_url: str = Field(..., description="Base URL for the API")
    auth: AuthConfig = Field(..., description="Authentication configuration")
    endpoints: Optional[Dict[str, EndpointConfig]] = Field(None, description="Key endpoints definition")
    error_codes: Optional[List[ErrorCode]] = Field(None, description="Common error codes")

class Pricing(BaseModel):
    input: Optional[float] = Field(None, description="Cost per 1M input tokens")
    output: Optional[float] = Field(None, description="Cost per 1M output tokens")

class Model(BaseModel):
    id: str = Field(..., description="Unique model identifier")
    name: str = Field(..., description="Display name of the model")
    type: str = Field(..., description="Model type (chat, embedding, video, etc.)")
    description: Optional[str] = Field(None, description="Brief description of the model")
    features: Optional[List[str]] = Field(None, description="List of supported features")
    context_window: Optional[int] = Field(None, description="Maximum context window size")
    max_output_tokens: Optional[int] = Field(None, description="Maximum output tokens")
    pricing: Optional[Pricing] = Field(None, description="Pricing information")

class Provider(BaseModel):
    id: str = Field(..., description="Unique provider identifier")
    name: str = Field(..., description="Display name of the provider")
    description: Optional[str] = Field(None, description="Description of the provider")
    website: Optional[str] = Field(None, description="Provider website URL")
    docs_url: Optional[str] = Field(None, description="Documentation URL")
    api_config: ApiConfig = Field(..., description="API connection configuration")
    pricing_currency: Optional[str] = Field("USD", description="Currency for pricing")
    models: List[Model] = Field(..., description="List of supported models")

class LLMRegistry(BaseModel):
    schema_: str = Field(..., alias="$schema", description="Path to the JSON schema")
    version: str = Field(..., description="Registry version")
    updated_at: str = Field(..., description="Last update date (YYYY-MM-DD)")
    description: str = Field(..., description="Registry description")
    providers: List[Provider] = Field(..., description="List of LLM providers")

def generate_schema():
    # Generate JSON Schema
    schema = LLMRegistry.model_json_schema()
    
    # Define output path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(root_dir, 'schema', 'llm_registry_schema.json')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(schema_path), exist_ok=True)
    
    # Write to file
    with open(schema_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    
    print(f"Successfully generated JSON Schema at: {schema_path}")

if __name__ == "__main__":
    generate_schema()
