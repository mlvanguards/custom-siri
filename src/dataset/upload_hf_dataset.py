import json
import logging
import os

from datasets import Dataset, Features, Value
from huggingface_hub import login

from settings import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("siri_upload.log")],
)
logger = logging.getLogger(__name__)

# File path
DATASET_PATH = "data/siri_xlam_dataset_v3.json"
HF_DATASET_REPO = "valex95/siri-function-calling-v3"

# Load your JSON file
logger.info(f"Loading dataset from {DATASET_PATH}")
if not os.path.exists(DATASET_PATH):
    logger.error("Dataset file does not exist.")
    exit(1)

with open(DATASET_PATH, "r") as f:
    data = json.load(f)

# Log example
logger.info(f"Loaded {len(data)} examples")
logger.info(f"Example: {data[0]}")

# Define Hugging Face features
features = Features(
    {
        "id": Value("int64"),
        "query": Value("string"),
        "answers": Value("string"),
        "tools": Value("string"),
    }
)

# Create Hugging Face dataset
logger.info("Creating Hugging Face dataset...")
dataset = Dataset.from_list(data, features=features)

# Save to disk (optional backup)
LOCAL_PATH = "siri_function_calling_dataset"
logger.info(f"Saving dataset locally to {LOCAL_PATH}...")
dataset.save_to_disk(LOCAL_PATH)

# Authenticate and push to HF
try:
    logger.info("Logging into Hugging Face Hub...")
    login(token=settings.HF_AUTH_TOKEN)

    logger.info(f"Pushing dataset to Hugging Face: {HF_DATASET_REPO}")
    dataset.push_to_hub(HF_DATASET_REPO)

    logger.info("✅ Dataset pushed successfully!")
except Exception as e:
    logger.error(f"❌ Failed to push dataset: {e}")
