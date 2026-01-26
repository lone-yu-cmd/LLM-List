# AI Context: Scripts Directory

> **Note for AI Agents**: This file describes the purpose and usage of the `scripts/` directory.

## Purpose
This directory contains Python automation scripts for building, validating, and crawling data. These scripts are typically invoked via `npm run <script-name>` defined in `package.json`.

## Key Scripts

### `build_registry.py`
*   **Command**: `npm run build`
*   **Function**: Merges `registry/` files into `llm_registry.json`.
*   **Logic**: Resolves `$ref` pointers in JSON files to create a self-contained output.

### `validate_format.py`
*   **Command**: `npm run validate:format`
*   **Function**: Lints JSON Schemas.
*   **Rule**: Enforces that every `type` field in a schema has a corresponding `format` field (OpenAPI style).

### `crawl_api_docs.py` & `scrape_content.py`
*   **Command**: `npm run crawl` / `npm run scrape`
*   **Function**: Web scrapers using Playwright.
*   **Output**: Saves raw Markdown to `docs_dump/`.

## Contribution Rules
*   Use Python 3.10+.
*   Do not hardcode paths; use relative paths from project root.
*   Add type hints to all Python functions.
