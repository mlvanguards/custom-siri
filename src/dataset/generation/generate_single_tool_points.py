import logging
import random

from src.dataset.utils import render_template

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_single_tool_examples(tool_name, tool_data, count, start_id):
    logger.info(
        f"Generating {count} examples for tool '{tool_name}' starting from ID {start_id}"
    )
    examples = []
    for i in range(count):
        args = {k: random.choice(v) for k, v in tool_data.get("args", {}).items()}
        template = random.choice(tool_data["templates"])
        query = render_template(template, args)
        answers = [{"name": tool_name, "arguments": args}]
        tools = [
            {
                "name": tool_name,
                "description": tool_data["description"],
                "parameters": tool_data["parameters"],
            }
        ]
        logger.debug(
            f"Example {i + 1}: args={args}, template='{template}', query='{query}'"
        )
        examples.append(
            {"id": start_id, "query": query, "answers": answers, "tools": tools}
        )
        start_id += 1
    logger.info(f"Generated {len(examples)} examples for tool '{tool_name}'")
    return examples, start_id
