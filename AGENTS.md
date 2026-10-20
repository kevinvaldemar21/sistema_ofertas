# AGENTS.md

## Repository status

- This workspace currently contains only `.venv/`; no application source, dependency manifest, documentation, tests, or Git metadata has been established yet.
- Do not infer the project architecture or supported commands from packages installed in `.venv/`.

## Codex workflow

- Before editing, inspect the current tree and identify the concrete entry point, owning module, and nearest test or executable check.
- Preserve existing user changes and keep edits narrowly scoped to the requested behavior.
- When adding application code, add the matching project metadata and a focused test or runnable check in the same change when practical.
- Prefer the repository's documented commands once they exist. Until then, use the workspace virtual environment at `.venv/` for Python checks and record any required command in the project documentation.
- Do not commit generated files, virtual-environment contents, secrets, or local editor state.

## Validation

- Run the narrowest relevant test, type check, lint, or executable smoke check after each implementation change.
- If no automated check exists, state that clearly and perform the cheapest meaningful smoke check available.