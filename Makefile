.PHONY: install lint format test run-api dev clean help run-mock run-all

PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
RUFF := $(PYTHON) -m ruff
BLACK := $(PYTHON) -m black
HYPERCORN := $(PYTHON) -m hypercorn

help:
	@echo "Available targets:"
	@echo "  install     - Install all dependencies including dev dependencies"
	@echo "  lint        - Run ruff linter"
	@echo "  format      - Format code with black and ruff"
	@echo "  test        - Run tests with pytest"
	@echo "  test-cov    - Run tests with coverage report"
	@echo "  run-api     - Start Quart server in production mode"
	@echo "  dev         - Start Quart server in development mode with auto-reload"
	@echo "  run-mock    - Start Mock Foundry Agent server on port 8001"
	@echo "  run-all     - Start both Mock Foundry Agent and Orchestrator API"
	@echo "  clean       - Remove Python cache files and build artifacts"
	@echo "  pre-commit  - Install pre-commit hooks"

install:
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]" --pre

create-agent:
	@echo " Creating new agent "

	@read -p "Agent name: " agent_name; \
	while [ -z "$$agent_name" ]; do \
		read -p "Agent name can't be empty. Agent Name: " agent_name; \
	done; \
	read -p "Agent Instruction: " agent_instruction; \
	while [ -z "$$agent_instruction" ]; do \
		read -p "The instructions can't be empty, Agent Instruction: " agent_instruction; \
	done; \
	read -p "Agent description (optional): " agent_description; \
	if [ -z "$$agent_description" ]; then \
		agent_description="Agente created by Makefile"; \
	fi; \
	read -p "Do you want to create new Vector Store (Y/n): " create_vs; \
	if [ "$$create_vs" = "Y" ] || [ "$$create_vs" = "y" ]; then \
		read -p "New Vector Store Name: " vs_name; \
		while [ -z "$$vs_name" ]; do \
			read -p "Vector Store Name can't be empty.Vector Store Name: " vs_name; \
		done; \
		read -p "Do you want to attache others Vector Stores (Y/n): " others_vs; \
		if [ "$$others_vs" = "Y" ] || [ "$$others_vs" = "y" ]; then \
			read -p "You can attach other vector stores using their ids(separated by commas) : " vs_ids; \
			while [ -z "$$vs_ids" ]; do \
				read -p "Ids can't be empty Vector Store Ids: " vs_ids; \
			done; \
		fi; \
	else \
    	echo "Skipping Vector Store creation..."; \
		read -p "You can attach other vector stores using their ids(separated by commas) : " vs_ids; \
		while [ -z "$$vs_ids" ]; do \
			read -p "Ids can't be empty Vector Store Ids: " vs_ids; \
		done; \
	fi; \
	echo "=== Summary ===";\
	echo "Agent Name: $$agent_name";\
	echo "Instructions: $$agent_instruction";\
	echo "Decription: $$agent_description";\
	echo "Vector Store Name: $$vs_name";\
	echo "Vector Store IDs: $$vs_ids";\
	read -p "Do you want to create agent? (y/n): " confirmar; \
	if [ "$$confirmar" = "y" ] || [ "$$confirmar" = "Y" ]; then \
		echo "Creating new agent ..."; \
		execute_command="python create_agent.py --agent-name \"$$agent_name\" --agent-instruction \"$$agent_instruction\" --agent-description \"$$agent_description\""; \
		if [ -n "$$vs_name" ]; then \
			execute_command="$$execute_command --vs-name \"$$vs_name\""; \
		fi; \
		if [ -n "$$vs_ids" ]; then \
			execute_command="$$execute_command --vs-ids \"$$vs_ids\""; \
		fi; \
		eval $$execute_command; \
	else \
		echo "Canceling operation ..."; \
		exit 1;	\
	fi

lint:
	$(RUFF) check app tests

format:
	$(BLACK) app tests
	$(RUFF) check --fix app tests

test:
	$(PYTEST) tests/

test-cov:
	$(PYTEST) --cov=app --cov-report=html --cov-report=term tests/

run-api:
	$(HYPERCORN) app.main:app --bind 0.0.0.0:8000

dev:
	$(HYPERCORN) app.main:app --bind 0.0.0.0:8000 --reload

pre-commit:
	pre-commit install

run-mock:
	@echo "============================================================"
	@echo "Starting Mock Foundry Agent on port 8001..."
	@echo "============================================================"
	$(PYTHON) mock_foundry_agent.py

run-all:
	@echo "============================================================"
	@echo "Starting Mock Foundry Agent and Orchestrator API..."
	@echo "============================================================"
	@echo "Mock will run on port 8001, Orchestrator on port 8000"
	@echo "Press Ctrl+C to stop both services"
	@echo "============================================================"
	@$(PYTHON) mock_foundry_agent.py & sleep 3 && $(HYPERCORN) app.main:app --bind 0.0.0.0:8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build dist htmlcov .coverage
