import google.generativeai as genai
import os
from dotenv import load_dotenv

# Şifreleri .env dosyasından yükle
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("HATA: .env dosyasında GOOGLE_API_KEY bulunamadı!")
else:
    genai.configure(api_key=api_key)
    
    print("🔍 Senin API Anahtarının İzin Verdiği Modeller:")
    print("-" * 50)
    
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
    except Exception as e:
        print(f"❌ Hata: {e}")