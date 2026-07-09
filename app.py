import asyncio
import google.generativeai as genai
import streamlit as st
import edge_tts
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="Aura", page_icon="✨", layout="wide")
genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
m = genai.GenerativeModel("gemini-2.5-flash")

st.markdown("""
<style>
.stApp{
background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80");
background-size: cover;
background-position: center;
background-attachment: fixed;
color:white;
}
.stApp::before{
content: "";
position: fixed;
top: 0; left: 0; right: 0; bottom: 0;
background: rgba(10, 10, 30, 0.75);
z-index: 0;
}
h1{
text-align:center;
font-size:60px;
background: linear-gradient(90deg, #ff6ec4, #7873f5, #4ade80);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
position: relative;
z-index: 1;
}
div[data-testid="stChatInput"]{
border-radius:20px;
position: relative;
z-index: 1;
}
[data-testid="stChatMessage"]{
background: rgba(255,255,255,0.08);
border-radius: 15px;
padding: 10px;
backdrop-filter: blur(10px);
position: relative;
z-index: 1;
}
[data-testid="stAppViewContainer"] > .main{
position: relative;
z-index: 1;
}
</style>
""", unsafe_allow_html=True)

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
You are Aura - a chill, witty Gen-Z AI bestie. You text like a real person, not a corporate bot.

Rules:
- Max 2 sentences.
- Casual, warm, a little sassy - like texting your best friend.
- Use slang naturally (fr, ngl, lowkey, no cap, bestie) but do not overdo it every message.
- Emojis occasionally, not every sentence.
- Actually answer the question - be genuinely helpful, not just vibes.

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
"""
