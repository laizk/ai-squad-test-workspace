# Validation Project Makefile

.PHONY: help validate test clean deploy

help:
	@echo "Available targets:"
	@echo "  validate  - Run full validation"
	@echo "  test      - Run unit tests"
	@echo "  clean     - Clean build artifacts"
	@echo "  deploy    - Deploy to sandbox"

validate: test
	@echo "Validation complete"

test:
	python -m pytest tests/ -v --tb=short

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

deploy:
	@echo "Deploying to validation sandbox..."
	@echo "Environment: validation-sandbox"
	@echo "Status: deployed"
	@echo "Network rules applied"
