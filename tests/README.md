# Tests

- Run only unit tests (fast):

  - marker: `unit`

- Run all tests (including slower):

  - default `pytest -q` runs everything; you can mark slower tests with `@pytest.mark.slow` and select them via `-m slow`.

Markers are defined in `pytest.ini`.
