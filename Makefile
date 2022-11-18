.PHONY: help init link lint-fix

help:
	@echo AVAILABLE COMMANDS
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-23s\033[0m%s\n", $$1, $$2}'

init: ## Initialise repo for local development
	@poetry install -v
	@! test -d ~/.cache/pre-commit || poetry run pre-commit clean
	@poetry run pre-commit install -f --install-hooks

lint: ## Lint source files
	poetry run autoflake --check --recursive --exclude tests --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --verbose tap_auth0
	poetry run isort --check --diff tap_auth0
	poetry run black --check --diff tap_auth0
	poetry run flake8 --max-complexity 10 tap_auth0

lint-fix: ## Lint source files and fix any issues
	poetry run autoflake --in-place --recursive --exclude tests --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --verbose tap_auth0
	poetry run isort tap_auth0
	poetry run black tap_auth0

test: ## Run tests
	@poetry run pytest
