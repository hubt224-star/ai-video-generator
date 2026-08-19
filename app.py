import streamlit as st
from gtts import gTTS
import requests
import os

st.title("Free AI Video Generator 🎬")

text_input = st.text_area("Yahan apna text ya script likhein:")

if st.button("Video Create Karein"):
    if text_input:
        st.info("1. Voiceover generate ho raha hai...")
        
        # Audio Create
        tts = gTTS(text=text_input, lang='hi')
        audio_path = "audio.mp3"
        tts.save(audio_path)

        st.info("2. Video download ho rahi hai...")
        
        # Direct Working MP4 Video Link
        video_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/freeheadpose.mp4"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(video_url, headers=headers, stream=True)
        
        with open("bg.mp4", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

        st.info("3. Audio aur Video merge ho raha hai...")
        
        # System FFmpeg Command (Fast & Error-free)
        output_video = "final_output.mp4"
        cmd = f"ffmpeg -y -i bg.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest {output_video}"
        os.system(cmd)

        st.success("Video Ready hai!")
        st.video(output_video)
    else:
        st.warning("Kripya pehle script likhein.")
