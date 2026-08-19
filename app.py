import streamlit as st
from gtts import gTTS
import requests
import os
import subprocess
import imageio_ffmpeg

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

        st.info("2. Topic se related Realistic Stock Video download ho raha hai...")
        
        # Default fallback video
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

        bg_video = "bg_input.mp4"
        res = requests.get(video_url, stream=True)
        with open(bg_video, "wb") as f:
            for chunk in res.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

        st.info("3. Audio aur Video merge ho rahe hain...")
        
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        output_video = "final_output.mp4"
        
        # FFmpeg command: loops video and syncs with audio length
        cmd = [
            ffmpeg_exe, "-y",
            "-stream_loop", "-1",
            "-i", bg_video,
            "-i", audio_file,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-pix_fmt", "yuv420p",
            output_video
        ]
        
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if os.path.exists(output_video) and os.path.getsize(output_video) > 0:
            st.success("Aapka Realistic HD Video Ready Hai! 🎉")
            
            with open(output_video, "rb") as v_file:
                video_bytes = v_file.read()
                st.video(video_bytes)
                
            st.download_button(
                label="📥 Download Video (.MP4)",
                data=video_bytes,
                file_name="realistic_ai_video.mp4",
                mime="video/mp4"
            )
        else:
            st.error("Video merge karne mein problem aayi, kripya dubara try karein.")
    else:
        st.warning("Kripya pehle script likhein.")
