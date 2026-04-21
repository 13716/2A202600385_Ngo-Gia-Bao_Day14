import asyncio
from typing import List, Dict
import os
try:
    from data.knowledge_base import KNOWLEDGE_BASE
except ModuleNotFoundError:
    try:
        from knowledge_base import KNOWLEDGE_BASE
    except ModuleNotFoundError:
        # Fallback cho trường hợp chạy từ root mà data không phải là package
        import sys
        sys.path.append(os.path.join(os.getcwd(), "data"))
        from knowledge_base import KNOWLEDGE_BASE

# Global state để phân biệt V1 và V2 mà không cần sửa main.py
_AGENT_COUNTER = 0

class MainAgent:
    """
    Agent RAG thực thụ thực hiện tìm kiếm trên bộ dữ liệu Access Control SOP.
    """
    def __init__(self, version: str = None):
        global _AGENT_COUNTER
        if version is None:
            _AGENT_COUNTER += 1
            self.version = "v1" if _AGENT_COUNTER % 2 != 0 else "v2"
        else:
            self.version = version
            
        self.name = f"SupportAgent-{self.version}"
        self.kb = KNOWLEDGE_BASE
        print(f"DEBUG: Initialized {self.name}")

    async def query(self, question: str) -> Dict:
        """
        Quy trình RAG thực tế:
        1. Retrieval: Tìm kiếm keyword similarity đơn giản (Mô phỏng Vector Search).
        2. Generation: Giả lập câu trả lời dựa trên context tìm được.
        """
        await asyncio.sleep(0.3) # Giả lập latency
        
        # Logic Retrieval thực tế: Tìm kiếm từ khóa xuất hiện trong chunks
        # Trong thực tế bạn sẽ dùng Embedding + VectorDB ở đây.
        scores = []
        words = set(question.lower().split())
        
        for doc in self.kb:
            doc_words = set(doc["text"].lower().split())
            overlap = len(words.intersection(doc_words))
            scores.append((doc["id"], doc["text"], overlap))
            
        # Sắp xếp theo điểm số giảm dần
        scores.sort(key=lambda x: x[2], reverse=True)
            
        # Logic Retrieval: 
        if self.version == "v2":
            # V2 sử dụng bộ lọc ngưỡng (Threshold Filter)
            # 1. Lấy Top 5 để không bỏ sót
            top_results = scores[:5]
            best_score = top_results[0][2]
            
            # 2. Bộ lọc: Chỉ giữ lại những đoạn có điểm >= 70% so với đoạn tốt nhất
            filtered_results = [res for res in top_results if res[2] >= best_score * 0.7 and res[2] > 0]
            
            retrieved_ids = [res[0] for res in filtered_results]
            contexts = [res[1] for res in filtered_results]
            
            # 3. Tổng hợp thông tin sạch
            source_info = f" (Nguồn: {', '.join(retrieved_ids)})"
            summary = "\n- ".join([c[:150].strip() + "..." for c in contexts])
            answer = f"Dựa trên quy trình SOP{source_info}, các quy định liên quan bao gồm:\n- {summary}\nXin vui lòng thực hiện đúng quy trình trên."
        else:
            # V1 vẫn dùng cơ chế cũ (Dễ bị thiếu hoặc nhiễu)
            top_results = scores[:1]
            retrieved_ids = [res[0] for res in top_results if res[2] > 0]
            contexts = [res[1] for res in top_results if res[2] > 0]
            answer = f"Thông báo: {contexts[0] if contexts else 'Không tìm thấy'}. (Nguồn: {retrieved_ids})"

        return {
            "answer": answer,
            "contexts": contexts,
            "retrieved_ids": retrieved_ids,
            "metadata": {
                "version": self.version,
                "model": "gpt-4o-mini",
                "tokens_used": 250 if self.version == "v2" else 150
            }
        }
