# AI Context: Registry Directory

> **Note for AI Agents**: This file describes the purpose and structure of the `registry/` directory. Read this to understand how to add or modify LLM provider data.

## Purpose
The `registry/` directory is the **Single Source of Truth** for all LLM provider data. It contains raw, dispersed JSON files that are compiled into the final `llm_registry.json` artifact.

## Structure

*   **`providers/`**: Contains one JSON file per LLM provider (e.g., `openai.json`).
    *   **Rule**: Do NOT put all providers in one file. Each provider must be isolated.
    *   **Rule**: Use the provider's unique ID as the filename.
*   **`schemas/`**: Contains JSON Schema definitions for API endpoints.
    *   **Rule**: Organized by `{provider_id}/endpoints/{endpoint_name}.json`.
    *   **Rule**: Schemas MUST include `type` and `format` fields for SDK generation.
*   **`i18n/`**: Contains error code translations.
    *   **Rule**: Organized by `{provider_id}/{lang}.json`.

## Common Tasks

### Adding a New Provider
1.  Create `registry/providers/{new_id}.json`.
2.  Define `api_config` and `models`.
3.  Add referenced schemas in `registry/schemas/{new_id}/`.

### Modifying an Endpoint
1.  Locate the schema in `registry/schemas/{provider_id}/endpoints/`.
2.  Edit the `request_parameters` or `response_parameters`.
3.  Run `npm run validate:format` to ensure correctness.
