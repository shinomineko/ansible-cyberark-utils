.PHONY: all
all: format test

.PHONY: format
format:
	@black --target-version py310 .

.PHONY: test
test:
	@pytest -v
