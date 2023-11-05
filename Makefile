# ----------------Commands----------------
#
# # change the 20 value in printf to adjust width
# # Use ' ## some comment' behind a command and it will be added to the help message automatically
help: ## Show this help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format: ## Format the code
	@echo "\n=== Isort ================================="
	poetry run isort web_suck_it_py tests
	@echo "\n=== Black ================================="
	poetry run black --target-version py311 web_suck_it_py tests
	@echo ""

test: ## Poetry run tests
	poetry run pytest -x tests

install: ## Install poetry packages and mypy missing types
	@echo "\n=== Installing packages ================================="
	@poetry install
	@echo "\n=== Installing stub packages ================================="
	@poetry run mypy --install-types --non-interactive

stubgen: ## Generate typing stubfiles
	@echo "\n=== Generating Stubs =================================="
	@cd web_suck_it_py && poetry run stubgen request.py response.py channel.py error.py base.py __init__.py -o stubs

check: ## Check codebase against some standards
	@echo "\n=== Flake8 Checks =================================="
	@poetry run flake8 . --ignore=E203,E266,E501,W503,W505 --max-line-length=88 \
		--exclude tests/conftest.py,web_suck_it_py/__init__.py,.venv
	@echo "\n=== Mypy =================================="
	poetry run mypy web_suck_it_py tests
	@echo ""


# --------------Configuration-------------
#  #
#  .NOTPARALLEL: ; # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell

.PHONY: docs all # All targets are accessible for user
	        .DEFAULT: help # Running Make will run the help target

MAKEFLAGS += --no-print-directory # dont add message about entering and leaving the working directory

