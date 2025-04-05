.PHONY: venv update-requirements

PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

all: setup

venv:
	# Check if the venv directory exists, if not create it
	# Update the venv directory to the latest version (pip, setuptools, etc)
	# Because the venv directory is created with python3, all the following commands will use python3 by default
	# even with the usage of 'python' or 'pip'.
	[ -d .venv ] || python3 -m venv --upgrade-deps .venv

setup: venv
	# Upgrade/install wheel to the latest version.
	# Wheel is a package format for Python that speeds up package installation by avoiding the need for
	# running setup.py and compilation, which makes it a preferred format over source archives.
	$(PIP) install --upgrade wheel

	# Install all dependencies listed in requirements.txt into the virtual environment
	$(PIP) install -r requirements.txt

depfreeze: venv
	# Generate a requirements.txt file with all the dependencies installed in the virtual environment
	$(PIP) freeze > requirements.txt

lint:
	ruff check --select I  # Check import sorting
	ruff format --check  # Check formatting
	mypy .  # Static type checking
	ruff check  # Run full limnting without fixing

lint/fix:
	ruff check --select I --fix  # Fix import sorting
	ruff format  # Fix formatting
	ruff check --fix  # Fix other auto-fixable lint issues
	mypy .  # Static type checking (does not fix, just reports)
