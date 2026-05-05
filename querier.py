import networkx as nx
import openai

client = openai.OpenAI()


def find_entity_in_graph(G: nx.DiGraph, query: str) -> list[str]:
    """Tìm node khớp với từ khóa trong câu hỏi (case-insensitive)."""
    query_lower = query.lower()
    matched = [n for n in G.nodes() if n.lower() in query_lower]
    return matched


def two_hop_subgraph(G: nx.DiGraph, entity: str) -> list[str]:
    """Lấy tất cả triple trong vòng 2-hop từ entity."""
    facts = []

    # 1-hop: các cạnh trực tiếp ra/vào
    for u, v, data in G.edges(data=True):
        if u == entity or v == entity:
            facts.append(f"{u} --[{data['relation']}]--> {v}")

    # 2-hop: neighbors của neighbors
    neighbors_1 = list(G.successors(entity)) + list(G.predecessors(entity))
    for nbr in neighbors_1:
        for u, v, data in G.edges(nbr, data=True):
            fact = f"{u} --[{data['relation']}]--> {v}"
            if fact not in facts:
                facts.append(fact)

    return facts


def graph_rag_answer(G: nx.DiGraph, question: str) -> str:
    """Pipeline hoàn chỉnh: câu hỏi → tìm entity → 2-hop → LLM trả lời."""
    # Bước 1: tìm entity
    entities = find_entity_in_graph(G, question)
    if not entities:
        return "[GraphRAG] Không tìm thấy entity liên quan trong đồ thị."

    # Bước 2: thu thập facts
    all_facts = []
    for ent in entities:
        facts = two_hop_subgraph(G, ent)
        all_facts.extend(facts)
    all_facts = list(set(all_facts))  # dedup

    context = "\n".join(all_facts)

    # Bước 3: LLM tổng hợp
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Bạn là trợ lý thông minh. Dùng các facts sau để trả lời câu hỏi một cách chính xác, ngắn gọn.",
            },
            {
                "role": "user",
                "content": f"Facts:\n{context}\n\nCâu hỏi: {question}",
            },
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
