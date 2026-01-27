# Plan: Registry Refactor and Completion

## 1. Directory Structure Refactor
-   [ ] Create `registry/schemas/anthropic/endpoints/`
-   [ ] Create `registry/schemas/google/endpoints/`
-   [ ] Create `registry/schemas/deepseek/endpoints/`
-   [ ] Create `registry/i18n/anthropic/`
-   [ ] Create `registry/i18n/google/`
-   [ ] Create `registry/i18n/deepseek/`

## 2. Data Analysis & Completion
-   [ ] **OpenAI**:
    -   Missing: `context_window`, `max_output_tokens`, `pricing_currency`, `error_codes`.
    -   Action: Search for "GPT-5 specs" or infer from `description`. Since date is 2026, I will attempt to use `scripts/crawl_api_docs.py` if available, or fall back to reasonable estimates for "future" models if search fails.
-   [ ] **Anthropic**:
    -   Missing: `pricing_currency`, `error_codes`.
    -   Action: Add standard Anthropic error codes (400, 401, 429, 500, 529). Add `USD`.
-   [ ] **Google**:
    -   Missing: `pricing_currency`, `error_codes`.
    -   Action: Add standard Google error codes (400, 403, 429, 500, 503). Add `USD`.
-   [ ] **DeepSeek**:
    -   Missing: `pricing_currency`, `error_codes`.
    -   Action: Add `CNY` (or USD). Add standard DeepSeek error codes.

## 3. Implementation Steps
1.  **Script Execution**: Try to run `python3 scripts/crawl_api_docs.py` to see if it works/helps.
2.  **Manual Updates**: Edit each JSON file to add missing fields.
3.  **Validation**: Run `npm run validate:format` (if available) or `python3 scripts/validate_format.py`.

## 4. Verification
-   Check all JSON files for `error_codes`, `pricing_currency`, and model details.
