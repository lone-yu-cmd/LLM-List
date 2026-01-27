# Plan: Publish JS SDK to NPM

## 1. Package Configuration
We need to enhance `sdks/js/package.json` and add `.npmignore`.

### `package.json` Updates
- `repository`: Point to the GitHub repo directory.
- `publishConfig`: Set registry (default npm).
- `files`: Explicitly whitelist files (optional, or rely on `.npmignore`).
- `description`, `keywords`: Enhance for SEO.

### `.npmignore`
Exclude:
- `test/`
- `.gitignore`
- `node_modules/` (default)

## 2. GitHub Action
Create `.github/workflows/publish-js.yml`.
- Trigger: `release` created or manual dispatch.
- Steps:
  - Checkout code.
  - Setup Node.js.
  - `npm install`.
  - `npm publish`.
- Secrets: `NPM_TOKEN`.

## 3. Directory Structure
```
sdks/js/
  ├── package.json
  ├── .npmignore
  ├── index.js
  ├── README.md (Copy from root or create specific)
  ├── data/
  └── schema/
```

## 4. Execution Steps
1.  Modify `sdks/js/package.json`.
2.  Create `sdks/js/.npmignore`.
3.  Create `sdks/js/README.md` (Symlink or Copy content from root SDK usage section).
4.  Create `.github/workflows/publish-js.yml`.
