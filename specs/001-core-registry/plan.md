# Implementation Plan: Core Registry & Build System

**Branch**: `001-core-registry` | **Date**: 2026-01-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-core-registry/spec.md`

## Summary

This plan documents the existing architecture of the LLM-List project, which centers around a JSON-based registry of LLM providers. The system uses a "Distributed Management, Centralized Build" pattern where source data is split into multiple files for maintainability but compiled into a single artifact for consumption.

## Technical Context

**Language/Version**: 
- **Scripts**: Python 3.10+ (for build/validation/scraping)
- **Data**: JSON Standard (RFC 8259), JSON Schema Draft 7
- **SDKs**: Node.js 16+, Go 1.21+, Python 3.9+

**Primary Dependencies**: 
- **Python**: `jsonschema` (validation), `playwright` (scraping), `requests`
- **Node**: `axios` (or native fetch) for SDK
- **Go**: Standard library `encoding/json`

**Storage**: File-based (Git). No external database required for the core registry.
**Testing**: 
- **Validation**: `scripts/validate_format.py` acts as a linting test.
- **SDKs**: Language-specific unit tests (e.g., `pytest`, `go test`, `npm test`).

**Project Type**: Monorepo (Data + Scripts + SDKs)
**Constraints**: 
- `llm_registry.json` must be self-contained (no external refs).
- Schema validation must enforce `format` for code generation compatibility.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Library-First**: Satisfied. The core product is a data library/SDK.
- **CLI Interface**: Satisfied. Build and validation are exposed via CLI scripts.
- **Test-First**: Partially Satisfied. Validation scripts serve as regression tests for data integrity.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-registry/
├── plan.md              # This file
├── spec.md              # Feature specification
└── tasks.md             # Implementation tasks status
```

### Source Code (repository root)

```text
LLM-List/
├── llm_registry.json          # Build Artifact
├── registry/                  # Data Source
│   ├── providers/             # {id}.json
│   ├── schemas/               # {provider_id}/endpoints/{name}.json
│   └── i18n/                  # {provider_id}/{lang}.json
├── scripts/                   # Automation
│   ├── build_registry.py      # Core Builder
│   ├── validate_format.py     # Validator
│   ├── crawl_api_docs.py      # Crawler
│   └── scrape_content.py      # Scraper
├── sdks/                      # Consumer Libraries
│   ├── js/
│   ├── go/
│   └── python/
└── package.json               # Task Runner
```

**Structure Decision**: The Monorepo structure is chosen to keep data and tools together, ensuring that changes to the schema can be immediately validated against the build scripts and SDKs.

## Implementation Details

### Build Process (`build_registry.py`)
1.  **Iterate** `registry/providers/*.json`.
2.  **Load** each provider config.
3.  **Resolve** `$ref` in `api_config.endpoints`.
    -   Read the referenced schema file.
    -   Inject it into the provider object.
4.  **Merge** into a master dictionary `{ "providers": [...] }`.
5.  **Write** to `llm_registry.json`.

### Validation Process (`validate_format.py`)
1.  **Walk** through `registry/schemas/`.
2.  **Parse** every JSON file.
3.  **Recursively** check every object for `type` fields.
4.  **Assert** that if `type` is present (and simple), `format` is also present or explicitly not required.
5.  **Exit** with non-zero code if violations found.

### SDK Design
-   **Stateless**: SDKs are thin wrappers around the JSON data.
-   **Lazy Loading**: Data is loaded on initialization or first access.
-   **Typed**: Where possible, types are generated or defined to match the JSON Schema.
