import streamlit as st
from PIL import Image
import base64
import requests

st.set_page_config(page_title="KÉHNDÉ Correcteur", layout="wide")
st.title("KÉHNDÉ Correcteur 📝")
st.subheader("Corrige tes copies de Français & Sciences en 30 secondes")

with st.sidebar:
    st.header("Paramètres copie")
    matiere = st.selectbox("Matière", ["Français - Dissertation", "Français - Commentaire", "SVT", "Physique-Chimie"])
    classe = st.selectbox("Classe", ["3ème", "Terminale A", "Terminale D", "Terminale C"])

uploaded_file = st.file_uploader("Photo de ta copie", type=['jpg','jpeg','png'])

if uploaded_file and st.button("Corriger avec KÉHNDÉ 🔍", type="primary"):
    with st.spinner('KÉHNDÉ lit ta copie...'):
        img = Image.open(uploaded_file)
        st.image(img, caption="Copie envoyée", width=300)
        
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        img_bytes = uploaded_file.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        prompt = f"""
        Tu es KÉHNDÉ, correcteur officiel MENET Côte d'Ivoire. 
        Matière: {matiere}, Classe: {classe}.
        
        Tâche:
        1. Lis cette copie manuscrite d'élève
        2. Note sur 20 selon le barème officiel ivoirien
        3. Liste 3 fautes principales avec explication
        4. Donne 1 conseil précis pour gagner +2 points
        5. Sois bienveillant mais strict comme un vrai prof
        
        Format réponse:
        **Note : X/20**
        **Points forts :**...
        **3 Fautes à corriger :**
        1....
        2.... 
        3....
        **Conseil KÉHNDÉ pour +2 pts :**...
        """
        
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1500,
            "messages": [{
                "role": "user", 
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_base64}},
                    {"type": "text", "text": prompt}
                ]
            }]
        }
        
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()['content'][0]['text']
            st.success("Correction terminée!")
            st.markdown(result)
            st.divider()
            st.warning("**Version Gratuite : 1 correction/jour**")
            st.markdown("**KÉHNDÉ Illimité : 2000 FCFA/mois** → Corrections illimitées")
        else:
            st.error("Erreur KÉHNDÉ. Vérifie ta clé API.")
