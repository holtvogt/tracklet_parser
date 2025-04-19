# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2025-04-19

### Added

- Published the package on [PyPI](https://pypi.org/project/tracklet-parser/), making it available for installation via `pip`.
- Enhanced unit tests for `TrackletParser`:
  - Added tests for edge cases, such as empty XML files and invalid XML structures.
  - Added tests for missing frame lists and empty tracklet lists.
- Integrated `TemporaryDirectory` for test isolation and automatic cleanup.

### Changed

- Improved test structure for better readability and maintainability:
  - Extracted helper methods for creating temporary files.
  - Simplified test setup and teardown using `TemporaryDirectory`.
- Restructured the project to a flat layout for better organization.
- Updated the `.pre-commit-config.yaml`:
  - Bumped all hooks to their new versions
  - Replaced `docformatter` configuration as it is currently broken
- Updated `README.md`:
  - Improved the usage example with better comments and structure.
  - Added a "Testing" section to explain how to run tests.
  - Added a "Contributing" section with clear contribution guidelines.
- Changed required Python version to `3.12`

---

## [1.0.1] - 2024-01-14

### Added

- Introduced `pyproject.toml` as the build system configuration file.

### Changed

- Migrated the project structure to a `src` layout for better modularity.
- Updated pre-commit hook versions to ensure compatibility with the latest tools.
- Revised installation instructions in `README.md` for clarity.

### Removed

- Deprecated `setup.py` in favor of `pyproject.toml` as per [PEP 517](https://peps.python.org/pep-0517/).

---

## [1.0.0] - 2022-08-14

### Added

- Initial version.
