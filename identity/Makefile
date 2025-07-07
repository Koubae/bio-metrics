.PHONY: run stop logs build flake8 black mypy isort tests unit integration

VENV := .venv

# ============================
#       Local Development
# ============================

run:
	bash -c "source $$(pipenv --venv)/bin/activate && python src/main.py"

shell:
	bash -c "source $$(pipenv --venv)/bin/activate && python"

# --------------------------
# Init
# --------------------------
init-venv: .update-env-file .install-pip-env .install-env .install-deps

.install-pip-env:
	pip install --user pipenv

.install-env:
	pipenv install --python=$(which python)

.install-deps:
	bash -c "source $$(pipenv --venv)/bin/activate && pipenv update --dev"

.update-env-file:
	@echo 'Updating .env from .env.example 🖋️...'
	# Updating .env
	@cp .env.example .env

# =========================
# 		Code Quality
# =========================
quality-checks: isort black flake8 mypy

flake8:
	bash -c "source $$(pipenv --venv)/bin/activate && flake8 --config=.flake8 src/"

black:
	bash -c "source $$(pipenv --venv)/bin/activate && black --config=pyproject.toml  src/"

mypy:
	bash -c "source $$(pipenv --venv)/bin/activate && mypy src/"

isort:
	bash -c "source $$(pipenv --venv)/bin/activate && isort src/"
