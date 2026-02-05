# Makefile so you don't have to remember the exact commands

# This Makefile uses the 'uv' tool (https://docs.astral.sh/uv/) to manage
# virtual envs and dependencies.
#
# Each uv invocation automatically creates and updates its venv before it does
# its work. This means we can leave venv management out this Makefile.
#
# Uv also makes it easy to test with older versions of the dependencies using
# the --resolution=lowest-direct flag. We use that in target pytest-old.
#
# It can be installed from its website or using 'dnf'.


build:
	uv build

pytest:
	uv run pytest

pytest-old:
	uv run --resolution=lowest-direct pytest

# untested yet
upload:
	uv run twine upload dist/*.whl dist/*.tar.gz
