SHELL := /usr/bin/bash
.DEFAULT_GOAL := help

# AutoDoc
# -------------------------------------------------------------------------
.PHONY: help
help: ## This help. Please refer to the Makefile to more insight about the usage of this script.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

# Docker
# -------------------------------------------------------------------------

# BOT
# -------------------------------------------------------------------------
.PHONY: build-docker-bot
build-docker-bot: ## Build the Telegram Bot Dockerfile. Optional variables BUILDKIT, DOCKER_BOT_IMAGE and DOCKER_BOT_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_BOT_IMAGE=$(or $(DOCKER_BOT_IMAGE),mairror-bot) \
		DOCKER_BOT_TAG=$(or $(DOCKER_BOT_TAG),test) && \
	docker build -t $$DOCKER_BOT_IMAGE:$$DOCKER_BOT_TAG .
.DEFAULT_GOAL := build-docker-bot

.PHONY: lint-docker-bot
lint-docker-bot: ## Lint the Telegram Bot Dockerfile
	docker run --rm -i -v ${PWD}:/hadolint --workdir=/hadolint hadolint/hadolint < Dockerfile
.DEFAULT_GOAL := lint-docker-bot

.PHONY: run-docker-bot
run-docker-bot: ## Run the BOT isolated. Optional variables BUILDKIT, DOCKER_BOT_IMAGE and DOCKER_BOT_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_BOT_IMAGE=$(or $(DOCKER_BOT_IMAGE),mairror-bot) \
		DOCKER_BOT_TAG=$(or $(DOCKER_BOT_TAG),test) && \
	docker run --rm --name $$DOCKER_BOT_IMAGE --env-file .env $$DOCKER_BOT_IMAGE:$$DOCKER_BOT_TAG
.DEFAULT_GOAL := run-docker-bot

# Python
# -------------------------------------------------------------------------

# Cache
# -------------------------------------------------------------------------
.PHONY: clean-pyc
clean-pycache: ## Clean pycache files

	find . -name '__pycache__' -exec rm -rf {} +
.DEFAULT_GOAL := clean-pyc

# Tests
# -------------------------------------------------------------------------
# .PHONY: test
# test: ## Run all test with pytest
# 	pytest src/tests
# .DEFAULT_GOAL := test
