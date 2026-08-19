import streamlit as st
from gtts import gTTS
import requests
import base64

st.set_page_config(page_title="Realistic AI Video Generator", layout="centered")

st.title("Realistic AI Video Generator 🎬")

text_input = st.text_area("Yahan apna text ya script likhein:", height=150)

if st.button("Realistic Video Create Karein"):
    if text_input:
        st.info("1. Voiceover (Audio) generate ho raha hai...")
        
        # Audio Creation
        tts = gTTS(text=text_input, lang='hi')
        audio_file = "audio.mp3"
        tts.save(audio_file)

        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()

        st.info("2. Realistic Background Stock Video download aur encode ho raha hai...")
        
        # Working Reliable Stock Video (Trading Chart)
        video_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/freeheadpose.mp4"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(video_url, headers=headers)
        
        # Video Base64 Encoding to bypass browser block
        video_b64 = base64.b64encode(res.content).decode()

        # Embedded HTML5 Video Player
        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 640px; margin: 0 auto; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <video id="bgVideo" style="width: 100%; display: block;" loop muted playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            <audio id="audioPlayer" src="data:audio/mp3;base64,{audio_b64}"></audio>
            
            <div style="position: absolute; bottom: 15px; width: 100%; text-align: center;">
                <button onclick="playVideo()" style="padding: 12px 28px; background: #FF4B4B; color: white; border: none; border-radius: 25px; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.4);">
                    ▶ Play Realistic AI Video
                </button>
            </div>
        </div>

        <script>
            function playVideo() {{
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
        st.success("Aapka AI Video Player Ready Hai! 🎉")
        
        st.download_button(
            label="📥 Download Voiceover (MP3)",
            data=audio_bytes,
            file_name="voiceover.mp3",
            mime="audio/mp3"
        )
    else:
        st.warning("Kripya pehle script likhein.")
