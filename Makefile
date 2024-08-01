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
	poetry add opencv-python
	poetry add pytesseract

#------------------------------------------------------------------------------
# Install after clone project
#------------------------------------------------------------------------------
.PHONY: set-env
set-env:
	poetry env use 3.12.4
	poetry install


#------------------------------------------------------------------------------
# run
#------------------------------------------------------------------------------
.PHONY: run
run:
	poetry run python ./src/main.py