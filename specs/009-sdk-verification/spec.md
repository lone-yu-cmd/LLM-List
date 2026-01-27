# Spec: SDK Verification

## 1. Background
Currently, the `registry-syncer` skill distributes the LLM Registry JSON and Schema to all SDKs (JS, Python, Go). However, there is no verification step to ensure that the generated SDKs can actually read and parse these files correctly.

## 2. Goals
- Create test files for each SDK to verify they can load the registry data.
- Update `registry-syncer` to automatically run these tests after synchronization.
- Ensure that if the registry data is invalid or incompatible with the SDK code, the sync process (or post-sync validation) flags the error.

## 3. User Stories
- **As a developer**, when I run `registry-syncer`, I want to know immediately if the new data breaks any SDK.
- **As a maintainer**, I want to ensure that the SDK code is always compatible with the latest data format.

## 4. Functional Requirements
1.  **JS SDK Test**: Create a test script (e.g., `test.js` or using a runner) that imports the package and calls `getProviders()`, verifying the result is not empty.
2.  **Python SDK Test**: Create a test script (e.g., `test_registry.py`) that imports `llm_list` and verifies data loading.
3.  **Go SDK Test**: Create a Go test (e.g., `registry_test.go`) that calls `LoadRegistry()` and verifies no errors.
4.  **Integration**: The `registry-syncer` skill (specifically `scripts/build_registry.py`) must invoke these tests after distribution.

## 5. Success Criteria
- All 3 SDKs have a runnable test file.
- Running `registry-syncer` triggers these tests.
- If a test fails, the process reports the failure.
