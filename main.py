"""
Lab Day 19 - GraphRAG Pipeline
Cách chạy: python main.py
Yêu cầu: OPENAI_API_KEY trong môi trường
"""

import os
import json
from corpus import CORPUS
from extractor import extract_all_triples
from graph_builder import build_graph, save_graph, load_graph, visualize_graph
from querier import graph_rag_answer
from flat_rag import FlatRAG

TRIPLES_FILE = "triples.json"
GRAPH_FILE = "knowledge_graph.pkl"

# ──────────────────────────────────────────
# 5 câu hỏi benchmark (multi-hop)
# ──────────────────────────────────────────
QUESTIONS = [
    "Sam Altman từng làm ở đâu trước khi gắn liền với OpenAI?",
    "Công ty nào đầu tư vào OpenAI và họ có hợp tác gì?",
    "Dario Amodei làm gì tại OpenAI trước khi rời đi?",
    "Elon Musk liên quan đến những công ty nào?",
    "Alphabet được thành lập khi nào và liên quan đến công ty nào?",
]


def step1_indexing():
    """Trích xuất triple và lưu vào file để tránh gọi API nhiều lần."""
    if os.path.exists(TRIPLES_FILE):
        print("[SKIP] Triples đã tồn tại, load từ file.")
        with open(TRIPLES_FILE) as f:
            return json.load(f)

    print("\n=== BƯỚC 1: TRÍCH XUẤT TRIPLE ===")
    triples = extract_all_triples(CORPUS)
    with open(TRIPLES_FILE, "w", encoding="utf-8") as f:
        json.dump(triples, f, ensure_ascii=False, indent=2)
    print(f"  → Đã lưu {len(triples)} triples vào {TRIPLES_FILE}")
    return triples


def step2_build_graph(triples):
    """Xây đồ thị và lưu ảnh."""
    if os.path.exists(GRAPH_FILE):
        print("\n[SKIP] Graph đã tồn tại, load từ file.")
        return load_graph(GRAPH_FILE)

    print("\n=== BƯỚC 2: XÂY DỰNG ĐỒ THỊ ===")
    G = build_graph(triples)
    save_graph(G, GRAPH_FILE)
    visualize_graph(G, "graph.png")
    return G


def step3_query(G):
    """Chạy benchmark so sánh GraphRAG vs FlatRAG."""
    print("\n=== BƯỚC 3 & 4: SO SÁNH GraphRAG vs Flat RAG ===")
    flat = FlatRAG(CORPUS)

    results = []
    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n--- Câu {i}: {q}")
        flat_ans = flat.answer(q)
        graph_ans = graph_rag_answer(G, q)
        print(f"  [Flat RAG]  : {flat_ans}")
        print(f"  [GraphRAG]  : {graph_ans}")
        results.append({
            "question": q,
            "flat_rag": flat_ans,
            "graph_rag": graph_ans,
        })

    # Lưu kết quả
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n  → Kết quả đã lưu vào results.json")


def main():
    triples = step1_indexing()
    G = step2_build_graph(triples)
    step3_query(G)
    print("\n✅ Lab hoàn thành!")


if __name__ == "__main__":
    main()
