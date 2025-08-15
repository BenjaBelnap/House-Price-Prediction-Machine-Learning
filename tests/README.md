# Tests

This project uses pytest for testing and Poetry for running commands consistently across environments.

## Quick start

- Unit tests only (fast):
  ```powershell
  poetry run poe unit
  ```

- All tests:
  ```powershell
  poetry run poe test
  ```

These tasks are defined under `[tool.poe.tasks]` in `pyproject.toml`.

## Markers and selection

- `@pytest.mark.unit` — fast unit tests for local development.
- `@pytest.mark.slow` — slower/integration tests (optional; add as needed).
- `@pytest.mark.e2e` — end-to-end tests requiring servers (optional).

Select by marker:
```powershell
poetry run pytest -q -m unit
poetry run pytest -q -m "slow or e2e"
poetry run pytest -q -m "not e2e"
```

Filter by name or path:
```powershell
poetry run pytest -q -k preprocessing
poetry run pytest -q tests/unit/test_model_utils.py::test_debug_model_performance_returns_metrics
```

Increase verbosity or show coverage (if `pytest-cov` is added later):
```powershell
poetry run pytest -vv
# poetry add --group dev pytest-cov
# poetry run pytest --cov=src --cov-report=term-missing
```

## Test layout

- `tests/unit/` — pure unit tests (fast).
- `tests/api/` — FastAPI endpoint tests using mocked models.
- `tests/frontend/` — frontend FastAPI server tests.
- `tests/integration/` — optional, heavier tests (not yet added).

Shared fixtures live in `tests/conftest.py` (e.g., FastAPI TestClient, fake models, matplotlib backend).

## Running without Poe

Poe tasks are convenience wrappers. You can always run pytest directly:
```powershell
poetry run pytest -q -m unit
poetry run pytest -q
```

## Troubleshooting

- "No module named 'src'":
  - Ensure the project is installed in the Poetry environment: `poetry install`.
  - Pytest is configured with `pythonpath = ["."]` in `pyproject.toml`.

- Poetry not found:
  - Add Poetry to PATH for the current session (PowerShell):
    ```powershell
    $env:Path += ";$env:APPDATA\Python\Scripts"
    poetry --version
    ```

- Slow tests or network dependencies:
  - Use markers to exclude: `-m "not slow"`.
  - Keep API/frontend tests mocked to avoid external calls.

- Matplotlib warnings in CI/local:
  - The tests force the 'Agg' backend via `conftest.py`; warnings are harmless.

## CI

You can run the same commands in CI. Example GitHub Actions step:
```yaml
- name: Install Poetry
  run: |
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
- name: Install deps
  run: poetry install --no-interaction --no-root
- name: Run tests
  run: poetry run poe unit
```
