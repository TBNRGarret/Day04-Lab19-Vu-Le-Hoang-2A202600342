import json
import openai
import time

client = openai.OpenAI()  

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

def extract_triples(text: str) -> tuple[list[dict], int]:
    """Gửi 1 đoạn văn → nhận list triple và số token đã sử dụng."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens
    # Bóc JSON an toàn
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw), total_tokens


def extract_all_triples(corpus: list[str]) -> tuple[list[dict], int, float]:
    """Chạy qua toàn bộ corpus, trả về list triple đã gộp, tổng token và thời gian chạy."""
    start_time = time.time()
    all_triples = []
    total_tokens_used = 0
    
    for i, text in enumerate(corpus):
        print(f"  [Extracting] Đoạn {i+1}/{len(corpus)}...")
        triples, tokens = extract_triples(text)
        all_triples.extend(triples)
        total_tokens_used += tokens
        
    # Deduplication đơn giản
    seen = set()
    unique = []
    for t in all_triples:
        key = (t["subject"].lower(), t["relation"], t["object"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(t)
            
    execution_time = time.time() - start_time
    print(f"  → {len(all_triples)} triples → {len(unique)} sau dedup")
    print(f"  → Đã sử dụng {total_tokens_used} tokens trong {execution_time:.2f} giây.")
    
    return unique, total_tokens_used, execution_time
