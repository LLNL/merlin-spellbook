# Changelog
All notable changes to Merlin Spellbook will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2]

### Fixed
- A conduit loading bug.

## [0.4.1]

### Added
- CLI test for `spellbook serialize`.
- CLI test for `spellbook make-samples`.
- Conduit bundler unit tests.

### Fixed
- A variety of bugs in `conduit-collect` and `conduit-translate`.

## [0.4.0]

### Added
- The new spellbook command `spellbook serialize`.
- The new spellbook command `spellbook conduit-collect`.
- The new spellbook command `spellbook conduit-translate`.

### Changed
- For better organization and speed, moved internal cli logic from `argparse` to `click`.

## [0.3.0]

### Added
- Central composite sampling in `make-samples`.

## [0.2.1]

### Fixed
- Bug that made make-samples break for single values of x0

## [0.2.0]

### Added
- Ability for `spellbook make_samples` to take multiple values in x0.
- Chunking logic for `spellbook collect`.
- Padding feature that allows `spellbook stack-npz` to handle variable-length arrays.

### Fixed
- Bug that caused `stack-npz` to break when given only 1 source file.

## [0.1.0]

### Added
- Command line functionality for all spellbook scripts
