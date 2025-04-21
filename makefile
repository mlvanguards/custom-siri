# Default values for dataset generation
SINGLE_TOOL_EXAMPLES ?= 1
MULTI_TOOL_EXAMPLES ?= 1
UNKNOWN_INTENT_EXAMPLES ?= 1
PARAPHRASE_COUNT ?= 1
DATASET_NAME ?= dataset.json

# Default values for dataset upload
DATASET_PATH ?= data/siri_xlam_dataset_v2.json
HF_REPO_ID ?= valex95/siri-function-calling-v4
LOCAL_PATH ?= siri_function_calling_dataset

.PHONY: help dataset upload

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

upload: ## Upload dataset to Hugging Face Hub
	PYTHONPATH=. python src/dataset/upload_hf_dataset.py \
		--dataset-path $(DATASET_PATH) \
		--repo-id $(HF_REPO_ID) \
		--local-path $(LOCAL_PATH)
