# Tasks: Core Registry & Build System

**Input**: Design documents from `/specs/001-core-registry/`
**Prerequisites**: plan.md (required), spec.md (required)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (registry, scripts, sdks)
- [x] T002 Initialize `package.json` with build/validate commands
- [x] T003 [P] Create `.gitignore` and `README.md`

---

## Phase 2: Foundational Data (User Story 1)

**Goal**: Establish the initial data source structure for providers and schemas.

- [x] T004 [US1] Create `registry/providers/openai.json` as sample provider
- [x] T005 [US1] Create `registry/providers/zhipuai.json` as sample provider
- [x] T006 [P] [US1] Create `registry/schemas/openai/endpoints/chat_completions.json`
- [x] T007 [P] [US1] Create `registry/i18n/openai/en.json` and `zh.json`

---

## Phase 3: Build System (User Story 2) 🎯 MVP

**Goal**: Merge dispersed JSON files into a single `llm_registry.json`.

**Independent Test**: `npm run build` generates valid JSON.

- [x] T008 [US2] Implement provider loader in `scripts/build_registry.py`
- [x] T009 [US2] Implement `$ref` resolution logic in `scripts/build_registry.py`
- [x] T010 [US2] Implement merge and write logic in `scripts/build_registry.py`
- [x] T011 [US2] Verify build output matches expected structure

---

## Phase 4: Validation System (User Story 3)

**Goal**: Ensure data integrity and schema compliance.

**Independent Test**: `npm run validate:format`.

- [x] T012 [US3] Implement `scripts/validate_format.py` walker
- [x] T013 [US3] Add logic to check for missing `format` fields in schemas
- [x] T014 [US3] Add validation script to `package.json` scripts

---

## Phase 5: SDK Implementation (User Story 4)

**Goal**: Provide consumption libraries for developers.

**Independent Test**: Unit tests in each SDK directory.

- [x] T015 [P] [US4] Implement JS SDK in `sdks/js/` (index.js, package.json)
- [x] T016 [P] [US4] Implement Python SDK in `sdks/python/` (setup.py, __init__.py)
- [x] T017 [P] [US4] Implement Go SDK in `sdks/go/` (registry.go, go.mod)

---

## Phase 6: Automation & Tools (Crawlers)

**Goal**: Automate data gathering.

- [x] T018 [P] Implement `scripts/crawl_api_docs.py`
- [x] T019 [P] Implement `scripts/scrape_content.py` using Playwright
