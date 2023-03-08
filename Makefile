
VER?=1.0.0
VSTRING=[0-9]\+\.[0-9]\+\.[0-9]\+

PROJ=spellbook
TEST=tests

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
	python3 -m isort --line-length 88 $(PROJ)
	python3 -m isort --line-length 88 $(TEST)
	python3 -m isort --line-length 88 *.py
	python3 -m black --line-length 88 --target-version py36 $(PROJ)
	python3 -m black --line-length 88 --target-version py36 $(TEST)
	python3 -m black --line-length 88 --target-version py36 *.py

check-style:
	python3 -m black --check --line-length 88 --target-version py36 $(PROJ)
	python3 -m black --check --line-length 88 --target-version py36 $(TEST)
	python3 -m pylint $(PROJ) --rcfile=setup.cfg --exit-zero
	python3 -m pylint *.py --rcfile=setup.cfg --exit-zero
