import streamlit as st
from gtts import gTTS
import requests
import base64

st.set_page_config(page_title="Realistic AI Video Generator", layout="centered")

st.title("Realistic AI Video Generator 🎬")

# Pexels Free API Key
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"  # Yahan apni Pexels API key dalein

text_input = st.text_area("Yahan apna text ya script likhein:", height=150)
search_query = st.text_input("Background Video Search Topic (English):", "stock market chart trading")

if st.button("Realistic HD Video Create Karein"):
    if text_input:
        st.info("1. Voiceover (Audio) generate ho raha hai...")
        
        # Audio Creation
        tts = gTTS(text=text_input, lang='hi')
        audio_file = "audio.mp3"
        tts.save(audio_file)

        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()

        st.info("2. Topic se related Stock Video link fetch ho raha hai...")
        
        # Default fallback working stock video
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-chart-on-a-screen-43223-large.mp4"
        
        # Pexels API Search
        if PEXELS_API_KEY != "YOUR_PEXELS_API_KEY_HERE":
            headers = {"Authorization": PEXELS_API_KEY}
            params = {"query": search_query, "per_page": 1, "orientation": "landscape"}
            res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
            
            if res.status_code == 200 and res.json().get('videos'):
                video_files = res.json()['videos'][0]['video_files']
                for vf in video_files:
                    if vf.get('width') and vf['width'] >= 1280:
                        video_url = vf['link']
                        break

        # Browser-based Video Player
        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 640px; margin: 0 auto; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <video id="bgVideo" style="width: 100%; display: block;" loop muted playsinline crossorigin="anonymous">
                <source src="{video_url}" type="video/mp4">
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
        st.success("Aapka HD AI Video Player Ready Hai! 🎉")
        
        st.download_button(
            label="📥 Download Audio Voiceover (MP3)",
            data=audio_bytes,
            file_name="voiceover.mp3",
            mime="audio/mp3"
        )
    else:
        st.warning("Kripya pehle script likhein.")
