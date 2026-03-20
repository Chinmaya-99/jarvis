import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"profile": {}, "facts": []}

def save_memory(memory_store):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f, indent=2)

memory_store = load_memory()

def handle_memory_commands(user_input):
    text = user_input.lower()

    if text.startswith("remember "):
        fact = user_input[len("remember "):].strip()
        memory_store["facts"].append(fact)
        save_memory(memory_store)
        return "I will remember that, Sir."

    if text.startswith("forget "):
        keyword = user_input[len("forget "):].strip().lower()
        memory_store["facts"] = [
            f for f in memory_store["facts"] if keyword not in f.lower()
        ]
        save_memory(memory_store)
        return "I have forgotten that, Sir."

    if "what do you remember" in text:
        if not memory_store["facts"]:
            return "I do not have any stored memories yet, Sir."
        return "Here is what I remember:\n- " + "\n- ".join(memory_store["facts"])

    return None


def extract_name(user_input):
    triggers = ["my name is", "i am", "call me"]

    for t in triggers:
        if t in user_input.lower():
            name = user_input.lower().split(t)[-1].strip().title()
            memory_store["profile"]["name"] = name
            save_memory(memory_store)
            return f"Understood, Sir. I will remember your name is {name}."

    return None
