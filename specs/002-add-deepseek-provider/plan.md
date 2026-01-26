# Implementation Plan: Add DeepSeek Provider

**Spec**: [spec.md](./spec.md)
**Status**: Draft

## Technical Approach

We will add a new JSON file to the `registry/providers/` directory following the standard schema. DeepSeek's API is OpenAI-compatible, so the `api_config` will use `protocol_format: "openai"`.

### Architecture Changes

- **Registry**: Add `registry/providers/deepseek.json`.
- **Build System**: No code changes needed, just execution of existing scripts.

### Data Models

**New Provider: DeepSeek**
```json
{
  "id": "deepseek",
  "name": "DeepSeek",
  "api_config": {
    "base_url": "https://api.deepseek.com",
    "protocol_format": "openai"
    ...
  },
  "models": [
    { "id": "deepseek-chat", ... },
    { "id": "deepseek-reasoner", ... }
  ]
}
```

## Implementation Steps

1.  **Create Provider File**: Create `registry/providers/deepseek.json` with metadata and model definitions.
2.  **Validation**: Run schema validation script.
3.  **Build**: Run registry build script.
4.  **Verification**: Run integrity tests.

## Verification Plan

### Automated Tests
- `npm run validate:format`: Ensures JSON schema compliance.
- `npm run build`: Ensures references are resolved.
- `python3 .trae/skills/registry-validator/scripts/test_registry_data.py`: Ensures data integrity.

### Manual Verification
- Inspect `llm_registry.json` to confirm DeepSeek presence.
