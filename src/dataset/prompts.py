def create_multi_tool_prompt(tool_payload):
    prompt_multi_tool = f"""You are helping build a natural language interface for an AI assistant. The assistant can call multiple functions in response to user commands.

    Here are two tools the assistant can use:
    {chr(10).join(tool_payload)}

    Write a natural instruction that would require using BOTH tools at once. Be specific and helpful."""

    return prompt_multi_tool


def create_paraphrase_prompt(query):
    prompt_paraphrase = f"""Paraphrase the following sentence while keeping its meaning and intention the same. Make it sound natural and human-like.

    Input: {query}
    Paraphrase:"""
    return prompt_paraphrase
