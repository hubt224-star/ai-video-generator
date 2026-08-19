import streamlit as st
from gtts import gTTS
import requests
import base64

st.set_page_config(page_title="AI Video Generator", layout="centered")

st.title("Free AI Video Generator 🎬")

# User Input
text_input = st.text_area("Yahan apna text ya script likhein:", height=150)

if st.button("HD Video Create Karein"):
    if text_input:
        st.info("1. High-Quality Audio generate ho raha hai...")
        
        # Audio Generation
        tts = gTTS(text=text_input, lang='hi')
        tts.save("audio.mp3")

        with open("audio.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()

        st.info("2. Background HD Video sync ho raha hai...")
        
        # Direct Working HD Stock Video Link
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-chart-on-a-screen-43223-large.mp4"

        # HTML5 Video & Audio Player
        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 640px; margin: 0 auto; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <video id="bgVideo" style="width: 100%; display: block;" loop muted playsinline>
                <source src="{video_url}" type="video/mp4">
            </video>
            <audio id="audioPlayer" src="data:audio/mp3;base64,{audio_b64}"></audio>
            
            <div style="position: absolute; bottom: 20px; width: 100%; text-align: center;">
                <button onclick="playHDVideo()" style="padding: 12px 28px; background: #FF4B4B; color: white; border: none; border-radius: 25px; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.4);">
                    ▶ Play HD Video
                </button>
            </div>
        </div>

        <script>
            function playHDVideo() {{
                var video = document.getElementById('bgVideo');
                var audio = document.getElementById('audioPlayer');
                
                video.currentTime = 0;
                audio.currentTime = 0;
                
                video.play();
                audio.play();
                
                audio.onended = function() {{
                    video.pause();
                }};
            }}
        </script>
        """

        st.components.v1.html(html_code, height=420)
        st.success("Aapka HD Video Ready hai!")
        
        # Download Audio Option
        st.download_button(
            label="📥 Download Generated Voiceover (MP3)",
            data=audio_bytes,
            file_name="ai_voiceover.mp3",
            mime="audio/mp3"
        )
    else:
        st.warning("Kripya pehle koi text ya script likhein.")
