import streamlit as st
from gtts import gTTS
import requests
import os

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

        st.info("2. Background Stock Video download ho raha hai...")
        
        # Working Reliable Stock Video Source
        video_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/freeheadpose.mp4"
        
        response = requests.get(video_url)
        video_path = "bg_video.mp4"
        with open(video_path, "wb") as f:
            f.write(response.content)

        st.success("Aapka Media Ready Hai!")

        # Native Streamlit Native Video & Audio Players
        st.subheader(" Background Video:")
        st.video(video_path)

        st.subheader(" AI Voiceover (Audio):")
        st.audio(audio_path)

        # Download Button
        with open(audio_path, "rb") as f:
            st.download_button(
                label="📥 Download Voiceover MP3",
                data=f,
                file_name="ai_voiceover.mp3",
                mime="audio/mp3"
            )
    else:
        st.warning("Kripya pehle koi text ya script likhein.")
