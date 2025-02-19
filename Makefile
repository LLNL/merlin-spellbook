
VER?=1.0.0
VSTRING=[0-9]\+\.[0-9]\+\.[0-9]\+
PYTHON?=python3
PY_TARGET_VER?=py311  # At the time this is added (2/19/25) black only supports up to py311

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

# Use like this: make VER=?.?.? verison
version:
	# do spellbook/__init__.py
	sed -i 's/__version__ = "$(VSTRING)"/__version__ = "$(VER)"/g' $(PROJ)/__init__.py
	# do CHANGELOG.md
	sed -i 's/## \[Unreleased\]/## [$(VER)]/g' CHANGELOG.md
	# do all file headers (works on linux)
	find $(PROJ)/ -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'
	find *.py -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'
	find $(TEST)/ -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'
	find Makefile -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'

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


check-style: check-flake8 check-black check-isort check-pylint
