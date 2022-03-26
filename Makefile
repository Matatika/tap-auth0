.PHONY: help init link lint-fix

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: ## Initialise repo for local development
	@! test -d ~/.cache/pre-commit || poetry run pre-commit clean
	@poetry run pre-commit install -f --install-hooks

lint: ## Lint source files
	@poetry run black --check .

lint-fix: ## Lint source files and fix any issues
	@poetry run black .

test: ## Run tests
	@poetry run pytest
