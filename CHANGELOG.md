# Changelog
All notable changes to Merlin Spellbook will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.0]

### Added
- Added normal and truncnorm distributions
- COPYRIGHT file for ownership details
- New check for copyright headers in the Makefile

### Changed
- Updated GitHub actions
    - Now uses a version of actions/cache that's not deprecated
    - Utilizes a shared action for jobs to reduce duplicate code
- Copyright headers in all files
  - These now point to the LICENSE and COPYRIGHT files
  - LICENSE: Legal permissions (e.g., MIT terms)
  - COPYRIGHT: Ownership, institutional metadata
  - Make commands that change version/copyright year have been modified

## [0.9.0]

### Added
- Added support for python 3.12 and python 3.13

### Changed
- Dropped support for python 3.7 and older
- Updated Makefile to use newer check-style targets

## [0.8.1]

### Fixed
- style and version number
- testing for make-samples

## [0.8.0]

### Added
- -round and -repeat options to make-samples, which allows for mixed integers and floats

### Changed
- changed python version support to 3.7 - 3.11 (3.6 is past end-of-life)

## [0.7.4]
### Fixed
- `learn.make_regressor` and `learn_alt.random_forest` properly calls `utils.load_infile`.

## [0.7.3]
### Fixed
- `make-barrier-qoi` can accept no constraints.
- `make-barrier-qoi` applies `numpy.atleast_2d` to the qoi before returning.
- `make-barrier-qoi` correctly normalizes inputs from 0 to 1.
- `utils.stack_arrays` returns inputs in correct shape: (# of features, dim of feature).
- `ml.learn` and `ml.learn_alt` use correct `load_infiles` function from `utils`.

## [0.7.2]

### Fixed
- Add missing __init__.py to optimization module.

### Changed
- Remove .keepme file in optimization module.

## [0.7.1]

### Fixed
- Package version

## [0.7.0]

### Added
- function `make-barrier-cost` to create optimization cost functions

## [0.6.1]

### Added
- pylint to dev requirements for format checking

### Changed
- Conduit tests are skipped when conduit python package is not available. (test_conduit.py is also skipped for format checking)
- Rename l variable in setup.py to line.
- Removed unused import libraries.
- Fixed bare "except" statements.
- Created a get_samples function for sample generation in MakeSamples.run to simplify run function.
- Update workflow to always run syntax checkers even if previous syntax heckers fail.
- Reformat code with isort, black and pylint to fit coding standards

## [0.6.0]

### Added
- Delimiter option in serialization command.

### Changed
- In serialize command, grab the first entry as the key and everything else as the value.

## [0.5.3]

### Fixed
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
