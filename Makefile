venv/:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip wheel setuptools

venv/bin/pytest: venv/
	venv/bin/pip install -e ".[test]"

pytest: venv/bin/pytest
	venv/bin/pytest -r A


venv/bin/twine: setup
	venv/bin/pip install twine

sdist: setup
	venv/bin/python setup.py build sdist

wheel: setup
	venv/bin/python setup.py build bdist_wheel

upload: venv/bin/twine wheel sdist
	venv/bin/twine upload dist/*.whl dist/*.tar.gz
