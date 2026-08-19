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
        
        output_video = "final_output.mp4"
        
        # Proper encoding command for Streamlit compatibility
        cmd = f"ffmpeg -y -i bg.mp4 -i audio.mp3 -c:v libx264 -c:a aac -strict experimental -shortest {output_video}"
        os.system(cmd)

        # File exists and is non-empty check
        if os.path.exists(output_video) and os.path.getsize(output_video) > 0:
            st.success("Video Ready hai!")
            with open(output_video, 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)
        else:
            st.error("Video generate nahi ho payi, kripya dubara try karein.")
    else:
        st.warning("Kripya pehle script likhein.")
