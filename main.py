import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from src.rag_engine import retrieve_lky_context
from src.persona_prompt import LKY_SYSTEM_PROMPT

# Muat environment variables
load_dotenv()

st.set_page_config(
    page_title="What Would Lee Kuan Yew Do? (LKY Chatbot)",
    page_icon="🏛️",
    layout="centered"
)

st.title("🏛️ What Would Lee Kuan Yew Do?")
st.caption("A persona-based AI chatbot trained on Lee Kuan Yew's governance, history, and life philosophy.")

# Validasi API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Error: GROQ_API_KEY tidak ditemukan di file .env!")
    st.stop()

client = Groq(api_key=api_key)

# Inisialisasi riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am here. Ask me about governance, leadership, geopolitics, or how small nations navigate a troubled world. What is on your mind?"}
    ]

# Tampilkan riwayat chat di UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari pengguna
if user_input := st.chat_input("Ask Lee Kuan Yew a question..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Proses RAG & Panggil LLM Groq
    with st.chat_message("assistant"):
        with st.spinner("Reflecting on statecraft and history..."):
            # 1. Ambil konteks RAG
            context = retrieve_lky_context(user_input)
            
            # 2. Susun system prompt dengan injeksi konteks
            formatted_system_prompt = LKY_SYSTEM_PROMPT.format(context=context)
            
            # 3. Siapkan riwayat pesan untuk Groq API
            messages_payload = [{"role": "system", "content": formatted_system_prompt}]
            for m in st.session_state.messages:
                messages_payload.append({"role": m["role"], "content": m["content"]})
                
            try:
                # Panggil model Groq (menggunakan model berkapasitas besar untuk ketajaman penalaran persona)
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages_payload,
                    temperature=0.4,
                    max_tokens=800
                )
                
                reply = response.choices[0].message.content.strip()
                st.markdown(reply)
                
                # Simpan jawaban ke riwayat chat
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
            except Exception as e:
                error_msg = f"Terjadi kesalahan saat menghasilkan respons: {e}"
                st.error(error_msg)