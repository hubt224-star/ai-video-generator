import streamlit as st
from gtts import gTTS
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

st.title("Free AI Video Generator 🎬")

text_input = st.text_area("Yahan apna text ya script likhein:")

if st.button("Video Create Karein"):
    if text_input:
        with st.spinner("Voiceover aur Video generate ho raha hai..."):
            # 1. Audio generate karein
            tts = gTTS(text=text_input, lang='hi')
            audio_path = "audio.mp3"
            tts.save(audio_path)
            audio_clip = AudioFileClip(audio_path)

            # 2. Background Video download karein
            video_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/freeheadpose.mp4"
            response = requests.get(video_url)
            with open("bg.mp4", "wb") as f:
                f.write(response.content)

            # 3. Audio & Video Sync Karein
            video_clip = VideoFileClip("bg.mp4")
            
            # Agar audio lamba hai toh video loop chalegi
            if audio_clip.duration > video_clip.duration:
                final_clip = video_clip.loop(duration=audio_clip.duration)
            else:
                final_clip = video_clip.subclip(0, audio_clip.duration)

            final_clip = final_clip.set_audio(audio_clip)

            # 4. Save & Render Video
            output_path = "final_video.mp4"
            final_clip.write_videofile(
                output_path, 
                fps=24, 
                codec='libx264', 
                audio_codec='aac',
                preset='ultrafast'
            )

        st.success("Aapka AI Video Ready hai!")
        st.video(output_path)
    else:
        st.warning("Kripya pehle text likhein.")
