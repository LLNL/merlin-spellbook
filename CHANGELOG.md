# Changelog
All notable changes to Merlin Spellbook will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.1]

## Changed
- Conduit tests are skipped when conduit python package is not available.
- Rename l variable in setup to line.
- Removed unused import libraries.
- Fixed bare "except" statements.
- Created a get_samples function for sample generation in MakeSamples.run.
- Update workflow to always run syntax checkers.

## [0.6.0]

## Added
- Delimiter option in serialization command.

## Changed
- In serialize command, grab the first entry as the key and everything else as the value.

## [0.5.3]

## Fixed
- version number in docs and setup.py to match 0.5.3

## [0.5.2]

### Fixed
- auto-deploy by adding a MANIFEST.in and changing to python -m build for release

## [0.5.1]

### Added
- prototype github actions for testing and auto-deploy

### Fixed
- `conduit-collect` incompatibility with recent versions of click
- Copyright year to 2022

## [0.5.0]

### Added
- Ability for `conduit-translate` to deal with chunks from `conduit-collect`.
- Ansynchronous parallelism for `conduit-translate -chunks -n <n processes>`.

### Fixed
- Help message for `-chunk_size` in `conduit-collect`. Previously was ambiguous,
  saying `-chunk_size` corresponded to number of files, instead of size of files.
- Typo in `make-samples` help message.
- Error in serializing booleans
- Bug in serializer and error in serialize testing

## [0.4.3]

### Fixed
- Allowed for pyDOE2 sampling functions to use seeds.
- Bug in `spellbook learn` that excluded the `-regressor` flag.

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
