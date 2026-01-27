---
name: "registry-syncer"
description: "Regenerates JSON Schema, rebuilds the LLM registry from source, and syncs both to all SDKs. Invoke when user updates registry, schema, or asks to sync/build."
---

# Registry Syncer

This skill manages the synchronization of the central LLM registry and its Schema to all supported SDKs.

## Purpose
To ensure that:
1.  The JSON Schema is regenerated from Python Pydantic models (`scripts/generate_schema.py`).
2.  Changes in `registry/providers/*.json` are aggregated into `llm_registry.json`.
3.  Both the Registry JSON and the Schema JSON are distributed to:
    - `sdks/go/`
    - `sdks/js/`
    - `sdks/python/`

## Instructions

When this skill is invoked:

1.  **Execute Build Script**:
    Run the following command, which now handles schema generation AND registry distribution:
    ```bash
    python3 scripts/build_registry.py
    ```

2.  **Verify Output**:
    -   Check for "Generating updated JSON Schema...".
    -   Check for "Successfully generated llm_registry.json".
    -   Confirm it reports syncing **registry and schema** to all 3 SDKs.

3.  **Optional Validation**:
    -   If the build fails, analyze the error (JSON syntax errors are common).
    -   You may invoke the `registry-validator` skill to perform a deep validation if the build script error is unclear.

## Example Usage

User: "I added a new model, please sync."
Agent: Invokes `registry-syncer`.
