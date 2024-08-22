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

### Added

- added GitHub pipelines code provided by pipelines project

### Changed

- upgraded all dependencies to the latest versions

### Removed

-

## [1.0.0] - 2024-08-20

- Initial release
