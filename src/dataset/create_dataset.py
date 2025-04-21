import json
import random
from pathlib import Path

# Full set of tools from user's provided functions
TOOLS = {
    "lock_screen": {
        "description": "Locks the laptop screen.",
        "parameters": {},
        "args": {},
        "templates": [
            "Lock the screen",
            "Please lock my laptop",
            "Activate screen lock",
        ],
    },
    "get_battery_status": {
        "description": "Returns battery level and charging status.",
        "parameters": {},
        "args": {},
        "templates": [
            "What's my battery status?",
            "How much battery do I have left?",
            "Is my laptop charging?",
        ],
    },
    "search_google": {
        "description": "Searches Google for a query.",
        "parameters": {
            "query": {"description": "The search query", "type": "str"},
        },
        "args": {"query": ["how to bake bread", "latest AI news", "best python tips"]},
        "templates": [
            "Search Google for '{query}'",
            "Look up '{query}' online",
            "Can you search: {query}?",
        ],
    },
    "set_volume": {
        "description": "Sets the system volume (0–100).",
        "parameters": {
            "level": {"description": "Volume level", "type": "int"},
        },
        "args": {"level": [10, 30, 50, 70, 90]},
        "templates": [
            "Set volume to {level}",
            "Adjust sound to {level} percent",
        ],
    },
    "create_note": {
        "description": "Creates a note using the Notes app.",
        "parameters": {
            "title": {"description": "Title of the note", "type": "str"},
            "content": {"description": "Content of the note", "type": "str"},
        },
        "args": {
            "title": ["Groceries", "Project Ideas"],
            "content": ["Buy milk and eggs", "Build an AI assistant"],
        },
        "templates": [
            "Create note '{title}' with content '{content}'",
            "Make a new note: {title} - {content}",
        ],
    },
}


def create_example(tool_name, tool_meta, idx):
    args = {}
    for k, v in tool_meta.get("args", {}).items():
        args[k] = random.choice(v)

    template = random.choice(tool_meta["templates"])
    query = template.format(**args)

    # answers and tools as stringified JSON
    answers = json.dumps([{"name": tool_name, "arguments": args}])

    tools = json.dumps(
        [
            {
                "name": tool_name,
                "description": tool_meta["description"],
                "parameters": tool_meta["parameters"],
            }
        ]
    )

    return {"id": idx, "query": query, "answers": answers, "tools": tools}


examples = []
example_id = 1
for tool_name, tool_data in TOOLS.items():
    for _ in range(300):  # 300 examples per function
        examples.append(create_example(tool_name, tool_data, example_id))
        example_id += 1

# Save to JSON
Path("data").mkdir(exist_ok=True)
with open("data/siri_xlam_dataset_v3.json", "w") as f:
    json.dump(examples, f, indent=2)
