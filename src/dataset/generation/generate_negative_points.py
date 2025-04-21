import random

from src.dataset.tools_description import UNKNOWN_INTENTS


def generate_unknown_intent_examples(count, start_id):
    examples = []
    for _ in range(count):
        query = random.choice(UNKNOWN_INTENTS)
        examples.append(
            {
                "id": start_id,
                "query": query,
                "answers": [],
                "tools": [],
            }
        )
        start_id += 1
    return examples, start_id
