import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="KÉHNDÉ - Correcteur IA", page_icon="🇨🇮", layout="centered")
st.title("🇨🇮 KÉHNDÉ - Le Prof IA du CP1 à la Terminale")
st.caption("Lit même les écritures difficiles. Corrigé selon programme ivoirien.")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

niveau = st.selectbox(
    "📚 Niveau de l'élève :",
    ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème", "2nde", "1ère", "Terminale"],
    index=9
)

type_exo = st.radio(
    "✍️ Type d'exercice :",
    ["Dictée/Copie", "Rédaction", "Grammaire/Conjugaison", "Dissertation/Commentaire"],
    horizontal=True
)

prompt_systeme = f"""Tu es KÉHNDÉ, correcteur expert pour l'école ivoirienne, niveau {niveau}.

RÈGLE #1 - DÉCHIFFRAGE : L'écriture est manuscrite, parfois sale, raturée, mal formée. Fais de ton mieux pour lire. 
Si un mot est totalement illisible, écris [illisible] et déduis avec le contexte. Ne jamais dire "je n'arrive pas à lire".

RÈGLE #2 - CORRECTION ADAPTÉE AU NIVEAU {niveau} :
- CP1-CP2 : Note /10. Vérifie sens des lettres, majuscules. Sois très encourageant. 2 phrases max.
- CE1-CE2 : Note /10. Orthographe de base. 3 phrases max.
- CM1-CM2 : Note /20. Grammaire, conjugaison. Prépare au collège. 4 phrases.
- 6ème-5ème : Note /20. Accords, conjugaison présent/imparfait/passé composé.
- 4ème-3ème : Note /20 stricte BEPC. Phrases complexes, subordonnées. Donne 3 fautes principales + 1 conseil.
- 2nde-1ère-Tle : Note /20 BAC. Corrige méthode dissertation/commentaire. Sois exigeant mais juste.

RÈGLE #3 - FORMAT DE RÉPONSE OBLIGATOIRE :
**Note : X/20** ou **X/10**
**Points forts :** 1 phrase
**À corriger :** 3 fautes max avec la règle simple
**Conseil KÉHNDÉ :** 1 phrase pour progresser

Tu corriges un exercice de type : {type_exo}. Adapte tes commentaires."""

photo = st.file_uploader(
    f"📸 Prends en photo la copie de {niveau} - Même mal écrite, raturée", 
    type=["jpg","png","jpeg"]
)

if photo:
    image = Image.open(photo)
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(image, caption=f"Copie {niveau}", use_column_width=True)
    with col2:
        if st.button(f"🔍 Déchiffrer et Corriger - {niveau}", type="primary", use_container_width=True):
            with st.spinner(f"KÉHNDÉ analyse l'écriture de {niveau}..."):
                try:
                    response = model.generate_content([prompt_systeme, image])
                    st.success("### ✅ Correction KÉHNDÉ")
                    st.markdown(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erreur KÉHNDÉ : Vérifie la clé API dans Secrets Streamlit. Détail: {e}")

st.divider()
st.caption("KÉHNDÉ v2.0 | IA pour tous les élèves ivoiriens | CP1 → Terminale")
