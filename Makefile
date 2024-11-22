.PHONY: all
all: format test requirements

.PHONY: format
format:
	@black --target-version py310 .

.PHONY: test
test:
	@pytest -v

.PHONY: requirements
requirements:
	@pipenv requirements > requirements.txt

.PHONY: docker
docker:
	@docker build -t shinomineko/ansible-cyberark-utils:test .
