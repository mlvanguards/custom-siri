import json

from litellm import completion

from src.dataset.prompts import FORMAT_CHECK_PROMPT


def check_entry_format(entry: dict, model="gpt-4"):
    message = (
        f"Validate the following entry:\n\n```json\n{json.dumps(entry, indent=2)}\n```"
    )

    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": FORMAT_CHECK_PROMPT},
            {"role": "user", "content": message},
        ],
    )

    result = response["choices"][0]["message"]["content"].strip()
    return result


def run_format_checker(dataset: list):
    valid, invalid = [], []

    for entry in dataset:
        result = check_entry_format(entry)
        if result.startswith("VALID"):
            valid.append(entry)
        else:
            invalid.append((entry["id"], result))

    return valid, invalid
