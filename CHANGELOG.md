# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automatically create an initialization project based on this project template.
- Conda environment management tasks (`inv conda.*`) for managing Anaconda environments.
- Requirements generation task (`inv build.requirements`) to convert `Pipfile` to `requirements.txt` and `requirements-dev.txt`.

### Changed
- Replaced legacy linters (`flake8`, `isort`, `pydocstyle`, `bandit`) with `ruff` and `black` for faster and modern code style enforcement.
