.PHONY: help tf-validate tf-plan tf-apply test lint install clean

PHASE ?= 01-foundation
ENV ?= dev

help:
	@echo "Usage:"
	@echo "  make tf-validate PHASE=01-foundation    Validate Terraform for a phase"
	@echo "  make tf-plan PHASE=01-foundation ENV=dev Plan Terraform for a phase"
	@echo "  make tf-apply PHASE=01-foundation ENV=dev Apply Terraform for a phase"
	@echo "  make install                             Install Python dependencies"
	@echo "  make test                                Run Python tests"
	@echo "  make lint                                Lint Python code"
	@echo "  make clean                               Remove build artifacts"

tf-validate:
	cd infra/phases/$(PHASE) && terraform init -backend=false && terraform validate

tf-plan:
	cd infra/phases/$(PHASE) && terraform init && terraform plan -var-file=../../../environments/$(ENV).tfvars

tf-apply:
	cd infra/phases/$(PHASE) && terraform init && terraform apply -var-file=../../../environments/$(ENV).tfvars

install:
	cd agents && pip install -e ".[dev]"

test:
	cd agents && pytest

lint:
	cd agents && ruff check .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
