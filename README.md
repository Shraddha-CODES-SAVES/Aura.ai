# ✨ Aura — Your Gen-Z AI Bestie

Aura is a voice-and-text AI assistant built with Streamlit and Google's Gemini API. She talks like a real person — casual, witty, a little sassy — and responds through both text and voice.

🔗 **Live app:** https://auraai-o4q2fowxgfmjytxmigrxsf.streamlit.app

## Features

- 💬 **Text chat** with persistent conversation memory
- 🎙️ **Voice input** — speak to Aura using your microphone
- 🔊 **Voice output** — Aura replies out loud using natural-sounding text-to-speech
- 🎨 **Custom themed UI** with a Gen-Z personality and aesthetic background

## Tech Stack

- **Frontend/App:** [Streamlit](https://streamlit.io)
- **AI Model:** Google Gemini (`gemini-2.5-flash`) via `google-generativeai`
- **Speech-to-Text:** `SpeechRecognition` (Google Speech API)
- **Text-to-Speech:** `edge-tts`
- **Mic input:** `streamlit-mic-recorder`

## How It Works

1. User types a message or records their voice
2. Voice input is transcribed to text using SpeechRecognition
3. The text is sent to Gemini with a custom personality prompt
4. Gemini's reply is displayed in the chat and converted to speech
5. The audio response plays automatically

## Running Locally

```bash
git clone https://github.com/Shraddha-CODES-SAVES/Aura.ai.git
cd Aura.ai
pip install -r requirements.txt
