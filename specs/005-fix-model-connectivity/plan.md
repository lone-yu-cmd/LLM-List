# Plan: Fix Model Connectivity Issues

## 1. Analysis
The registry stores provider configurations in `registry/providers/<provider_id>.json`. The `models` array within each provider object contains the list of supported models. We need to filter this array to remove the models identified in the spec.

## 2. Technical Approach
- **File Editing**: We will use `SearchReplace` or `Write` (after reading) to update the JSON files. Since JSON structure is strict, reading the whole file, parsing, modifying, and writing back is safer than regex replacement, but `SearchReplace` can work if we are careful with commas. Given the number of deletions (especially for Zhipu), reading and rewriting the whole file might be cleaner, but the tool `SearchReplace` is preferred for diffs. However, for large JSON lists, `SearchReplace` can be tricky.
- **Alternative**: I will read the file, modify it in memory (conceptually), and use `Write` to overwrite the file with the corrected JSON. This ensures validity.

## 3. Files to Modify
- `registry/providers/google.json`
- `registry/providers/openai.json`
- `registry/providers/zhipuai.json`

## 4. Verification
- Run `python3 scripts/build_registry.py` to regenerate `llm_registry.json`.
- Run `python3 .trae/skills/registry-validator/scripts/verify_connectivity.py` to confirm the fix.

## 5. Risks
- Removing a model that *should* be there but was temporarily unavailable.
    - Mitigation: The spec is based on a connectivity check. If it's missing in remote, we can't guarantee it works, so removing it is the correct action for now.
- JSON syntax errors during editing.
    - Mitigation: Use `Write` with full content or carefully constructed `SearchReplace`. I will use `Write` for safety.

