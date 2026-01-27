# Specification: API Connectivity & Model Validation

## 1. Background
The project maintains a registry of LLM providers (`registry/providers/*.json`). Currently, we verify basic provider connectivity (e.g., listing models). However, we need to go further and verify that **every specific model** listed in our registry is actually accessible and valid for the given provider.

## 2. Goals
1.  **Environment Management**: Standardize how API keys are managed using `.env` and `.env.example`.
2.  **Connectivity Testing**: Implement a script to test authentication and basic endpoint reachability for all defined providers.
3.  **Model Validation**: Iterate through every model ID defined in the registry and verify its existence/availability via the provider's API.

## 3. User Scenarios
-   **Scenario 1**: A new developer clones the repo. They copy `.env.example` to `.env`, fill in their API keys, and run the verification script to confirm their setup works.
-   **Scenario 2**: A maintainer adds a new model to `openai.json`. They run the script to ensure the model ID is correct and accessible before merging.

## 4. Functional Requirements
-   **FR1**: Create `.env.example` containing placeholder variables for all supported providers.
-   **FR2**: Update `.gitignore` to ensure `.env` is never committed.
-   **FR3**: Enhance `verify_connectivity.py` to:
    -   Load environment variables from `.env`.
    -   Iterate through all providers in `llm_registry.json`.
    -   **Step A**: Send a test request (e.g., list models) to verify provider configuration.
    -   **Step B**: For each model defined in `provider.models`, check if it exists in the provider's returned model list.
    -   Report detailed pass/fail status for each model.

## 5. Success Criteria
-   Verification script reports status for EVERY model defined in the registry.
-   If a model is defined in JSON but not returned by the API, it should be flagged as a warning or error.
