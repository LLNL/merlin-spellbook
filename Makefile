
VER?=1.0.0
VSTRING=[0-9]\+\.[0-9]\+\.[0-9]\+
PYTHON?=python3
PY_TARGET_VER?=py311  # At the time this is added (2/19/25) black only supports up to py311
FROM?=Unreleased

PROJ=spellbook
TEST=tests

# check setup.cfg exists
ifeq (,$(wildcard setup.cfg))
	MAX_LINE_LENGTH=127
else
	MAX_LINE_LENGTH=$(shell grep 'max-line-length' setup.cfg | cut -d ' ' -f3)
endif

unit-tests:
	python3 -m pytest $(TEST)/

command-line-tests:
	python3 $(TEST)/command_line_tests.py

tests: unit-tests command-line-tests

release:
	python3 -m build .

# Increment the Spellbook version. USE ONLY ON DEVELOP BEFORE MERGING TO MASTER.
# Usage: make version VER=1.13.0 FROM=1.13.0-beta
#        (defaults to FROM=Unreleased if not set)
version:
	@echo "Updating Spellbook version from [$(FROM)] to [$(VER)]..."
	sed -i 's/__version__ = "\(.*\)"/__version__ = "$(VER)"/' spellbook/__init__.py
	@if grep -q "## \[$(FROM)\]" CHANGELOG.md; then \
		sed -i 's/## \[$(FROM)\]/## [$(VER)]/' CHANGELOG.md; \
	else \
		echo "⚠️  No matching '## [$(FROM)]' found in CHANGELOG.md"; \
	fi

# Increment copyright year = Usage: make year YEAR=2026
year:
	@echo "Updating COPYRIGHT file to year $(YEAR)..."
	sed -i -E 's/(Copyright \(c\) 2019–)[0-9]{4}( Lawrence Livermore National Laboratory)/\1$(YEAR)\2/' COPYRIGHT

clean:
	-find $(PROJ) -name "*.py[cod]" -exec rm -f {} \;
	-find $(PROJ) -name "__pycache__" -type d -exec rm -rf {} \;
	-rm -rf dist
	-rm -rf build

fix-style:
	python3 -m isort --line-length $(MAX_LINE_LENGTH) $(PROJ)
	python3 -m isort --line-length $(MAX_LINE_LENGTH) $(TEST)
	python3 -m isort --line-length $(MAX_LINE_LENGTH) *.py
	python3 -m black --line-length $(MAX_LINE_LENGTH) --target-version $(PY_TARGET_VER) $(PROJ)
	python3 -m black --line-length $(MAX_LINE_LENGTH) --target-version $(PY_TARGET_VER) $(TEST)
	python3 -m black --line-length $(MAX_LINE_LENGTH) --target-version $(PY_TARGET_VER) *.py


check-flake8:
	echo "Flake8 linting for invalid source (bad syntax, undefined variables)..."; \
	$(PYTHON) -m flake8 --count --select=E9,F63,F7,F82 --show-source --statistics; \
	echo "Flake8 linting failure for CI..."; \
	$(PYTHON) -m flake8 . --count --max-complexity=15 --statistics --max-line-length=127; \


check-black:
	$(PYTHON) -m black --check --line-length $(MAX_LINE_LENGTH) --target-version $(PY_TARGET_VER) $(PROJ); \
	$(PYTHON) -m black --check --line-length $(MAX_LINE_LENGTH) --target-version $(PY_TARGET_VER) $(TEST); \
	$(PYTHON) -m black --check --line-length $(MAX_LINE_LENGTH) --target-version $(PY_TARGET_VER) *.py; \


check-isort:
	$(PYTHON) -m isort --check --line-length $(MAX_LINE_LENGTH) $(PROJ); \
	$(PYTHON) -m isort --check --line-length $(MAX_LINE_LENGTH) $(TEST); \
	$(PYTHON) -m isort --check --line-length $(MAX_LINE_LENGTH) *.py; \


check-pylint:
	echo "PyLinting spellbook source..."; \
	$(PYTHON) -m pylint $(PROJ) --rcfile=setup.cfg --disable=logging-fstring-interpolation; \
	$(PYTHON) -m pylint *.py --rcfile=setup.cfg --exit-zero
	echo "PyLinting spellbook tests..."; \
	$(PYTHON) -m pylint $(TEST) --rcfile=setup.cfg; \


check-copyright:
	@echo "🔍 Checking for required copyright header..."
	@missing_files=$$(find $(PROJ) $(TEST) \
		-name '*.py' -print | \
		xargs grep -L "Copyright (c) Lawrence Livermore National Security, LLC and other" || true); \
	if [ -n "$$missing_files" ]; then \
		echo "❌ The following files are missing the required copyright header:"; \
		echo "$$missing_files"; \
		exit 1; \
	else \
		echo "✅ All files contain the required header."; \
	fi


check-style: check-copyright check-flake8 check-black check-isort check-pylint
