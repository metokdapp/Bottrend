import json
import config
from google import genai


def analyze_payload_with_gemini(d):
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    return {
        "market_regime_detected": "BULL_TREND",
        "action": "BUY",
        "confidence": 90,
        "reason": "Test Termux",
    }
