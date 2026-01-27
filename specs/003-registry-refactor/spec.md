# Specification: Registry Refactor and Completion

## 1. Background
The `registry/` directory is the core data source for LLMList. Currently, `zhipuai.json` serves as the gold standard for data completeness and structure. Other providers (OpenAI, DeepSeek, etc.) are missing key information such as error codes, pricing currency, and detailed model specifications (context window, output tokens).

## 2. Goals
1.  **Standardize Structure**: Ensure the `registry/` directory follows a consistent layout as defined in `AI_README.md` and `zhipuai.json`.
2.  **Complete Data**: Bring all provider JSONs up to parity with `zhipuai.json` by adding missing fields (`error_codes`, `pricing_currency`, `context_window`, `max_output_tokens`).
3.  **Verify Integrity**: Ensure all references (e.g., schemas) are valid and present.

## 3. User Scenarios
-   **Scenario 1**: A developer looks up `openai.json` and finds the same level of detail (error codes, limits) as `zhipuai.json`.
-   **Scenario 2**: The build script runs and generates a uniform `llm_registry.json` without missing fields for any provider.

## 4. Functional Requirements
-   **FR1**: Update `registry/providers/*.json` to include `pricing_currency` (if applicable) and `api_config.error_codes`.
-   **FR2**: Update `registry/providers/*.json` models list to include `context_window` and `max_output_tokens` for all models.
-   **FR3**: Ensure `registry/schemas/{provider}/` exists for all providers if they use `$ref` in their config.
-   **FR4**: Ensure `registry/i18n/{provider}/` exists if applicable (or at least establish a pattern).

## 5. Success Criteria
-   All provider JSON files contain `error_codes` and `pricing_currency` (where public).
-   All models in provider files have `context_window` and `max_output_tokens` defined.
-   `registry-validator` passes (if available/updated).
