import logging
import random

from src.dataset.tools_description import UNKNOWN_INTENTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_unknown_intent_examples(count, start_id):
    examples = []
    logger.info(
        f"Generating {count} unknown intent examples starting from id {start_id}"
    )
    for _ in range(count):
        query = random.choice(UNKNOWN_INTENTS)
        logger.debug(f"Selected query: {query} for id {start_id}")
        examples.append(
            {
                "id": start_id,
                "query": query,
                "answers": [],
                "tools": [],
            }
        )
        start_id += 1
    logger.info(f"Generated {len(examples)} examples. Next start_id: {start_id}")
    return examples, start_id
