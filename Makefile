.PHONY: setup \
		mypy \
		lint \
		test \
		black \
		help

PIP_VERSION = 21.3.1

venv/bin/activate: ## Alias for virtual environment
	python -m venv venv

setup: venv/bin/activate ## Project setup
	. venv/bin/activate; pip install pip==${PIP_VERSION} wheel setuptools
	. venv/bin/activate; pip install --exists-action w -Ur requirements.txt


mypy: venv/bin/activate ## Run mypy
	. venv/bin/activate; mypy ./

lint: venv/bin/activate ## Run linter
	. venv/bin/activate; flake8 ./

db: venv/bin/activate ## Run migrations
	. venv/bin/activate; python manage.py migrate

run: venv/bin/activate ## Local Run
	. venv/bin/activate; python manage.py runserver

test: venv/bin/activate ## Run tests
	. venv/bin/activate; python manage.py test

file_to_black = .
black: venv/bin/activate ## Run isort and black
	. venv/bin/activate; isort $(file_to_black); black $(file_to_black)
