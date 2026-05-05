import json
import openai

client = openai.OpenAI()  # dùng OPENAI_API_KEY từ env

SYSTEM_PROMPT = """Bạn là một hệ thống trích xuất tri thức.
Từ đoạn văn bản, hãy trích xuất các bộ ba (triple) theo dạng JSON.
Mỗi triple gồm: {"subject": "...", "relation": "...", "object": "..."}
Chỉ trả về JSON array, không giải thích thêm.

Ví dụ input: "OpenAI được thành lập bởi Sam Altman vào năm 2015."
Ví dụ output:
[
  {"subject": "OpenAI", "relation": "FOUNDED_BY", "object": "Sam Altman"},
  {"subject": "OpenAI", "relation": "FOUNDED_IN", "object": "2015"}
]
"""

def extract_triples(text: str) -> list[dict]:
    """Gửi 1 đoạn văn → nhận list triple."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # rẻ hơn gpt-4
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()
    # Bóc JSON an toàn
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def extract_all_triples(corpus: list[str]) -> list[dict]:
    """Chạy qua toàn bộ corpus, trả về list triple đã gộp."""
    all_triples = []
    for i, text in enumerate(corpus):
        print(f"  [Extracting] Đoạn {i+1}/{len(corpus)}...")
        triples = extract_triples(text)
        all_triples.extend(triples)
    # Deduplication đơn giản
    seen = set()
    unique = []
    for t in all_triples:
        key = (t["subject"].lower(), t["relation"], t["object"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(t)
    print(f"  → {len(all_triples)} triples → {len(unique)} sau dedup")
    return unique
