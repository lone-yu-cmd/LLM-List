---
name: "registry-validator"
description: "Ensures data integrity by running validation tests. Invoke AUTOMATICALLY whenever JSON files in 'registry/' are modified."
---

# Registry Validator

This skill guarantees that all changes to the LLM Registry data are valid, consistent, and linkable before they are finalized.

## When to Use

**Invoke immediately after**:
- Creating a new provider JSON file.
- Modifying an existing provider or schema.
- Editing any JSON file under the `registry/` directory.

## Workflow

1.  **Detect Change**: You have just edited/created a file in `registry/`.
2.  **Execute Validation**:
    -   Run the Schema Format Validator:
        ```bash
        npm run validate:format
        ```
    -   Run the Build Script (to verify merge integrity and reference resolution):
        ```bash
        npm run build
        ```
    -   Run the Data Integrity Test (cross-check source files vs artifact):
        ```bash
        python3 .trae/skills/registry-validator/scripts/test_registry_data.py
        ```
    -   (Optional) Run Connectivity Verification (requires API keys in env):
        ```bash
        python3 .trae/skills/registry-validator/scripts/verify_connectivity.py
        ```
3.  **Analyze Output**:
    -   **Success**: If all commands exit with code 0, the change is valid.
    -   **Failure**: If any command fails, READ the error log.
4.  **Auto-Correction**:
    -   Based on the error log, fix the JSON file immediately.
    -   Repeat Step 2 until success.

## Verification Checklist

When adding a new model/provider, ensure:
1.  `npm run validate:format` passes (Schema has types and formats).
2.  `npm run build` passes (References `$ref` are resolvable).
3.  `test_registry_data.py` passes (All source files are correctly compiled into the artifact).
4.  (Optional) `verify_connectivity.py` passes (Real-world API connection verified).
