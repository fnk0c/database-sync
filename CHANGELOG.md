# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

When a new release is proposed:

1. Create a new branch `bump/x.x.x` (this isn't a long-lived branch!!!);
2. The Unreleased section on `CHANGELOG.md` gets a version number and date;
3. Update the version on `database_sync/__init__.py`;
4. Open a Pull Request with the bump version changes targeting the `main` branch;
5. When the Pull Request is merged, a new `git` tag must be created using [GitHub environment](https://github.com/fnk0c/database-sync/tags).

Releases to productive environments should run from a tagged version.
Exceptions are acceptable depending on the circumstances (critical bug fixes that can be cherry-picked, etc.).

## [Unreleased]

### Changed

- changed CI workflow to use a single `pdm-docker.yaml` call instead of separate `python.yaml` + `python-docker.yaml` jobs, matching the standard pipeline composition pattern

### Added

- added required versions of jinja2 `3.1.6` and cryptography `44.0.1` to avoid vulnerabilities
- added `Makefile` integrating `rios0rios0/pipelines` for standardized `make lint`, `make test`, and `make sast` targets
- added multi-stage `app.Dockerfile` at `.ci/stages/40-delivery/` for Docker delivery with semver tagging
- added full CI pipeline (`python.yaml`) with code checks, security scanning, and tests to the GitHub Actions workflow

### Changed

- updated required Python version from `3.9` to `3.13.12`
- updated safety version from `3.0.1` to `3.5.1` to address vulnerabilities
- updated build backend from deprecated `pdm-pep517` to `pdm-backend`
- renamed `safety-check` script to `safety-scan` to match the pipelines convention
- updated PR templates to reference `make lint`, `make test`, and `make sast` instead of manual `pdm run` commands

### Fixed

- fixed Trivy DS-0026 by adding `HEALTHCHECK` to `app.Dockerfile` and removing the old Dockerfile at `.ci/40-delivery/`
- fixed missing exclude table command for the id_seq of the table ignored
- fixed dropping the id_seq table for the ignored table

### Security

- updated `urllib3` from `2.2.2` to `2.6.3` to fix CVE-2025-50612 and 4 other vulnerabilities
- updated `cryptography` from `45.0.2` to `46.0.5` to fix CVE-2026-26007
- updated `authlib` from `1.3.2` to `1.6.9` to fix CVE-2025-59420, CVE-2025-68158, CVE-2025-61920, and CVE-2025-62706
- updated `requests` from `2.32.3` to `2.32.5` to fix known vulnerability
- updated `setuptools` from `74.0.0` to `82.0.1` to fix path traversal vulnerability
- updated `filelock` from `3.16.1` to `3.19.1` to fix 3 known vulnerabilities
- updated `marshmallow` from `3.22.0` to `4.0.1` to fix known vulnerability
- updated `regex` from `2024.11.6` to `2026.1.15` to fix known vulnerability

### Removed

- removed not used `ignore-vulnerabilities` from safety policy
- removed `export` script from `pyproject.toml` (inlined into `safety-scan`)

## [1.1.0] - 2024-10-01

### Added

- added GitHub pipelines code provided by the pipelines project
- added `.env.example` file to guide new users on the required environment variables for setting up their `.env` file

### Changed

- changed to add `--no-owner` and `--no-acl` options in the `pg_restore` command to avoid restoring ownership and access control lists, resolving errors during database restoration
- upgraded all dependencies to the latest versions

### Fixed

- fixed the password which was not set before executing the `pg_restore` command, by adding `self.__set_pgpassword()` in the `restore` method

## [1.0.0] - 2024-08-20

- Initial release
