# Changelog

All notable changes to the **LLM-List** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- update model connectivity validation and registry

### Changed
- standardize registry structure and complete missing provider data

### Documentation
- update JS SDK installation instructions and convert to ES modules
- Add specifications for Core Registry and DeepSeek integration

### Added
- configure JS SDK for NPM publishing and add CI workflow
- configure NPM publishing for JS SDK
- add SDK verification tests and documentation
- implement registry-syncer skill, auto-generate schema, and migrate SDK data files
- implement comprehensive connectivity and model availability verification
- Implement automated skills README generation and update script
- Add connectivity verification to registry-validator skill
- Add auto-committer skill for automated workflows
- Update Zhipu AI with Embedding-3, Rerank, and other models
- Add DeepSeek provider with V3.2 Chat and Reasoner models

## [0.1.0] - 2026-01-27

### Added
- **Core Registry**: Initial implementation of the provider registry system (`specs/001-core-registry`).
    - Added `registry/` directory structure for providers, schemas, and i18n.
    - Added `scripts/build_registry.py` to compile dispersed JSON files into `llm_registry.json`.
    - Added `scripts/validate_format.py` for JSON Schema validation.
- **SDKs**: Initial scaffold for JS, Python, and Go SDKs in `sdks/`.
- **Docs**: Project constitution and architecture documentation.
- **Tools**: Spec Kit integration for specification-driven development.