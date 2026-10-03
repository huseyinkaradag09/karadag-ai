import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Karadag AI", page_icon="🤖")

# --- GİZLİ ŞİFRE KORUMASI ---
# İstediğin şifreyi buradaki "1234" yerine yazabilirsin!
dogru_sifre = "3169"

st.sidebar.title("🔐 Güvenlik Paneli")
girilen_sifre = st.sidebar.text_input("Giriş Şifresini Gir:", type="password")

if girilen_sifre != dogru_sifre:
    st.title("🤖 Karadag AI")
    st.warning("⚠️ Bu asistan özel korumalıdır. Devam etmek için lütfen sol menüye doğru şifreyi girin.")
    st.stop()
# ----------------------------

st.title("🤖 Karadag AI")
st.write("Soyadı Karadağ olan yapay zeka asistanın!")

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Google AI Studio API Anahtarını Gir:", type="password")
    if not api_key:
        st.warning("⚠️️ Devam etmek için lütfen sol menüden API anahtarınızı girin.")
        st.stop()

client = genai.Client(api_key=api_key)

model_adi = "gemini-3.8-flash"

sistem_talimati = (
    "Senin adın Karadag AI. Soyadı Karadağ olan, Google'ın altyapısıyla güçlendirilmiş, "
    "samimi ve Türkçe diline hakim bir yapay zeka asistanısın."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Karadag AI'a bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Karadag AI düşünüyor..."):
            try:
                chat = client.chats.create(
                    model=model_adi,
                    config=types.GenerateContentConfig(
                        system_instruction=sistem_talimati,
                        temperature=0.7,
                    )
                )
                response = chat.send_message(prompt)
                yanit_metni = response.text
                st.markdown(yanit_metni)
                st.session_state.messages.append({"role": "assistant", "content": yanit_metni})
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")