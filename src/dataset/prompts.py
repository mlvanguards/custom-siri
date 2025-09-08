from src.dataset.utils import extract_datapoints_hf_dataset


def create_multi_tool_prompt(
    tool_payload,
    use_hf_examples: bool = False,
    num_examples: int = 10,  
):
    # Parse the tool_payload to extract the specific tool calls that were generated
    # tool_payload format: ["- search_google({'query': 'pizza recipes'}) ➜ Searches Google for a query."]
    
    tool_calls = []
    for payload_line in tool_payload:
        # Extract the tool call part before the arrow
        if '➜' in payload_line:
            tool_call = payload_line.split('➜')[0].strip('- ').strip()
            tool_calls.append(tool_call)
    
    tool_calls_text = " and ".join(tool_calls)
    
    prompt_multi_tool = f"""Write a natural user request that would need these exact tool calls:
{tool_calls_text}

Example requests:
- "Search for Italian recipes and save them to my cooking notes"
- "Set volume to 70% then lock the screen for security"
- "Check my battery level and create a note about it"

❌ DON'T write:
- "Here's a request..." 
- "The user wants..."
- Any explanations

✅ Write the direct user request:"""

    if use_hf_examples:
        # Extract only the actual user queries, not full JSON
        best_practices = extract_datapoints_hf_dataset(num_datapoints=num_examples)
        
        # Parse and extract just the user queries from the JSON
        actual_queries = []
        for practice in best_practices: 
            try:
                import json
                if isinstance(practice, str):
                    data = json.loads(practice)
                    if 'query' in data:  
                        actual_queries.append(data['query'])
            except:
                continue
        
        if actual_queries:
            prompt_multi_tool += f"\n\nSimilar examples:\n"
            for query in actual_queries:
                prompt_multi_tool += f"- \"{query}\"\n"

    return prompt_multi_tool.strip()


def create_paraphrase_prompt(query):
    return f"""Rewrite this user request in different words but same meaning:

Original: {query}

❌ DON'T write explanations, steps, or multiple options
❌ DON'T use markdown or formatting
✅ Write ONLY the rephrased request:"""


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
