import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak_any(reply):
    try:
        text = str(reply)
        if text.strip():
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[0].id)
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)
