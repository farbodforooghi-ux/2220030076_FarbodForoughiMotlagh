import os
from typing import Any

from dotenv import load_dotenv


def build_prompt(target: str, ports: list[dict], banners: list[dict]) -> str:
    return f"""
Sen bir siber güvenlik analistisin. Aşağıdaki sonuçlar yalnızca öğrencinin kendi lab ortamındaki hedef makineden alınmıştır.
Hedef IP: {target}

Açık port ve servis sonuçları:
{ports}

Banner grabbing sonuçları:
{banners}

Lütfen Türkçe, anlaşılır ve profesyonel bir güvenlik analizi hazırla.
Şunları mutlaka ekle:
1. Her açık port ve servis için kısa risk değerlendirmesi
2. Banner bilgilerinin güvenlik açısından yorumu
3. Kapatılması veya güncellenmesi gereken servisler için somut öneriler
4. Genel güvenlik özeti
5. Önceliklendirilmiş aksiyon listesi
""".strip()


def analyze_with_gemini(prompt: str) -> str:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError("Missing package. Install requirements with: pip install -r requirements.txt") from exc

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
