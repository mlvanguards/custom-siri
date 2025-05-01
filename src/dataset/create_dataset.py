import argparse
import json
import logging
from pathlib import Path

from src.dataset.generation.generate_multi_tool_points import (
    generate_multi_tool_examples,
)
from src.dataset.generation.generate_negative_points import (
    generate_unknown_intent_examples,
)
from src.dataset.generation.generate_single_tool_points import (
    generate_single_tool_examples,
)
from src.dataset.generation.paraphrase import paraphrase_dataset
from src.dataset.tools_description import TOOLS

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def build_dataset(
    single_tool_examples_per_tool=50,
    multi_tool_examples=50,
    unknown_intent_examples=30,
    paraphrase_count=100,
    dataset_name: str = "dataset.json",
):
    logging.info("Starting dataset generation pipeline...")
    dataset = []
    idx = 1

    # Generate single tool examples
    logging.info("Generating single-tool examples...")
    total_single_tools = 0
    for tool_name, tool_data in TOOLS.items():
        single_tool, idx = generate_single_tool_examples(
            tool_name, tool_data, single_tool_examples_per_tool, idx
        )
        dataset.extend(single_tool)
        total_single_tools += len(single_tool)
    logging.info(f"Generated {total_single_tools} single-tool examples.")

    # Generate multi-tool examples
    logging.info("Generating multi-tool examples...")
    multi_tool, idx = generate_multi_tool_examples(
        multi_tool_examples, idx, use_hf_examples=True, num_examples=200
    )
    dataset.extend(multi_tool)
    logging.info(f"Generated {len(multi_tool)} multi-tool examples.")

    # Generate unknown intent examples
    logging.info("Generating unknown intent examples...")
    unknowns, idx = generate_unknown_intent_examples(unknown_intent_examples, idx)
    dataset.extend(unknowns)
    logging.info(f"Generated {len(unknowns)} unknown intent examples.")

    logging.info(f"Generated base dataset with {len(dataset)} examples.")

    # Paraphrase
    if paraphrase_count > 0:
        paraphrased = paraphrase_dataset(dataset, 1000, paraphrase_count)
        full_dataset = dataset + paraphrased
        logging.info(f"Added {len(paraphrased)} paraphrased examples.")
    else:
        full_dataset = dataset
        logging.info("Skipping paraphrasing as paraphrase_count is 0.")

    # Save
    try:
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        out_path = data_dir / dataset_name
        logging.info(f"Saving final dataset to {out_path}...")
        with open(out_path, "w") as f:
            json.dump(full_dataset, f, indent=2)
        logging.info(
            f"Saved final dataset with {len(full_dataset)} examples to {out_path}"
        )
    except IOError as e:
        logging.error(f"Failed to save dataset to {out_path}: {e}", exc_info=True)

    logging.info("Dataset generation pipeline finished.")


# Run
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate dataset")
    parser.add_argument(
        "--single-tool-examples",
        type=int,
        default=50,
        help="Number of examples per single tool",
    )
    parser.add_argument(
        "--multi-tool-examples",
        type=int,
        default=50,
        help="Number of multi-tool examples",
    )
    parser.add_argument(
        "--unknown-intent-examples",
        type=int,
        default=30,
        help="Number of unknown intent examples",
    )
    parser.add_argument(
        "--paraphrase-count",
        type=int,
        default=10,
        help="Number of paraphrased examples",
    )
    parser.add_argument(
        "--dataset-name",
        type=str,
        default="dataset.json",
        help="Output dataset filename",
    )

    args = parser.parse_args()

    build_dataset(
        single_tool_examples_per_tool=args.single_tool_examples,
        multi_tool_examples=args.multi_tool_examples,
        unknown_intent_examples=args.unknown_intent_examples,
        paraphrase_count=args.paraphrase_count,
        dataset_name=args.dataset_name,
    )
