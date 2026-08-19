import streamlit as st
from gtts import gTTS

st.title("Free AI Video Generator 🎬")

# User Input
text_input = st.text_area("Yahan apna text ya script likhein:")

if st.button("Video Create Karein"):
    if text_input:
        st.info("Audio generate ho raha hai...")
        
        # Text to Audio
        tts = gTTS(text=text_input, lang='hi')
        tts.save("audio.mp3")
        
        # Audio Player
        st.audio("audio.mp3")
        st.success("Audio ready hai! Next update mein video rendering active ho jayegi.")
    else:
        st.warning("Kripya pehle kuch text likhein.")
