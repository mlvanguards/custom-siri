from src.dataset.utils import extract_datapoints_hf_dataset


def create_multi_tool_prompt(
    tool_payload,
    use_hf_examples: bool = False,
    num_examples: int = 5,
):
    prompt_multi_tool = f"""
You are an AI data generation expert. Your goal is to write **clear, natural-sounding user instructions** that require the AI assistant to **use multiple tools at once** to complete the task.

---

🔧 Tools available to the assistant:
{chr(10).join(tool_payload)}

---

🧠 Your task:
Generate a **realistic user instruction** (like one you'd say to a smart assistant or a chatbot) that **requires using BOTH tools** to fulfill the request. Make sure the instruction is:

1. **Specific**: Include clear details (like timeframes, names, locations, etc.).
2. **Natural**: Make it sound like a real request someone would make.
3. **Multi-functional**: The task should truly require both tools. Avoid simplistic or single-tool requests.

---

✅ Output format:
Just write the user instruction as plain text. Do **not** describe how the tools are used—just the instruction.

"""

    if use_hf_examples:
        best_practices = extract_datapoints_hf_dataset(num_datapoints=num_examples)

        prompt_multi_tool += (
            "\n\n🧪 Examples of high-quality multi-tool instructions:\n"
        )
        for i, practice in enumerate(best_practices):
            prompt_multi_tool += f"\nExample {i + 1}:\n{practice}\n"

    return prompt_multi_tool.strip()


def create_paraphrase_prompt(query):
    prompt_paraphrase = f"""Paraphrase the following sentence while keeping its meaning and intention the same. Make it sound natural and human-like.

    Input: {query}
    Paraphrase:"""
    return prompt_paraphrase


FORMAT_CHECK_PROMPT = """
You are a dataset validation expert. Your task is to validate the format of JSON entries used in a function-calling dataset.

Each entry must follow this strict format:

- "id": an integer
- "query": a non-empty natural language instruction
- "answers": a list of one or more dicts with:
  - "name": a string (function name)
  - "arguments": a dictionary of named arguments and their values
- "tools": a list of one or more dicts with:
  - "name": same string as in answers
  - "description": string
  - "parameters": a dictionary of parameter names and types

Respond ONLY with:
- `VALID ✅` if everything is perfect
- `INVALID ❌: <reason>` if there's any format issue
"""
