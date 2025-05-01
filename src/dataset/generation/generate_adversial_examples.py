def generate_adversarial_examples(tools, count, start_id):
    examples = []
    adversarial_templates = [
        # Ambiguous
        "Do the thing with the battery and sound, you know what I mean.",
        "Check if I'm charging and also not charging.",
        # Typos
        "Plase l0ck teh sceren now!",
        "Gte the btry staus an crete a not.",
        # Misleading structure
        "Search 'lock screen' on Google and then actually lock the screen.",
        "Write a note titled 'Battery Status' saying 'Lock the screen first.'",
        # Conflicting
        "Mute the volume and set it to 100.",
        # Function overload
        "Create a note, search Google, lock the screen, and check battery.",
    ]

    for i in range(min(count, len(adversarial_templates))):
        query = adversarial_templates[i]
        examples.append(
            {
                "id": start_id,
                "query": query,
                "answers": [],  # Ideally left blank for adversarial, or filled incorrectly on purpose
                "tools": [],  # Can optionally include misleading tool suggestions
                "adversarial": True,
            }
        )
        start_id += 1

    return examples, start_id
