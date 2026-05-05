# Lab 19: Xây dựng hệ thống GraphRAG với Tech Company Corpus

Báo cáo này tổng hợp kết quả của quá trình xây dựng và đánh giá hệ thống GraphRAG so với hệ thống Flat RAG truyền thống.

## 1. Đánh Giá Benchmark (20 Câu Hỏi)

Bảng dưới đây so sánh kết quả trả lời của hệ thống **Flat RAG** và **GraphRAG** dựa trên cùng một tập dữ liệu *Tech Company Corpus*.

| STT | Câu hỏi | Kết quả Flat RAG | Kết quả GraphRAG | Nhận xét |
|:---:|:---|:---|:---|:---|
| 1 | Sam Altman từng làm ở đâu trước khi gắn liền với OpenAI? | Trước khi gắn liền với OpenAI, Sam Altman từng làm việc tại Y Combinator. | Sam Altman từng làm việc tại Y Combinator trước khi gắn liền với OpenAI. | Cả hai đều trả lời đúng, do câu hỏi khá trực diện. |
| 2 | Công ty nào đầu tư vào OpenAI và họ có hợp tác gì? | Microsoft là công ty đã đầu tư vào OpenAI. Họ hợp tác để tích hợp GPT-4 vào Bing và Office 365. | Microsoft là công ty đầu tư vào OpenAI và họ hợp tác phát triển các sản phẩm như GPT-4, tích hợp vào Bing và Office 365. | Cả hai truy xuất đủ thông tin. |
| 3 | Dario Amodei làm gì tại OpenAI trước khi rời đi? | Dario Amodei từng là VP Research tại OpenAI trước khi thành lập Anthropic. | Dario Amodei từng giữ vị trí Phó Giám đốc Nghiên cứu (VP Research) tại OpenAI trước khi rời đi. | GraphRAG thể hiện mối quan hệ rõ ràng hơn. |
| 4 | Elon Musk liên quan đến những công ty nào? | Elon Musk liên quan đến các công ty sau: Tesla, SpaceX và OpenAI. | Elon Musk liên quan đến các công ty sau: OpenAI, Tesla, và SpaceX. | Tương đương. |
| 5 | Alphabet được thành lập khi nào và liên quan đến công ty nào? | Alphabet được thành lập vào năm 2015 và liên quan đến công ty Google. | Alphabet được thành lập vào năm 2015 và liên quan đến công ty Google. | Tương đương. |
| 6 | Những mô hình ngôn ngữ nào được phát triển bởi các công ty thành lập sau năm 2000? | Nêu đúng Claude (Anthropic, 2021) và LLaMA (Meta, 2004). | [GraphRAG] Không tìm thấy entity liên quan trong đồ thị. | **Flat RAG tốt hơn**. GraphRAG gặp khó khăn trong việc trích xuất entity đại diện từ một câu hỏi chung chung (không có specific entity). |
| 7 | Mark Zuckerberg và Sam Altman là CEO/người sáng lập của những công ty nào và các công ty đó phát triển sản phẩm gì? | Đầy đủ thông tin về Meta, LLaMA, Facebook, Instagram; OpenAI, GPT-4, ChatGPT. | Đầy đủ thông tin về Meta, LLaMA, Facebook, Instagram; OpenAI, GPT-4, ChatGPT. | Tương đương. |
| 8 | Ai là người sáng lập công ty phát triển mô hình Claude và người đó từng có liên hệ gì với công ty phát triển GPT-4? | Dario Amodei và Daniela Amodei; Dario từng làm việc tại OpenAI. | Dario Amodei là người sáng lập Anthropic; từng làm việc tại OpenAI. | Tương đương. |
| 9 | Microsoft có liên quan như thế nào đến công ty do Sam Altman thành lập? | Microsoft đầu tư vào OpenAI, phát triển Azure. | Microsoft có quan hệ đối tác với OpenAI, phát triển Azure mà OpenAI sử dụng. | GraphRAG kết nối logic các mối quan hệ (hợp tác, dùng chung nền tảng) tốt hơn. |
| 10 | Công ty nào phát triển Gemini và công ty mẹ của nó được thành lập vào năm nào? | Google phát triển Gemini, công ty mẹ thành lập năm 1998 (Sai, Google thành lập 1998, Alphabet thành lập 2015). | Google phát triển Gemini, Alphabet thành lập năm 1998 (Sai). | **Cả hai bị ảo giác (hallucination) / nhầm lẫn thông tin** giữa năm thành lập Google và Alphabet. |
| 11 | Elon Musk có vai trò gì với công ty đang hợp tác cùng Microsoft? | Sáng lập OpenAI, rời đi năm 2018. | Sáng lập OpenAI, rời đi năm 2018. | Cả hai hệ thống đều thực hiện multi-hop reasoning (hợp tác cùng Microsoft -> OpenAI -> Elon Musk) rất tốt. |
| 12 | Công ty nào phát triển LLaMA và được thành lập năm nào? | Meta, năm 2004. | Meta, năm 2004. | Tương đương. |
| 13 | Các sản phẩm tích hợp mô hình GPT-4 của Microsoft là gì? | Bing và Office 365. | Bing và Office 365. | Tương đương. |
| 14 | Sam Altman có mối liên hệ nào với Y Combinator và OpenAI? | Làm việc tại Y Combinator, đồng sáng lập/CEO OpenAI. | Làm việc tại Y Combinator, đồng sáng lập/CEO OpenAI. | Tương đương. |
| 15 | Ai là người đồng sáng lập Google cùng với Larry Page? | Sergey Brin. | Sergey Brin. | Tương đương. |
| 16 | Công ty nào trong dữ liệu được thành lập trước năm 2000 và ai là người sáng lập? | Microsoft (1975). Bỏ qua Google (1998). | [GraphRAG] Không tìm thấy entity. | **Flat RAG tốt hơn** nhưng vẫn sót thông tin. GraphRAG thất bại vì không parse được keyword thực thể. |
| 17 | Mô hình GPT-4 do công ty nào phát triển và công ty đó nhận đầu tư từ ai? | OpenAI, nhận đầu tư từ Microsoft. | OpenAI, thành lập bởi Elon Musk và Sam Altman. | **Flat RAG chính xác hơn**. GraphRAG truy xuất sai relation lân cận (lấy người sáng lập thay vì nhà đầu tư). |
| 18 | Dario Amodei và Daniela Amodei đã thành lập công ty nào vào năm 2021? | Anthropic. | Anthropic. | Tương đương. |
| 19 | Mark Zuckerberg thành lập Meta vào năm nào và công ty này phát triển những sản phẩm nào? | Meta (2004), phát triển Facebook, Instagram. Thiếu LLaMA. | Meta (2004), phát triển LLaMA, Facebook, Instagram. | **GraphRAG tốt hơn**, lấy được toàn bộ các node `PRODUCT` liên quan đến `Meta`. |
| 20 | Những công ty nào trong dữ liệu có liên quan đến việc phát triển mô hình ngôn ngữ lớn (LLM)? | Kể ra OpenAI, Anthropic, Meta. | [GraphRAG] Không tìm thấy entity. | **Flat RAG tốt hơn** do tìm kiếm theo ngữ nghĩa thay vì keyword matching khắt khe của GraphRAG. |

### Tổng kết Ưu / Nhược điểm
- **Flat RAG** thể hiện ưu thế vượt trội trong các câu hỏi mang tính **thống kê, tổng hợp** (Ví dụ: "Những công ty nào...", "Các mô hình nào..."). Tìm kiếm vector (Semantic Search) giúp nó gom được các đoạn văn có chung ngữ nghĩa mà không cần người dùng chỉ đích danh 1 thực thể cố định.
- **GraphRAG** hoạt động cực kỳ xuất sắc với các truy vấn **xác định được điểm bắt đầu (Entity)** rõ ràng. Đặc biệt ở câu 19, khả năng duyệt toàn bộ đồ thị lân cận giúp nó trả về câu trả lời **đầy đủ thông tin hơn** (bao gồm cả LLaMA, Facebook, Instagram), trong khi Flat RAG bị sót. Tuy nhiên, GraphRAG rất dễ thất bại nếu bộ trích xuất Node không tìm được Entity trọng tâm trong câu hỏi.

---

## 2. Phân Tích Chi Phí Triển Khai (Cost & Time Analysis)

Quá trình trích xuất đồ thị tri thức (Knowledge Graph) từ văn bản thô tốn kém hơn đáng kể so với chunking & embedding thông thường. Dưới đây là đo đạc thực tế trên `Tech Company Corpus`:

- **Mô hình sử dụng:** OpenAI `gpt-4o-mini`
- **Số lượng triples trích xuất:** 38 triples (sau deduplication).
- **Tổng số tokens tiêu thụ:** `2694` tokens.
- **Tổng thời gian chạy (Execution Time):** `25.5` giây.
- **Chi phí quy đổi:** Với mức giá của `gpt-4o-mini` (~$0.150 / 1M input tokens & $0.600 / 1M output tokens), chi phí cho quá trình Indexing này là rất nhỏ, rơi vào khoảng **~ $0.0008 USD**.

**Nhận xét:** 
Mặc dù chi phí bằng tiền (USD) cho corpus nhỏ này là không đáng kể, nhưng **thời gian xử lý (25.5s cho 10 câu)** lại khá chậm do quá trình trích xuất Triples đòi hỏi mô hình LLM phải tự sinh (generation) lượng lớn output JSON. Khi scale lên hệ thống Production với hàng triệu document, quá trình xây dựng GraphRAG sẽ cần kiến trúc phân tán và tốn kém tài nguyên điện toán lớn hơn rất nhiều so với Flat RAG.
