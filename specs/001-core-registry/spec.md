# Feature Specification: Core Registry & Build System

**Feature Branch**: `001-core-registry`
**Created**: 2025-01-27
**Status**: Implemented (Backfilled)
**Input**: User description: "Existing core functionality of LLM-List project including registry data, build scripts, and validation."

## User Scenarios & Testing

### User Story 1 - Provider Data Management (Priority: P1)

As a maintainer, I want to manage LLM provider information in separate, isolated JSON files so that the codebase remains organized and conflicts are minimized.

**Why this priority**: This is the fundamental data source for the entire project.

**Independent Test**: Can be tested by adding a new provider JSON in `registry/providers/` and verifying it exists.

**Acceptance Scenarios**:
1. **Given** a new LLM provider, **When** I create a file in `registry/providers/{id}.json`, **Then** the file is recognized as a valid data source.
2. **Given** an existing provider, **When** I edit their model list, **Then** the changes are isolated to that file.

---

### User Story 2 - Registry Build Process (Priority: P1)

As a maintainer, I want to run a build command to merge all dispersed provider and schema files into a single `llm_registry.json` so that consumers have a single source of truth.

**Why this priority**: Essential for generating the distributable artifact.

**Independent Test**: Run `npm run build` and check if `llm_registry.json` is generated/updated.

**Acceptance Scenarios**:
1. **Given** valid provider and schema files, **When** I run `npm run build`, **Then** a unified `llm_registry.json` is generated in the root.
2. **Given** a schema using `$ref`, **When** I run the build, **Then** the reference is resolved and embedded in the final JSON.

---

### User Story 3 - Data Validation (Priority: P2)

As a maintainer, I want to automatically validate that all schema definitions follow OpenAPI standards (specifically `format` fields) so that generated SDKs are strictly typed.

**Why this priority**: Ensures data quality and SDK compatibility.

**Independent Test**: Run `npm run validate:format`.

**Acceptance Scenarios**:
1. **Given** a schema missing a `format` field for a number/string, **When** I run validation, **Then** the script reports an error.
2. **Given** compliant schemas, **When** I run validation, **Then** it passes silently or with a success message.

---

### User Story 4 - Multi-language SDK Consumption (Priority: P2)

As a developer, I want to use SDKs in JS, Python, or Go that automatically load the registry data so that I can easily integrate LLM capabilities into my app.

**Why this priority**: The primary consumption channel for end-users.

**Independent Test**: Import the SDK in a test project and call `getProviders()`.

**Acceptance Scenarios**:
1. **Given** the JS SDK, **When** I call `getProviders()`, **Then** it returns the list of providers from `llm_registry.json`.
2. **Given** the Python SDK, **When** I call `getProviderModels('openai')`, **Then** it returns the OpenAI model list.

## Requirements

### Functional Requirements

- **FR-001**: System MUST support "Distributed Management" where providers, schemas, and i18n data are stored in separate directories (`registry/`).
- **FR-002**: System MUST support "Centralized Build" via `scripts/build_registry.py` to merge all data.
- **FR-003**: The build process MUST resolve local JSON references (`$ref`).
- **FR-004**: The validation script (`scripts/validate_format.py`) MUST enforce the presence of `format` fields in JSON Schemas.
- **FR-005**: SDKs MUST NOT duplicate the registry data but read from the project root (or bundled path).
- **FR-006**: Provider configuration MUST include `api_config` (base_url, auth, endpoints) and `models` list.

### Key Entities

- **Provider**: Represents an LLM vendor (e.g., OpenAI). Contains ID, API config, and Models.
- **Schema**: Represents an API endpoint definition (Request/Response parameters).
- **Registry**: The aggregated JSON file containing all Providers and Schemas.
