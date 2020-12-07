
VER?=1.0.0
VSTRING=[0-9]\+\.[0-9]\+\.[0-9]\+

unit-tests:
	python3 -m pytest tests/

release:
	python3 setup.py sdist bdist_wheel

# Use like this: make VER=?.?.? verison
version:
	# do spellbook/__init__.py
	sed -i 's/__version__ = "$(VSTRING)"/__version__ = "$(VER)"/g' spellbook/__init__.py
	# do CHANGELOG.md
	sed -i 's/## \[Unreleased\]/## [$(VER)]/g' CHANGELOG.md
	# do all file headers (works on linux)
	find spellbook/ -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'
	find *.py -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'
	find tests/ -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'
	find Makefile -type f -print0 | xargs -0 sed -i 's/Version: $(VSTRING)/Version: $(VER)/g'

clean:
	-find spellbook -name "*.py[cod]" -exec rm -f {} \;
	-find spellbook -name "__pycache__" -type d -exec rm -rf {} \;
	-rm -rf dist
	-rm -rf build
