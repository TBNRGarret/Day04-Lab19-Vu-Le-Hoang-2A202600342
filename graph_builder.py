import networkx as nx
import matplotlib.pyplot as plt
import pickle

GRAPH_FILE = "knowledge_graph.pkl"


def build_graph(triples: list[dict]) -> nx.DiGraph:
    """Tạo directed graph từ list triple."""
    G = nx.DiGraph()
    for t in triples:
        subj = t["subject"]
        rel  = t["relation"]
        obj  = t["object"]
        G.add_node(subj)
        G.add_node(obj)
        G.add_edge(subj, obj, relation=rel)
    print(f"  → Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


def save_graph(G: nx.DiGraph, path: str = GRAPH_FILE):
    with open(path, "wb") as f:
        pickle.dump(G, f)
    print(f"  → Đã lưu graph tại {path}")


def load_graph(path: str = GRAPH_FILE) -> nx.DiGraph:
    with open(path, "rb") as f:
        return pickle.load(f)


def visualize_graph(G: nx.DiGraph, output_file: str = "graph.png"):
    """Vẽ đồ thị và lưu ảnh."""
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42, k=2)

    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="skyblue", alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

    edge_labels = nx.get_edge_attributes(G, "relation")
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, label_pos=0.3)

    plt.title("Knowledge Graph - Tech Companies", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"  → Đã lưu ảnh đồ thị: {output_file}")
    plt.close()
