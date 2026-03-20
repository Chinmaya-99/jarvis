from config import client, SYSTEM_PROMPT
from memory import handle_memory_commands, extract_name, memory_store

def wants_detail(user_input):
    detail_words = ["explain", "why", "how", "detail", "deep", "steps"]
    return any(word in user_input.lower() for word in detail_words)

def jarvis_reply(user_input):
    print("[JARVIS] Thinking...", flush=True)

    # Memory commands
    cmd = handle_memory_commands(user_input)
    if cmd:
        return cmd

    name = extract_name(user_input)
    if name:
        return name

    # Build memory context
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

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *memory_context,
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="xiaomi/mimo-v2-flash:free",
        messages=messages,
        temperature=0.5,
        max_tokens=400 if wants_detail(user_input) else 90
    )

    reply = response.choices[0].message.content.strip()
    return reply
