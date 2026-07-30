# Setup diagnostics

- Initial scaffold command attempted `pytest -q` and exited `127`: `pytest` was unavailable on PATH.
- Retrying via the workspace virtual environment exited `1`: `.venv/bin/python` has no `pytest` module.
- Recovery: replaced the contract scaffold with a dependency-free `unittest` test so contract validation can run before upstream dependencies are installed.
- No claim experiment was run and no claim status changed.
