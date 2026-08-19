import streamlit as st
from gtts import gTTS
import requests
import base64

st.title("HD AI Video Generator 🎬")

# Pexels API Key
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY_HERE"  # Yahan apni Pexels API Key dalein

# User Inputs
video_topic = st.text_input("Background Video ka Topic (e.g. trading, nature, business):", "trading")
text_input = st.text_area("Yahan apna text ya script likhein:")

if st.button("HD Video Create Karein"):
    if text_input:
        st.info("1. High-Quality Audio generate ho raha hai...")
        
        # Audio Create
        tts = gTTS(text=text_input, lang='hi')
        tts.save("audio.mp3")

        with open("audio.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()

        st.info("2. Pexels se Full HD Background Video fetch ho raha hai...")
        
        # Fetch HD Video from Pexels
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-chart-on-a-screen-43223-large.mp4" # Default backup
        
        if PEXELS_API_KEY != "YOUR_PEXELS_API_KEY_HERE":
            headers = {"Authorization": PEXELS_API_KEY}
            params = {"query": video_topic, "per_page": 1, "orientation": "landscape"}
            res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
            
            if res.status_code == 200 and res.json().get('videos'):
                video_files = res.json()['videos'][0]['video_files']
                # Pick 1080p/HD link
                for vf in video_files:
                    if vf.get('width') and vf['width'] >= 1280:
                        video_url = vf['link']
                        break

        # Render HTML5 Overlay Video Player
        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 640px; margin: 0 auto; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
            <video id="bgVideo" style="width: 100%; display: block;" loop muted playsinline>
                <source src="{video_url}" type="video/mp4">
            </video>
            <audio id="audioPlayer" src="data:audio/mp3;base64,{audio_b64}"></audio>
            
            <div style="position: absolute; bottom: 20px; width: 100%; text-align: center;">
                <button onclick="playHDVideo()" style="padding: 12px 25px; background: #FF4B4B; color: white; border: none; border-radius: 25px; font-weight: bold; font-size: 16px; cursor: pointer;">
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

        st.components.v1.html(html_code, height=400)
        st.success("High Quality AI Video Player Ready Hai!")
    else:
        st.warning("Kripya pehle script likhein.")
