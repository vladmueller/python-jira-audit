PYTHON_VENV = venv

ifeq ($(OS),Windows_NT)
    PYTHON = $(PYTHON_VENV)/Scripts/python.exe
else
    PYTHON = $(PYTHON_VENV)/bin/python
endif


# Create virtual environment if it does not exist and install dependencies
$(PYTHON):
	python3 -m venv $(PYTHON_VENV)
	$(PYTHON) -m pip install --upgrade pip
ifneq ("$(wildcard requirements.txt)", "")
	$(PYTHON) -m pip install -r requirements.txt
endif


install:
	$(MAKE) python


audit: $(PYTHON)
	@$(PYTHON) audit.py


clean:
	@echo "Cleaning up..."


.PHONY: install clean python
