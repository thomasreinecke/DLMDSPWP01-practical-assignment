VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: all install clean test

all: install

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

test: install
	$(VENV)/bin/pytest tests/
