import random

from litellm import completion

from settings import settings
from src.dataset.prompts import create_multi_tool_prompt
from src.dataset.tools_description import TOOLS


def generate_multi_tool_examples(count, start_id):
    examples = []
    tool_items = list(TOOLS.items())

    for _ in range(count):
        selected = random.sample(tool_items, 2)
        tool_payload = []
        answers, tools_list = [], []

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

        prompt = create_multi_tool_prompt(tool_payload)

        try:
            response = completion(
                model=settings.dataset.GPT_MODEL,
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
            start_id += 1
        except Exception as e:
            print(f"[ERROR] Skipping due to LLM error: {e}")

    return examples, start_id
