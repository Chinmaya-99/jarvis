from openai import OpenAI
import json
import os
import pyttsx3
# ================== OPENROUTER CLIENT ==================
#client = OpenAI(
#    api_key=os.getenv("OPENROUTER_API_KEY"),
#    base_url="https://openrouter.ai/api/v1"
#)
OPENROUTER_API_KEY = "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"
fast_api_key="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"
client = OpenAI(
    api_key=fast_api_key,
    base_url="https://openrouter.ai/api/v1"
)


# ================== JARVIS PERSONALITY ==================
SYSTEM_PROMPT = """
You are JARVIS.
You DO have memory of previous conversations provided to you.
You should use that memory to answer questions about the user.
Rules:
- By default, give SHORT and DIRECT answers (2,3 sentences max).
- Do NOT explain unless the user explicitly asks.
- If the user says words like:
  "explain", "why", "how", "in detail", "deep", "steps"
  then give a detailed explanation.
- Keep answers precise and simple.
- Address the user as "Sir".
"""


# ================== MEMORY SETUP ==================
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
chat_history = []   # (temporary, not saved)

#===================remeber/forget command=============

def handle_memory_commands(user_input):
    text = user_input.lower()

    # Remember command
    if text.startswith("remember "):
        fact = user_input[len("remember "):].strip()
        memory_store["facts"].append(fact)
        save_memory(memory_store)
        return f"I will remember that, Sir."

    # Forget command
    if text.startswith("forget "):
        keyword = user_input[len("forget "):].strip().lower()
        memory_store["facts"] = [
    f for f in memory_store["facts"] if keyword not in f.lower()
]

        save_memory(memory_store)
        return f"I have forgotten that, Sir."

    # Ask memory
    if "what do you remember" in text:
        if not memory_store["facts"]:
            return "I do not have any stored memories yet, Sir."
        return "Here is what I remember about you:\n- " + "\n- ".join(memory_store["facts"])

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


#=============tts============

engine = pyttsx3.init()
engine.setProperty("rate", 150)
def speak_any(reply):
    try:
        text = str(reply)   # convert ANY dtype to text
        if text.strip():
            voices=engine.getProperty("voices")
            engine.setProperty("voice",voices[0].id)
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)
# ================== JARVIS RESPONSE ==================
def wants_detail(user_input):
    detail_words = [
        "explain", "why", "how", "detail",
    "deep", "steps", "elaborate"
     ]
    return any(word in user_input.lower() for word in detail_words)
def jarvis_reply(user_input):
    print("[JARVIS] Thinking...", flush=True)

    #  Memory commands
    cmd_response = handle_memory_commands(user_input)
    if cmd_response:
        return cmd_response

    name_response = extract_name(user_input)
    if name_response:
        return name_response

    #  Build memory context FIRST
    memory_context = []

    if "name" in memory_store["profile"]:
        memory_context.append({
            "role": "system",
            "content": f"The user's name is {memory_store['profile']['name']}."
        })

    for fact in memory_store["facts"]:
        memory_context.append({
            "role": "system",
            "content": f"Remember this about the user: {fact}"
        })

    #  Build messages (WITH memory)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *memory_context,
        {"role": "user", "content": user_input}
    ]
    # Call model
    response = client.chat.completions.create(
        model="xiaomi/mimo-v2-flash:free",
        messages=messages,
        temperature=0.5,
        max_tokens=400 if wants_detail(user_input) else 90
    )

    #  EXTRACT + RETURN (THIS WAS MISSING)
    reply = response.choices[0].message.content.strip()

    print("[JARVIS] Response received.", flush=True)
    return reply
    


# ================== MAIN LOOP ==================
print("\nJARVIS online. Type 'exit' to shut down.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("JARVIS: Shutting down. Goodbye, Sir.")
        break

    reply = jarvis_reply(user_input)
    speak_any(reply)

    print("JARVIS:", reply)



#====================================


#=====================

