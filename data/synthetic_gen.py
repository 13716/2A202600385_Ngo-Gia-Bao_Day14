import json
import asyncio
import os
from typing import List, Dict
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm.asyncio import tqdm
from openai import AsyncOpenAI
# Load environment variables
load_dotenv(override=True)

try:
    from data.knowledge_base import KNOWLEDGE_BASE
except ModuleNotFoundError:
    from knowledge_base import KNOWLEDGE_BASE

client = AsyncOpenAI()

async def generate_qa_for_chunk(chunk: Dict, num_pairs: int = 5) -> List[Dict]:
    """
    Sử dụng OpenAI API để tạo các test cases.
    """
    prompt = f"""
Bạn là chuyên gia thiết kế dữ liệu QA test cases tiếng Việt. 
Tài liệu cung cấp:
ID: {chunk['id']}
Nội dung: {chunk['text']}

Yêu cầu: Sinh ra chính xác {num_pairs} test cases dựa trên tài liệu này ở định dạng JSON Array hợp lệ.
Cấu trúc mỗi object:
{{
  "question": "câu hỏi",
  "expected_answer": "câu trả lời chuẩn mực cần AI trả lời",
  "context": "{chunk['text']}",
  "ground_truth_context_id": "{chunk['id']}",
  "metadata": {{
     "difficulty": "loại câu hỏi (chọn 1: standard/adversarial/edge_case/Multi-turn)"
  }}
}}

Yêu cầu:
- 3 câu Standard
- 1 câu Adversarial (gài bẫy)
- 1 câu Edge Case (câu hỏi biên)

CHỈ trả về mảng JSON Array, KHÔNG BỌC trong markdown ```json ```. Bắt buộc phải là mảng JSON hợp lệ.
"""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You output strictly valid JSON array without any markdown wrappers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "", 1)
        if content.endswith("```"):
            content = content[:-3]
        
        qa_pairs = json.loads(content.strip())
        return qa_pairs
    except Exception as e:
        print(f"Error generating QA for {chunk['id']}: {e}")
        return []

async def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ LỖI: Chưa cấu hình OPENAI_API_KEY. Vui lòng thêm vào file .env!")
        return
    
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 15 else "***"
    print(f"🔑 Đã đọc được OPENAI_API_KEY từ .env: {masked_key}")
    
    print("🚀 Đang khởi tạo Golden Dataset với 50 Test Cases bằng OpenAI GPT-4o-mini...")
    
    all_qa_pairs = []
    # Khôi phục cơ chế chạy tuần tự + nghỉ nhỏ để phòng xa lỗi Rate Limit của OpenAI Tier-0
    for i, chunk in enumerate(KNOWLEDGE_BASE):
        print(f"Đang xử lý phân đoạn {i+1}/{len(KNOWLEDGE_BASE)}...")
        pairs = await generate_qa_for_chunk(chunk, 5)
        all_qa_pairs.extend(pairs)
        if i < len(KNOWLEDGE_BASE) - 1:
            await asyncio.sleep(2) # Nghỉ hờ 2s để chống Spam API
        
    os.makedirs("data", exist_ok=True)
    with open("data/golden_set.jsonl", "w", encoding="utf-8") as f:
        for pair in all_qa_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")
            
    print(f"\n✅ Đã tạo thành công {len(all_qa_pairs)} test cases!")
    print("📁 Dữ liệu được lưu tại: data/golden_set.jsonl")

if __name__ == "__main__":
    asyncio.run(main())
