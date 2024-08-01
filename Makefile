#------------------------------------------------------------------------------
# Only Initial install
#------------------------------------------------------------------------------
.PHONY: install-python
install-python:
	asdf plugin add python
	#asdf list all python
	asdf install python 3.12.4
	python -V
	asdf local python 3.12.4

# https://python-poetry.org/docs/#installing-with-the-official-installer
.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: create-project
create-project:
	poetry new ocr-py

.PHONY: install-dependencies
install-dependencies:
	poetry add opencv-python pytesseract
	poetry add -D flake8 black isort mypy pytest
	poetry add --group dev Flake8-pyproject

#------------------------------------------------------------------------------
# Install after clone project
#------------------------------------------------------------------------------
.PHONY: set-env
set-env:
	poetry env use 3.12.4
	poetry install

#------------------------------------------------------------------------------
# dev
#------------------------------------------------------------------------------
.PHONY: lint
lint:
	@#import文を自動整理す
	poetry run isort src
	@#PEP8に準拠したフォーマット
	poetry run black src
	@#文法チェック
	poetry run flake8 src

.PHONY: run
run:
	poetry run python main.py