import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="KÉHNDÉ Correcteur", page_icon="🇨🇮")
st.title("🇨🇮 KÉHNDÉ - Le Correcteur de 3ème")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

prompt_correcteur = """Tu es KÉHNDÉ, prof de français de 3ème en Côte d'Ivoire. 
Corrige cette copie. Donne:
1. Note /20 stricte selon BEPC
2. 3 fautes principales avec règle
3. 1 conseil pour progresser
Sois direct et bienveillant. 4 phrases max."""

photo = st.file_uploader("📸 Photo de la copie", type=["jpg","png","jpeg"])

if photo:
    image = Image.open(photo)
    st.image(image, width=300)
    if st.button("Corriger avec KÉHNDÉ"):
        with st.spinner("KÉHNDÉ corrige..."):
            response = model.generate_content([prompt_correcteur, image])
            st.success(response.text)
            st.balloons()
