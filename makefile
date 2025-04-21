# Default values for dataset generation
SINGLE_TOOL_EXAMPLES ?= 1
MULTI_TOOL_EXAMPLES ?= 1
UNKNOWN_INTENT_EXAMPLES ?= 1
PARAPHRASE_COUNT ?= 1
DATASET_NAME ?= dataset.json

.PHONY: help dataset

help:
	@echo "Available make targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dataset: ## Generate a dataset using configured environment variables
	PYTHONPATH=. python src/dataset/create_dataset.py \
		--single-tool-examples $(SINGLE_TOOL_EXAMPLES) \
		--multi-tool-examples $(MULTI_TOOL_EXAMPLES) \
		--unknown-intent-examples $(UNKNOWN_INTENT_EXAMPLES) \
		--paraphrase-count $(PARAPHRASE_COUNT) \
		--dataset-name $(DATASET_NAME)
