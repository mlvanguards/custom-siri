import logging
import random

from litellm import completion

from settings import settings
from src.dataset.prompts import create_multi_tool_prompt
from src.dataset.tools_description import TOOLS

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def generate_multi_tool_examples(count, start_id, use_hf_examples=True, num_examples=5):
    examples = []
    tool_items = list(TOOLS.items())

    logging.info(f"Starting generation of {count} multi-tool examples.")

    for i in range(count):
        selected = random.sample(tool_items, 2)
        tool_payload = []
        answers, tools_list = [], []

        logging.debug(
            f"Example {i + 1}: Selected tools: {[name for name, _ in selected]}"
        )

        for tool_name, tool_data in selected:
            args = {k: random.choice(v) for k, v in tool_data.get("args", {}).items()}
            answers.append({"name": tool_name, "arguments": args})
            tools_list.append(
                {
                    "name": tool_name,
                    "description": tool_data["description"],
                    "parameters": tool_data["parameters"],
                }
            )
            tool_payload.append(f"- {tool_name}({args}) ➜ {tool_data['description']}")
            logging.debug(f"Tool: {tool_name}, Args: {args}")

        prompt = create_multi_tool_prompt(
            tool_payload=tool_payload,
            use_hf_examples=use_hf_examples,
            num_examples=num_examples,
        )

        try:
            response = completion(
                model=settings.dataset.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            query = response["choices"][0]["message"]["content"].strip()
            examples.append(
                {
                    "id": start_id,
                    "query": query,
                    "answers": answers,
                    "tools": tools_list,
                }
            )
            logging.info(f"Generated example with id {start_id}")
            start_id += 1
        except Exception as e:
            logging.error(f"Skipping due to LLM error: {e}")

    logging.info(f"Finished generating examples. Total: {len(examples)}")
    return examples, start_id


if __name__ == "__main__":
    examples, start_id = generate_multi_tool_examples(10, 1)
    logging.info(f"Generated examples: {examples}")
