.PHONY: run stop logs build flake8 black mypy isort tests unit integration

VENV := .venv

# ============================
#       Local Development
# ============================
run:
	. $(VENV)/bin/activate && fastapi dev src/main.py --port=20000

shell:
	bash -c "source $$(pipenv --venv)/bin/activate && python"


# Needed if you need to generate NEW RSA certificates for JWT Authorization
generate_certificates:
	openssl genrsa -out ./conf/cert_private.pem 2048 && openssl rsa -in ./conf/cert_private.pem -pubout -out ./conf/cert_public.pem

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
	bash -c "source $$(pipenv --venv)/bin/activate && flake8 --config=.flake8 dependencies/ src/"

black:
	bash -c "source $$(pipenv --venv)/bin/activate && black --config=pyproject.toml dependencies/ src/"

mypy:
	bash -c "source $$(pipenv --venv)/bin/activate && mypy dependencies/ && mypy src/"

isort:
	bash -c "source $$(pipenv --venv)/bin/activate && isort dependencies/ src/"

# =========================
# 		Tests
# =========================

tests: unit integration

unit:
	@. $(VENV)/bin/activate && pytest ./tests/unit

integration:
	@. $(VENV)/bin/activate && pytest ./tests/integration
