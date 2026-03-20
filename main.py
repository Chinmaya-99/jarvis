from jarvis import jarvis_reply
from tts import speak_any

print("\nJARVIS online. Type 'exit' to shut down.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("JARVIS: Shutting down. Goodbye, Sir.")
        break

    reply = jarvis_reply(user_input)
    speak_any(reply)

    print("JARVIS:", reply)
