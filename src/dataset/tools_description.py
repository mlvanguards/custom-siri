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
        "templates": ["What's my battery status?", "Is my laptop charging?"],
    },
    "search_google": {
        "description": "Searches Google for a query.",
        "parameters": {"query": {"description": "Search query", "type": "str"}},
        "args": {"query": ["how to bake bread", "latest AI news", "best python tips"]},
        "templates": ["Search Google for '{query}'", "Can you search: {query}?"],
    },
    "set_volume": {
        "description": "Sets system volume (0–100).",
        "parameters": {"level": {"description": "Volume level", "type": "int"}},
        "args": {"level": [10, 30, 50, 70, 90]},
        "templates": ["Set volume to {level}", "Adjust sound to {level} percent"],
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

UNKNOWN_INTENTS = [
    "What's the weather like today?",
    "Book a flight to Paris.",
    "Who won the football match?",
    "Send an email to my boss.",
    "Translate 'hello' to Japanese.",
]
