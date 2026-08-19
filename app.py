import streamlit as st
from gtts import gTTS
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

st.title("Free AI Video Generator 🎬")

text_input = st.text_area("Yahan apna text ya script likhein:")

if st.button("Video Create Karein"):
    if text_input:
        st.info("1. Voiceover generate ho raha hai...")
        
        # Text to Speech
        tts = gTTS(text=text_input, lang='hi')
        tts.save("audio.mp3")
        
        audio = AudioFileClip("audio.mp3")
        duration = audio.duration

        st.info("2. Free Background Video download ho raha hai...")
        
        # Free Stock Video Download
        video_url = "https://assets.mixkit.co/videos/preview/mixkit-chart-on-a-screen-43223-large.mp4"
        video_data = requests.get(video_url).content
        with open("bg.mp4", "wb") as f:
            f.write(video_data)

        st.info("3. Audio aur Video ko merge kiya ja raha hai...")
        
        # Merge Audio & Video
        video = VideoFileClip("bg.mp4").subclip(0, min(duration, 30))
        final_video = video.set_audio(audio)
        final_video.write_videofile("output.mp4", fps=24, codec="libx264")

        st.success("Video Ready hai!")
        st.video("output.mp4")
    else:
        st.warning("Kripya pehle script likhein.")
