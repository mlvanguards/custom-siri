import json

from datasets import load_dataset


def render_template(template, args):
    return template.format(**args)


def extract_datapoints_hf_dataset(
    dataset="Salesforce/xlam-function-calling-60k", num_datapoints=1000
) -> list[dict]:
    """
    Extracts a specified number of datapoints from a Hugging Face dataset.

    Args:
        dataset (str): The name of the Hugging Face dataset to load.
        num_datapoints (int): The number of datapoints to extract.
    """

    str_data = []

    datasets = load_dataset(dataset)

    shuffled = datasets["train"].shuffle(seed=42)

    first_1000 = shuffled.select(range(num_datapoints))

    for datapoint in first_1000:
        str_data.append(json.dumps(datapoint, indent=2))

    return str_data
