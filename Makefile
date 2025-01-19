.PHONY: all
all: format test requirements

.PHONY: format
format:
	@uv run black --target-version py313 .

.PHONY: test
test:
	@uv run pytest -v

.PHONY: requirements
requirements:
	@uv export --format requirements-txt --no-dev > requirements.txt

.PHONY: docker
docker:
	@docker build -t shinomineko/ansible-cyberark-utils:test .
