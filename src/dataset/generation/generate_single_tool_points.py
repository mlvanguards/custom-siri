import random

from src.dataset.utils import render_template


def generate_single_tool_examples(tool_name, tool_data, count, start_id):
    examples = []
    for _ in range(count):
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
        examples.append(
            {"id": start_id, "query": query, "answers": answers, "tools": tools}
        )
        start_id += 1
    return examples, start_id
