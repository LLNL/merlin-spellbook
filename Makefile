
VER?=1.0.0
VSTRING=[0-9]\+\.[0-9]\+\.[0-9]\+

PROJ=spellbook
TEST=tests
MAX_LINE_LENGTH=127
MAX_COMPLEXITY=15

unit-tests:
	python -m pytest $(TEST)/

command-line-tests:
	python $(TEST)/command_line_tests.py

tests: unit-tests command-line-tests

release:
	python -m build .

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
	isort --line-length $(MAX_LINE_LENGTH) $(PROJ)
	isort --line-length $(MAX_LINE_LENGTH) $(TEST)
	isort --line-length $(MAX_LINE_LENGTH) *.py
	black --line-length $(MAX_LINE_LENGTH) --target-version py36 $(PROJ)
	black --line-length $(MAX_LINE_LENGTH) --target-version py36 $(TEST)
	black --line-length $(MAX_LINE_LENGTH) --target-version py36 *.py

check-flake8:
	echo "Flake8 linting for invalid source (bad syntax, undefined variables)..."; \
	flake8 --count --select=E9,F63,F7,F82 --show-source --statistics; \
	echo "Flake8 linting failure for CI..."; \
	flake8 . --count --max-complexity=15 --statistics --max-line-length=127; \


check-black:
	black --check --line-length $(MAX_LINE_LENGTH) --target-version py36 $(PROJ); \
	black --check --line-length $(MAX_LINE_LENGTH) --target-version py36 $(TEST); \
	black --check --line-length $(MAX_LINE_LENGTH) --target-version py36 *.py; \


check-isort:
	isort --check --line-length $(MAX_LINE_LENGTH) $(PROJ); \
	isort --check --line-length $(MAX_LINE_LENGTH) $(TEST); \
	isort --check --line-length $(MAX_LINE_LENGTH) *.py; \


check-pylint:
	echo "PyLinting spellbook source..."; \
	pylint $(PROJ) --rcfile=setup.cfg; \
	echo "PyLinting spellbook tests..."; \
	pylint $(TEST) --rcfile=setup.cfg; \

check-mypy:
	echo "mypying spellbook source..."; \
	mypy $(PROJ) --config-file=setup.cfg; \
	echo "mypying spellbook tests..."; \
	mypy $(TEST) --config-file=setup.cfg; \

check-style: check-flake8 check-black check-isort check-pylint check-mypy

check-push: tests check-style