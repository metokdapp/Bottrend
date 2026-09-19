import json
import config
from google import genai


def analyze_payload_with_gemini(data):
    if not config.GEMINI_API_KEY:
        return {"action": "HOLD", "confidence": 0, "reason": "Thiếu GEMINI_API_KEY."}

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    prompt = f"""Bạn là AI phân tích BTC/USDT.
Phân tích dữ liệu sau: {json.dumps(data, ensure_ascii=False)}
Cân nhắc kỹ thuật, phái sinh, tâm lý, Fear & Greed và ETF nếu dữ liệu có sẵn.
Không bịa dữ liệu còn thiếu.
Trả về JSON hợp lệ gồm action (BUY/SELL/HOLD), confidence (0-100), reason bằng tiếng Việt.
"""
    try:
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        return json.loads(response.text)
    except Exception as exc:
        return {"action": "HOLD", "confidence": 0, "reason": f"Gemini lỗi: {exc}"}
