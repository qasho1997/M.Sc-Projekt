import streamlit as st
import openai
import os
from RFEM_prompts import process_prompt

# 🔑 API-Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit Setup
st.set_page_config(page_title="RFEM KI-Generator", layout="wide")
st.title("🏗️ RFEM Webservice Generator")

# Eingabe
st.subheader("🧠 Beschreibe dein Modell")
user_prompt = st.text_area("Beispiel: 'Einfeldträger mit 6 m, S235, IPE 300, zwei Auflager, 4 kN/m'", height=150)

# GPT-Code-Generierung
if st.button("💡 GPT-Code generieren"):
    if not user_prompt.strip():
        st.warning("Bitte gib eine Modellbeschreibung ein.")
    else:
        try:
            rfem_code = process_prompt(user_prompt)

            # Entferne Markdown falls vorhanden
            if rfem_code.strip().startswith("```"):
                rfem_code = rfem_code.strip().strip("```python").strip("```")

            st.session_state["rfem_code"] = rfem_code
            st.success("✅ Code erfolgreich generiert.")

        except Exception as e:
            st.error(f"❌ Fehler beim Generieren:\n{e}")

# Code-Anzeige
if "rfem_code" in st.session_state:
    st.subheader("📄 Generierter RFEM-Code")
    st.code(st.session_state["rfem_code"], language="python")

# Ausführung
if st.button("🚀 Modell berechnen"):
    if "rfem_code" in st.session_state:
        try:
            exec(st.session_state["rfem_code"])
            st.success("✅ Modell erfolgreich erstellt und berechnet.")
        except Exception as e:
            st.error(f"❌ Fehler bei der Ausführung:\n\n{e}")
    else:
        st.warning("Bitte zuerst Code generieren.")
