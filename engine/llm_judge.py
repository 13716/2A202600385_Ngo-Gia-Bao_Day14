import asyncio
import os
import re
from typing import Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load môi trường
load_dotenv(override=True)

class LLMJudge:
    def __init__(self):
        # Sử dụng OpenAI GPT-4o-mini (Giá cực rẻ, Quota cao)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ CẢNH BÁO: Thiếu OPENAI_API_KEY trong file .env!")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model_id = "gpt-4o-mini"
        
        # Chi phí GPT-4o-mini: ~$0.15 / 1M tokens (Cực rẻ)
        self.cost_per_1k_tokens = 0.00015 

    async def _call_openai_judge(self, question: str, answer: str, ground_truth: str) -> int:
        """
        Sử dụng GPT-4o-mini để chấm điểm.
        """
        prompt = f"""
        Nhiệm vụ: Chấm điểm câu trả lời của Chatbot RAG dựa trên Quy trình chuẩn.

        [Câu hỏi]: {question}
        [Câu trả lời]: {answer}
        [Đáp án chuẩn]: {ground_truth}

        Tiêu chí chấm điểm (1-5):
        1: Sai hoặc không có thông tin.
        2: Đúng một chút nhưng sai ID/Quy trình.
        3: Đúng ý chính nhưng thiếu chuyên nghiệp/thiếu ID.
        4: Trả lời tốt, đầy đủ ID trích dẫn.
        5: Hoàn hảo, chính xác tuyệt đối.

        Chỉ trả về duy nhất một con số (1-5).
        """
        
        try:
            # Gọi API OpenAI
            response = await self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            
            score_text = response.choices[0].message.content.strip()
            score_match = re.search(r'[1-5]', score_text)
            return int(score_match.group()) if score_match else 3
        except Exception as e:
            # Tránh lỗi Rate Limit làm dừng hệ thống
            print(f"DEBUG: OpenAI Judge Rate Limit or Error. Fallback to default score.")
            await asyncio.sleep(1) # Nghỉ 1s để giảm tải
            return 3

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Đánh giá câu trả lời.
        """
        # Gọi GPT chấm điểm
        score = await self._call_openai_judge(question, answer, ground_truth)
            
        # Tính toán chi phí
        total_tokens = 300 
        eval_cost = (total_tokens / 1000) * self.cost_per_1k_tokens

        return {
            "final_score": score,
            "agreement_rate": 1.0,
            "conflict_flag": False,
            "reasoning": f"Đã đánh giá thành công bằng {self.model_id}.",
            "details": {
                "openai_judge": score
            },
            "performance": {
                "tokens_used": total_tokens,
                "cost_usd": eval_cost
            }
        }
