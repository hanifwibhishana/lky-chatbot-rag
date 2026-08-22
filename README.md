# 🏛️ "What Would Lee Kuan Yew Do?" (LKY Persona Chatbot)

An intelligent, persona-based RAG chatbot designed to emulate the governance philosophy, historical perspective, and leadership style of Lee Kuan Yew, the founding father of Modern Singapore. This project is submitted for Section 3 of the 99 Group AI Aptitude Challenge[cite: 2].

---

## 🚀 Project Overview
This application serves as a conversational interface where users can ask questions regarding statecraft, geopolitics, history, leadership, and personal life choices. Instead of responding with generic AI phrasing, the system grounds its answers in a curated historical knowledge base combined with a strict persona prompt, ensuring responses reflect LKY’s trademark pragmatism, blunt realism, and analytical depth.

---

## 🧠 System Architecture & Workflow

```text
[User] ---> Enters Question (e.g., "How to handle corruption?")
              |
              v
[RAG Engine] ---> Searches local knowledge base (LKY quotes & doctrines) 
              |    and queries Tavily Search API for modern context mapping.
              v
[Groq API]   ---> Ingests retrieved context + Persona System Prompt into 
              |    model (openai/gpt-oss-120b) with temperature control.
              v
[Streamlit]  ---> Renders the historical, in-character response in a 
                   chat-style interface with full history memory.