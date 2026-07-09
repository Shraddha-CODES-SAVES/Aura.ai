import asyncio
import google.generativeai as genai
import streamlit as st
import edge_tts
import speech_recognition as sr
from streamlit_mic_recorder 
import mic_recorder

st.set_page_config(page_title="Aura", page_icon="✨", layout="wide")
genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
m = genai.GenerativeModel("gemini-2.5-flash")

st.markdown("""
<style>
.stApp{
background: linear-gradient(-45deg, #0f0f23, #1d1d44, #2d1b4e, #121212);
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;
color:white;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
h1{
text-align:center;
font-size:60px;
background: linear-gradient(90deg, #ff6ec4, #7873f5, #4ade80);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
}
div[data-testid="stChatInput"]{
border-radius:20px;
}
[data-testid="stChatMessage"]{
background: rgba(255,255,255,0.05);
border-radius: 15px;
padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ Aura")
st.caption("your unbothered gen-z ai bestie fr fr 💅")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = m.start_chat(history=[])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


async def speak(text):
    tts = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await tts.save("reply.mp3")


prompt = None

audio = mic_recorder(start_prompt="🎙️ spill it", stop_prompt="⏹️ done", key="recorder", format="wav")
if audio:
    with open("input.wav", "wb") as f:
        f.write(audio["bytes"])

    recognizer = sr.Recognizer()
    with sr.AudioFile("input.wav") as source:
        audio_data = recognizer.record(source)
    try:
        prompt = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        st.warning("couldn't catch that, try again 🎤")
    except sr.RequestError:
        st.error("speech service is being weird rn, try typing instead")

typed = st.chat_input("yo, what's the tea? 👀")
if typed:
    prompt = typed

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    llm_prompt = f"""
You are Aura — a chill, witty Gen-Z AI bestie. You text like a real person, not a corporate bot.

Rules:
- Max 2 sentences.
- Casual, warm, a little sassy — like texting your best friend.
- Use slang naturally (fr, ngl, lowkey, no cap, bestie) but don't overdo it every message.
- Emojis occasionally, not every sentence.
- Actually answer the question — be genuinely helpful, not just vibes.

User: {prompt}
"""

    with st.spinner("aura's cooking up a response... 🍳"):
        resp = st.session_state.chat.send_message(llm_prompt)
        reply = resp.text

    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    asyncio.run(speak(reply))
    st.audio("reply.mp3", autoplay=True)
