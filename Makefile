unit-tests:
	python3 -m pytest tests/

release:
	python3 setup.py sdist bdist_wheel
