## Development workflow

- This project is typed. Run ty after adding or modifying code:
  - `uv run ty check`
- Use Ruff for formatting and linting:
  - `uv run ruff format .`
  - `uv run ruff check .`
- Run the full test suite after modifying code:
  - `uv run pytest`
- Add or update tests when changing behavior.
- Before committing, run:
  - `uv run pre-commit run`
- Prefer small, focused functions.

## Documentation
- Update documentation when public behavior changes.