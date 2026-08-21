import os
import json
from tavily import TavilyClient

def load_local_knowledge():
    """Memuat database lokal LKY."""
    path = "data/lky_knowledge.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def retrieve_lky_context(query: str) -> str:
    """Mencari konteks relevan dari database lokal dan internet (Tavily)."""
    knowledge_base = load_local_knowledge()
    
    # 1. Pencarian sederhana di knowledge base lokal berdasarkan kata kunci topik
    matched_texts = []
    query_lower = query.lower()
    for item in knowledge_base:
        if any(keyword in query_lower for keyword in item["topic"].split()):
            matched_texts.append(item["content"])
            
    # Jika tidak ada yang cocok secara spesifik, ambil semua prinsip dasar
    if not matched_texts:
        matched_texts = [item["content"] for item in knowledge_base]
        
    local_context = "\n".join(matched_texts)
    
    # 2. Opsional: Tambahkan Tavily Search jika pertanyaan menyangkut konteks modern/global kontemporer
    tavily_key = os.getenv("TAVILY_API_KEY")
    web_context = ""
    if tavily_key and len(query) > 5:
        try:
            client = TavilyClient(api_key=tavily_key)
            response = client.search(query=f"Lee Kuan Yew perspective on {query}", search_depth="basic", max_results=2)
            web_context = "\n".join([res['content'] for res in response.get('results', [])])
        except Exception:
            pass # Lanjutkan jika web search gagal
            
    combined_context = f"Historical Doctrines:\n{local_context}\n\nModern Context References:\n{web_context}"
    return combined_context