# BÁO CÁO PHÂN TÍCH LỖI (FAILURE ANALYSIS) - ACCESS CONTROL SOP AGENT

Báo cáo này được trích xuất từ hệ thống **Evaluation Factory** sau khi đánh giá 55 Test Cases trên hai phiên bản Agent_V1 (Cơ bản) và Agent_V2 (Tối ưu). Dưới đây là phân tích các cụm lỗi hệ thống và đề xuất giải pháp.

---

## 🛑 Cụm lỗi 1: Nhiễu ngữ cảnh (Context Noise)
- **Kịch bản:** Trong lần thử nghiệm đầu tiên, phiên bản V2 (lấy Top 3 chunks) có điểm số thấp hơn V1 (chỉ lấy Top 1).
- **Nguyên nhân:** Khi lấy quá nhiều đoạn văn bản liên quan nhưng không có bộ lọc, các thông tin từ các cấp độ truy cập khác nhau (VD: Level 2 và Level 4) bị trộn lẫn, khiến câu trả lời của Agent trở nên mâu thuẫn hoặc quá dài dòng, làm giảm điểm Fairness và Accuracy từ Judge.

### Phân tích 5 Whys:
1. **Why?** Tại sao điểm V2 lại thấp hơn V1 dù có nhiều dữ liệu hơn?
   *Vì câu trả lời chứa các thông tin thừa, không tập trung vào câu hỏi chính.*
2. **Why?** Tại sao lại có thông tin thừa?
   *Do thuật toán RAG lấy ra 3 đoạn văn bản (Top-k=3) và nối chúng lại một cách cơ học.*
3. **Why?** Tại sao các đoạn văn bản đó lại xuất hiện?
   *Vì độ tương đồng từ khóa của các đoạn trong SOP rất cao (đều chứa từ "Access", "Level"), dẫn đến việc lấy nhầm các Section không liên quan.*
4. **Why?** Tại sao hệ thống không biết loại bỏ các đoạn không liên quan?
   *Vì ban đầu hệ thống thiếu một bộ lọc ngưỡng (Similarity Threshold) để loại bỏ những đoạn có độ khớp thấp.*
5. **Why?** Nguyên nhân gốc rễ là gì?
   *Thiết kế Retrieval Pipeline quá thô sơ, chỉ ưu tiên số lượng (Quantity) thay vì chất lượng (Relevance).*
   => **Giải pháp:** Đã triển khai **Threshold Filter** 70% để loại bỏ nhiễu.

---

## 🛑 Cụm lỗi 2: Truy xuất thất bại (Retrieval Misses)
- **Kịch bản:** Hit Rate hiện tại đạt mức **89.1%**, nghĩa là vẫn còn khoảng 6 câu hỏi Agent không tìm thấy đúng đoạn SOP cần thiết.
- **Biểu hiện:** Agent trả lời "Tôi không biết" hoặc trả lời sai hoàn toàn dựa trên một đoạn văn bản không liên quan.

### Phân tích 5 Whys:
1. **Why?** Tại sao Agent không tìm đúng đoạn văn bản cần tìm?
   *Vì câu hỏi sử dụng các thuật ngữ không trùng khớp chính xác với SOP (VD: "Phê duyệt" vs "Approval").*
2. **Why?** Tại sao hệ thống không hiểu được sự tương đồng đó?
   *Do Agent hiện tại đang sử dụng tìm kiếm Keyword Search đơn giản (Simple Overlap Search).*
3. **Why?** Tại sao không dùng Vector Search nâng cao?
   *Vì hệ thống chưa được tích hợp mô hình Embedding chuyên sâu cho tiếng Việt.*
4. **Why?** Tại sao lại quan trọng?
   *Vì trong các bộ Test Cases có nhóm "Adversarial" cố tình dùng từ đồng nghĩa để đánh lừa Agent.*
5. **Why?** Nguyên nhân gốc rễ là gì?
   *Sự thiếu hụt khả năng hiểu ngữ nghĩa (Semantic Understanding) trong khâu Retrieval.*
   => **Giải pháp:** Cần nâng cấp lên **Hybrid Search** (Kết hợp Keyword và Vector Embedding) và sử dụng cơ chế **Contextual Compression**.

---

## 🛑 Cụm lỗi 3: Sự bất đồng giữa các giám khảo (Judge Disagreement)
- **Kịch bản:** Agreement Rate chỉ đạt **62.7%**, chứng tỏ GPT và Gemini/Claude thường xuyên có ý kiến khác nhau về cùng một câu trả lời.
- **Biểu hiện:** Một giám khảo cho 5 điểm (tuyệt vời), giám khảo kia chỉ cho 3 điểm (trung bình).

### Phân tích 5 Whys:
1. **Why?** Tại sao hai AI Judge lại chấm điểm vênh nhau lớn?
   *Do mỗi mô hình có "khẩu vị" đánh giá khác nhau về độ dài của câu trả lời (Conciseness vs Completeness).*
2. **Why?** Tại sao không có tiêu chuẩn chung?
   *Do System Prompt của Judge còn quá chung chung, chưa định nghĩa rõ thế nào là một câu trả lời 5 điểm.*
3. **Why?** Tại sao Prompt lại chung chung?
   *Vì Team tập trung vào việc chạy song song nhiều mô hình thay vì tinh chỉnh Rubric (tiêu chí chấm điểm).*
4. **Why?** Tại sao Rubric lại quan trọng?
   *Nếu không có Rubric chi tiết, kết quả Eval sẽ mang tính chủ quan của từng mô hình LLM.*
5. **Why?** Nguyên nhân gốc rễ là gì?
   *Thiếu một **Evaluation Rubric** chuẩn hóa và cơ chế **Conflict Resolution** tự động để xử lý các ca điểm vênh.*
   => **Giải pháp:** Xây dựng bộ tiêu chí chấm điểm (Rubric) cực kỳ chi tiết gửi kèm vào Prompt của Judge để bắt buộc các mô hình tuân theo.
---
**Nhóm thực hiện:** 04 
Ngô Gia Bảo - 2A202600385
