import argparse
import json
import logging
import os
from typing import Any, Dict, List

from datasets import Dataset, Features, Value
from huggingface_hub import login

from settings import settings


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Upload dataset to Hugging Face Hub")
    parser.add_argument(
        "--dataset-path",
        type=str,
        default="data/siri_xlam_dataset_v3.json",
        help="Path to the JSON dataset file",
    )
    parser.add_argument(
        "--repo-id",
        type=str,
        default="valex95/siri-function-calling-v3",
        help="Hugging Face repository ID",
    )
    parser.add_argument(
        "--local-path",
        type=str,
        default="siri_function_calling_dataset",
        help="Local path to save the dataset",
    )
    return parser.parse_args()


# Configure logging
def setup_logging(log_file: str = "siri_upload.log") -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        log_file: Path to the log file

    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
    )
    return logging.getLogger(__name__)


def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """Load dataset from JSON file.

    Args:
        file_path: Path to the JSON dataset file

    Returns:
        List[Dict[str, Any]]: Loaded dataset

    Raises:
        FileNotFoundError: If dataset file doesn't exist
        json.JSONDecodeError: If JSON file is invalid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset file not found at {file_path}")

    with open(file_path, "r") as f:
        return json.load(f)


def create_dataset_features() -> Features:
    """Create and return dataset features schema.

    Returns:
        Features: Hugging Face dataset features
    """
    return Features(
        {
            "id": Value("int64"),
            "query": Value("string"),
            "answers": Value("string"),
            "tools": Value("string"),
        }
    )


def create_hf_dataset(data: List[Dict[str, Any]], features: Features) -> Dataset:
    """Create Hugging Face dataset from data.

    Args:
        data: List of data examples
        features: Dataset features schema

    Returns:
        Dataset: Hugging Face dataset
    """
    return Dataset.from_list(data, features=features)


def save_dataset_locally(dataset: Dataset, local_path: str) -> None:
    """Save dataset to local disk.

    Args:
        dataset: Hugging Face dataset
        local_path: Path to save dataset
    """
    dataset.save_to_disk(local_path)


def upload_to_hub(dataset: Dataset, repo_id: str, auth_token: str) -> None:
    """Upload dataset to Hugging Face Hub.

    Args:
        dataset: Hugging Face dataset
        repo_id: Hugging Face repository ID
        auth_token: Hugging Face authentication token

    Raises:
        Exception: If upload fails
    """
    login(token=auth_token)
    dataset.push_to_hub(repo_id)


def main() -> None:
    """Main execution function."""
    # Parse command line arguments
    args = parse_args()

    # Setup logging
    logger = setup_logging()

    try:
        # Load dataset
        logger.info(f"Loading dataset from {args.dataset_path}")
        data = load_dataset(args.dataset_path)
        logger.info(f"Loaded {len(data)} examples")
        logger.info(f"Example: {data[0]}")

        # Create dataset
        features = create_dataset_features()
        dataset = create_hf_dataset(data, features)

        # Save locally
        logger.info(f"Saving dataset locally to {args.local_path}")
        save_dataset_locally(dataset, args.local_path)

        # Upload to Hugging Face
        logger.info(f"Pushing dataset to Hugging Face: {args.repo_id}")
        upload_to_hub(dataset, args.repo_id, settings.auth.HUGGINGFACE_TOKEN)
        logger.info("✅ Dataset pushed successfully!")

    except FileNotFoundError as e:
        logger.error(f"❌ Dataset file error: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON format: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Failed to process dataset: {e}")
        raise


if __name__ == "__main__":
    main()
