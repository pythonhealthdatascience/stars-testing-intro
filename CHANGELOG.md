# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates formatted as YYYY-MM-DD as per [ISO standard](https://www.iso.org/iso-8601-date-and-time-format.html).

## v0.2.0 - 2026-11-11

Finalised version of website, accompanying release of videos on HDR UK Futures in November 2026.

### Added

* New pages on:
    * Smoke tests.
    * Defensive programming.
    * Data, temporary files and mocking.
* Example defensive programming versions of `calculate_wait_times()` added to `pages/code/`.
* Add videos of breaking code and tests failing in `break.qmd`.
* Add notebooks and Rmd files used when filming videos.
* Add spellcheck GitHub action.

### Changed

* Renamed repository and environments
* Removed HDR UK Futures logo and favicon.
* Add link to Zenodo on README.
* Rename "back/functional" to "regression/system".
* Improve appearance of tables.
* Add link to live course on HDR UK Futures.

### Fixed

* Capture parametrise in snippets.
* Fixes to GitHub actions and environments.

## v0.1.0 - 2026-01-20

🌱 Initial release of the website.

### Added

* Website with pages:
    * Homepage
    * When and why to run tests
    * Case study
    * How to write a basic test
    * How to run tests
    * Parametrising tests
    * Unit tests
    * Functional tests
    * Back tests
    * What was the point? Let's break it and see!
    * Test coverage
    * Running tests via GitHub actions
    * Example repositories
* Python and R environments for the site.
* GitHub actions to create docker, render and deploy site, and run python and R tests.
* Example python and R code used within website in `examples/`.
* Other research artefacts (e.g., `tools/`, `CONTRIBUTING.md`, `README.md`).