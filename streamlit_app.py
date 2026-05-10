import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="KEHNDE", page_icon="🇨🇮")
st.title("🇨🇮 KEHNDE - CP1 a Terminale")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

niveau = st.selectbox("Niveau :", ["CP1","CP2","CE1","CE2","CM1","CM2","6eme","5eme","4eme","3eme","2nde","1ere","Terminale"])

prompt = f"Tu es KEHNDE, prof ivoirien niveau {niveau}. Dechiffre l ecriture meme raturee. Si illisible ecris [illisible]. Note sur 10 pour CP1-CE2, sur 20 pour autres. Donne: Note, Points forts, A corriger, Conseil."

photo = st.file_uploader("Photo de la copie", type=["jpg","png","jpeg"])

if photo:
    image = Image.open(photo)
    st.image(image)
    if st.button("Corriger"):
        response = model.generate_content([prompt, image])
        st.write(response.text)
