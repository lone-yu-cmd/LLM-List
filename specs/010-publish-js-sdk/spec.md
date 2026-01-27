# Spec: Publish JS SDK to NPM

## 1. Background
The JS SDK is currently only available via Git or local file installation. To make it easier for Node.js developers to use, we want to publish it to the NPM registry.

## 2. Goals
- Configure `sdks/js` for NPM publication.
- Automate the publishing process using GitHub Actions.
- Ensure only necessary files are included in the package.

## 3. User Stories
- **As a JS developer**, I want to install the library via `npm install llm-list` (or scoped name) so I can easily manage versions.
- **As a maintainer**, I want the package to be automatically published when a new release is created.

## 4. Functional Requirements
1.  **Package Metadata**: Update `package.json` with correct repository links, homepage, and publish configuration.
2.  **File Inclusion**: Use `.npmignore` to exclude tests, CI configs, and other non-essential files. Only `index.js`, `data/`, `schema/`, and `README` should be included.
3.  **Automation**: Create a GitHub Action workflow that triggers on release tags to publish to NPM.
4.  **Package Name**: Use `llm-list` if available, or `@llm-list/core` / `llm-list-registry`. *Decision*: We will stick with `llm-list` for now, assuming the user has rights or will change it if taken.

## 5. Success Criteria
- `npm pack` in `sdks/js` produces a clean tarball with only necessary files.
- GitHub Action file exists and is configured correctly.
