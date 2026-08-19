import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

st.title("Free AI Video Generator 🎬")

text_input = st.text_area("Yahan apna text ya script likhein:")

if st.button("Video Create Karein"):
    if text_input:
        st.info("1. Voiceover generate ho raha hai...")
        tts = gTTS(text=text_input, lang='hi')
        tts.save("audio.mp3")

        st.info("2. Background Image ready ho rahi hai...")
        # Stock Market Chart Image
        img_url = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800"
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img.save("bg_image.png")

        st.success("Aapka AI Audio & Visual Background Ready hai!")
        
        # Display Image & Audio
        st.image("bg_image.png", caption="Stock Trading Background", use_container_width=True)
        st.audio("audio.mp3")
    else:
        st.warning("Kripya pehle text likhein.")
