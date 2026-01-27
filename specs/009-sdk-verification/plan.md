# Plan: SDK Verification

## 1. Technical Approach
We will implement lightweight "smoke tests" for each SDK. These tests will focus on the critical path: loading the registry JSON and parsing it into the SDK's native structures.

## 2. Test Implementation
- **JS**: `sdks/js/test/verify.js` using standard `node:assert`. Update `package.json` scripts.
- **Python**: `sdks/python/tests/test_verify.py` using `unittest`.
- **Go**: `sdks/go/registry_test.go` using standard `testing` package.

## 3. Automation Logic
We will modify `scripts/build_registry.py` to include a verification step at the end.
- After syncing files, the script will execute the test command for each SDK.
- If any test fails, the script should output a warning or error.

## 4. Verification Steps
1.  **JS**: Run `npm test` inside `sdks/js`.
2.  **Python**: Run `python3 -m unittest discover tests` inside `sdks/python`.
3.  **Go**: Run `go test ./...` inside `sdks/go`.

## 5. Updates to Skill
- The `registry-syncer` SKILL.md does not strictly *need* updates if `build_registry.py` handles the logic, but we should update the description to reflect that verification is now part of the process.
