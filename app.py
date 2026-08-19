import streamlit as st
from gtts import gTTS
import requests
from io import BytesIO

st.set_page_config(page_title="AI Video Generator", layout="centered")

st.title("Free AI Video Generator 🎬")

text_input = st.text_area("Yahan apna text ya script likhein:", height=150)

if st.button("Video Create Karein"):
    if text_input:
        st.info("1. Voiceover generate ho raha hai...")
        
        # Audio File Save
        tts = gTTS(text=text_input, lang='hi')
        audio_path = "audio.mp3"
        tts.save(audio_path)

        st.info("2. HD Background visual load ho raha hai...")
        
        # Stock Market HD Image
        img_url = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1000"
        response = requests.get(img_url)
        
        st.success("Aapka AI Media Ready Hai!")

        # Display High Quality Background Visual
        st.subheader(" 📈 Background Visual:")
        st.image(response.content, use_container_width=True)

        st.subheader(" 🔊 AI Voiceover (Audio):")
        st.audio(audio_path)

        # Download Voiceover
        with open(audio_path, "rb") as f:
            st.download_button(
                label="📥 Download Voiceover MP3",
                data=f,
                file_name="ai_voiceover.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("Kripya pehle koi text ya script likhein.")
