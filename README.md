# jarvis
 🚀 A step toward building a real-world AI assistant like JARVIS
AI-powered assistant inspired by JARVIS using Python
# 🤖 JARVIS AI Assistant

## 📌 Overview
JARVIS is an AI-powered personal assistant inspired by the JARVIS system from Iron Man.  
It can understand user input, respond intelligently using AI models, remember user information, and even speak responses using text-to-speech.

---

## 🚀 Features
- 🧠 AI-powered intelligent responses  
- 💾 Persistent memory system (stores user facts)  
- 🗣️ Text-to-speech (TTS) output  
- 🎯 Context-aware conversations  
- ⚡ Dynamic response control (short/detailed answers)  
- 🔐 Secure API key handling using environment variables  

---

## 🛠️ Tech Stack
- **Language:** Python  
- **AI API:** OpenRouter (LLM integration)  
- **Libraries:**  
  - openai  
  - pyttsx3  
  - json, os  

---

## 📂 Project Structure
jarvis/
│── main.py # Entry point
│── jarvis.py # AI logic
│── memory.py # Memory system
│── tts.py # Text-to-speech
│── config.py # API + system prompt
│── memory.json # Stored user memory
│── requirements.txt



---

## ⚙️ How It Works
1. User gives input  
2. Memory system checks stored facts  
3. AI processes input with context  
4. JARVIS generates response  
5. Output is spoken using TTS  

---

## ▶️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis

install the dependencies
pip install -r requirements.txt

set your api key
export OPENROUTER_API_KEY="your_api_key_here"

run the main file
python main.py
