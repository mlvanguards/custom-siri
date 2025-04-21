import json

import requests

from src.functions.functions import available_function_calls

if __name__ == "__main__":
    query = """
    o give me the status of my laptop battery
    """

    prompt = f"""
    You are a local assistant that calls functions. Only return a JSON array like this:
    Always respond ONLY in this JSON format:

[
  {{
    "name": "function_name",
    "arguments": {{
      "param1": "value1",
      ...
    }}
  }}
]

Use these functions: {list(available_function_calls.keys())}

User: {query}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "hf.co/valex95/llama3.1_ollama_v2:Q4_K_M",
            "prompt": prompt,
            "stream": False,
        },
    )

    response_text = response.json()["response"]
    print("\n💬 Model response:\n", response_text)

    # -------------- Parse and Execute Tool Calls ------------------

    try:
        function_calls = json.loads(response_text)
        print("\n🔧 Executing tool calls...")
        for func in function_calls:
            name = func.get("name")
            args = func.get("arguments", {})
            if name in available_function_calls:
                result = available_function_calls[name](**args)
                print(f"\n✅ {name}({args}) -> {result}")
            else:
                print(f"\n❌ Unknown function: {name}")
    except Exception as e:
        print("❌ Failed to parse model output as JSON:", e)
