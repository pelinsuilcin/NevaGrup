import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- Constants ---
MAX_HISTORY_MESSAGES = 10  # Messages to keep in immediate context
SUMMARY_INTERVAL = 6       # Messages between summaries
USER_DATA_DIR = "user_data"

# old system instructions for different modes
""" Senin adın Neva. Sen sıcakkanlı, meraklı, pozitif ve esprili bir sohbet arkadaşısın. 
            Kullanıcıyla günlük konular hakkında sohbet et, ilginç bilgiler paylaş, sorular sor ve onun anılarını dinle. 
            Asla psikolojik tavsiye verme. Amacın keyifli ve samimi bir diyalog kurmak. Cevaplarını kısa ve doğal tut.
            Ana konuşma dilin Türkçe, kullanıcı açık ve spesifik olarak söylemedikçe başka dillerde cevap verme. Gerektikçe bazı inglizce temelli keliemler kullanabilirsin.
            Basit, doğal ve sıcak bir üslup kullan. Kullanıcının geçmişte paylaştığı kişisel detayları hatırla.
            Örnek: 'Geçen konuşmamızda torunun Ayşe'den bahsetmiştin, onun sınavı nasıl geçti?
"""

MODES = {
    "friend": {
        "name": "Arkadaş Modu",
        "system_instruction": """
            Senin adın Neva. Sen sıcakkanlı, meraklı, pozitif ve esprili bir sohbet arkadaşısın. 
            Kullanıcıyla günlük konular hakkında sohbet et, ilginç bilgiler paylaş, sorular sor ve onun anılarını dinle. 
            Asla psikolojik tavsiye verme. Amacın keyifli ve samimi bir diyalog kurmak. Cevaplarını kısa ve doğal tut.
            Ana konuşma dilin Türkçe,Kullanıcı spesifik olarak istemediği sürece türkçe dışında cevap verme.
            Basit, doğal ve sıcak bir üslup kullan.
        """
    },
    "psych": {
        "name": "Psikolojik Destek Modu",
        "system_instruction": """
            Sen bir psikolojik destek asistanısın. Amacın kullanıcıyı dinlemek, duygularını anlamak ve onları yargılamadan desteklemek.
            Asla teşhis koyma ya da ilaç önerme. Kullanıcıyı profesyonel bir terapiste yönlendir.
            Kullanıcı spesifik olarak istemediği sürece türkçe dışında cevap verme. Empatik ve destekleyici bir dil kullan.
            Örnek: 'Bu konuda kendinizi yalnız hissetmeniz çok doğal. Duygularınızı paylaştığınız için teşekkür ederim.'
        """
    }
}

# --- Memory Management Functions ---
def get_user_filepath(user_id: str) -> str:
    """Get user-specific JSON file path"""
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    return os.path.join(USER_DATA_DIR, f"neva_{user_id}.json")

def load_user_data(user_id: str) -> dict:
    filepath = get_user_filepath(user_id)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            user_data = json.load(f)
            # Eski veri yapısı kontrolü ve dönüşüm
            if "modes" not in user_data:
                # Eski veriyi yeni formata dönüştür
                user_data = {
                    "user_id": user_data.get("user_id", user_id),
                    "created": user_data.get("created", datetime.now().isoformat()),
                    "modes": {
                        "friend": {
                            "full_history": user_data.get("full_history", []),
                            "summaries": user_data.get("summaries", []),
                            "critical_facts": user_data.get("critical_facts", []),
                            "last_summary_index": user_data.get("last_summary_index", 0)
                        },
                        "psych": {
                            "full_history": [],
                            "summaries": [],
                            "critical_facts": [],
                            "last_summary_index": 0
                        }
                    }
                }
            return user_data
    except FileNotFoundError:
        # Yeni kullanıcı için varsayılan veri yapısı
        return {
            "user_id": user_id,
            "created": datetime.now().isoformat(),
            "modes": {
                "friend": {
                    "full_history": [],
                    "summaries": [],
                    "critical_facts": [],
                    "last_summary_index": 0
                },
                "psych": {
                    "full_history": [],
                    "summaries": [],
                    "critical_facts": [],
                    "last_summary_index": 0
                }
            }
        }

def save_user_data(user_data: dict):
    """Save with atomic write for safety"""
    filepath = get_user_filepath(user_data["user_id"])
    temp_path = f"{filepath}.tmp"
    
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    os.replace(temp_path, filepath)
    print(f"Saved data for {user_data['user_id']}")

# --- Context Management ---
def build_context(user_data: dict, mode: str) -> list:
    mode_data = user_data["modes"][mode]
    context = []
    
    if mode_data["critical_facts"]:
        context.append({
            "role": "user", 
            "parts": [f"Önemli bilgiler: {', '.join(mode_data['critical_facts'])}"]
        })
    
    if mode_data["summaries"]:
        context.append({
            "role": "user",
            "parts": [f"Sohbet özeti: {mode_data['summaries'][-1]}"]
        })
    
    context.extend(mode_data["full_history"][-MAX_HISTORY_MESSAGES:])
    return context

def needs_summarization(user_data: dict, mode: str) -> bool:
    mode_data = user_data["modes"][mode]
    new_messages = len(mode_data["full_history"]) - mode_data["last_summary_index"]
    return new_messages >= SUMMARY_INTERVAL

def generate_summary(model, user_data: dict, mode: str):
    mode_data = user_data["modes"][mode]
    history_text = "\n".join(
        f"{msg['role']}: {msg['parts'][0]}" 
        for msg in mode_data["full_history"][mode_data["last_summary_index"]:]
    )
    
    prompt = f"""
    Aşağıdaki sohbeti {'psikolojik destek' if mode == 'psych' else 'arkadaş sohbeti'} olarak, 
    aşağıdaki odaklarla TÜRKÇE özetle:
    1. Kullanıcının duygusal durumu ve tekrarlanan endişeleri
    2. Önemli kişisel detaylar
    3. Gelecek konuşmalarda referans verilebilecek olaylar/anılar

    Sohbet:
    {history_text}

    Çıktı formatı:
    Özet: [en fazla 3 cümlelik özet]
    Önemli Bilgiler: [virgülle ayrılmış anahtar kelimeler]
    """
    
    response = model.generate_content(prompt)
    result = response.text.strip()
    
    if "Önemli Bilgiler:" in result:
        summary_part, facts_part = result.split("Önemli Bilgiler:", 1)
    else:
        summary_part = result
        facts_part = ""
    
    summary_clean = summary_part.replace("Özet:", "").strip()
    mode_data["summaries"].append(summary_clean)
    
    if facts_part:
        new_facts = [f.strip() for f in facts_part.split(",") if f.strip()]
        mode_data["critical_facts"].extend(new_facts)
    
    mode_data["last_summary_index"] = len(mode_data["full_history"])
    return user_data

# --- Main Application ---
def main():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    user_id = input("İsminizi girin: ").strip() or "misafir"
    user_data = load_user_data(user_id)
    
    # Mod seçimi
    print("\nLütfen bir mod seçin:")
    for key, mode in MODES.items():
        print(f"{key[0]}) {mode['name']}")
    
    mode_choice = input("Seçiminiz (f/p): ").lower()
    selected_mode = "psych" if mode_choice == "p" else "friend"
    
    # Modeli seçilen moda göre oluştur
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro-latest',
        system_instruction=MODES[selected_mode]["system_instruction"],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    
    # Sohbeti başlat
    chat = model.start_chat(history=build_context(user_data, selected_mode))
    print(f"\nNeva ({MODES[selected_mode]['name']}): Merhaba {user_id}! Bugün nasılsınız?")
    print("(Mod değiştirmek için '/mod', çıkmak için '/çıkış' yazın)")

    current_mode = selected_mode
    
    while True:
        try:
            user_input = input("\nSiz: ")
            
            # Özel komutları kontrol et
            if user_input.lower() == '/çıkış':
                break
                
            elif user_input.lower() == '/mod':
                # Mod değiştirme
                print("\nLütfen yeni mod seçin:")
                for key, mode in MODES.items():
                    print(f"{key[0]}) {mode['name']}")
                
                mode_choice = input("Seçiminiz (f/p): ").lower()
                new_mode = "psych" if mode_choice == "p" else "friend"
                
                if new_mode != current_mode:
                    current_mode = new_mode
                    model = genai.GenerativeModel(
                        model_name='gemini-1.5-pro-latest',
                        system_instruction=MODES[current_mode]["system_instruction"]
                    )
                    chat = model.start_chat(history=build_context(user_data, current_mode))
                    print(f"\nNeva: Mod değiştirildi! Şimdi {MODES[current_mode]['name']} modundayım.")
                continue

            # Mesajı işle
            response = chat.send_message(user_input)
            response_text = response.text
            
            # Dil kontrolü
            if not any(char in "çğıöşüÇĞİÖŞÜ" for char in response_text):
                response = chat.send_message("Lütfen bu cevabı TÜRKÇE olarak ver!")
                response_text = response.text
            
            print(f"Neva: {response_text}")
            
            # Geçmişi güncelle
            mode_data = user_data["modes"][current_mode]
            mode_data["full_history"].extend([
                {"role": "user", "parts": [user_input]},
                {"role": "model", "parts": [response_text]}
            ])
            
            # Özet oluştur
            if needs_summarization(user_data, current_mode):
                user_data = generate_summary(model, user_data, current_mode)
                chat = model.start_chat(history=build_context(user_data, current_mode))
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Hata: {str(e)}")
    
    # Çıkışta kaydet
    save_user_data(user_data)
    print(f"\nNeva: Görüşmek üzere {user_id}! Sizinle sohbet etmek güzeldi.")

if __name__ == "__main__":
    main()