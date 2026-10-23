import speech_recognition as sr
import pyttsx3
import datetime
import os
import pywhatkit
import google.generativeai as genai

# ==========================================
# 1. إعداد العقل الذكي (Gemini AI Brain)
# ==========================================
# ملحوظة: ضع مفتاح الـ API الخاص بك في متغيرات البيئة على جهازك أو مكان الكلمة بالأسفل عند التشغيل المحلي فقط
API_KEY = os.getenv("GEMINI_API_KEY", "PUT_YOUR_API_KEY_HERE")
genai.configure(api_key=API_KEY)

# إعطاء جارفيس شخصية المساعد الذكي الخاص بـ توني ستارك
system_instruction = (
    "You are J.A.R.V.I.S, an advanced, witty, and highly intelligent AI assistant. "
    "Address the user respectfully as 'Sir' (or 'يا فندم' in Arabic). "
    "Keep your spoken responses concise, insightful, and natural. "
    "Provide well-reasoned opinions when asked to discuss any engineering, scientific, or general topic."
)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
chat_session = model.start_chat(history=[])

# ==========================================
# 2. إعداد الصوت والسمع (Voice & Ears)
# ==========================================
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

def speak(text):
    # تنظيف النص من رموز الماركداون عشان النطق يكون سليم
    clean_text = text.replace("*", "").replace("#", "")
    print(f"\nJarvis: {clean_text}")
    engine.say(clean_text)
    engine.runAndWait()

def listen(lang='en-GB'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("[Recognizing...]")
        query = recognizer.recognize_google(audio, language=lang)
        print(f"You: {query}")
        return query.lower()
    except Exception:
        return "none"

# ==========================================
# 3. وظيفة النقاش الذكي وإبداء الرأي
# ==========================================
def ask_jarvis_brain(prompt):
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return "Sir, I am unable to connect to the neural network right now. Please check the API key."

# ==========================================
# 4. الحلقة الرئيسية (التحكم + النقاش + الاتصالات)
# ==========================================
def run_jarvis():
    speak("All systems operational. Jarvis v2.0 with AI Brain is online. How may I assist you today, sir?")
    
    while True:
        query = listen()
        if query == "none":
            continue

        # --- 1. أوامر التحكم في اللاب توب (OS Control) ---
        if 'open notepad' in query:
            speak("Opening Notepad, sir.")
            os.system("notepad.exe")
            
        elif 'open calculator' in query:
            speak("Launching calculator.")
            os.system("calc.exe")

        elif 'take screenshot' in query:
            import pyautogui
            speak("Capturing screen now, sir.")
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            speak("Screenshot saved successfully.")

        elif 'shutdown laptop' in query:
            speak("Initiating system shutdown in 10 seconds.")
            os.system("shutdown /s /t 10")

        # --- 2. أوامر إرسال رسائل واتساب فورية ---
        elif 'send whatsapp message' in query:
            speak("Sending the scheduled WhatsApp message now, sir.")
            # يفتح واتساب ويب ويرسل الرسالة فوراً
            pywhatkit.sendwhatmsg_instantly("+201000000000", "Hello, this is an automated message from Jarvis.", 15, True, 3)

        # --- 3. أوامر البحث واليوتيوب ---
        elif 'search for' in query:
            search_term = query.replace('search for', '').strip()
            speak(f"Searching the entire web for {search_term}")
            pywhatkit.search(search_term)

        elif 'play' in query:
            song = query.replace('play', '').strip()
            speak(f"Playing {song} on YouTube, sir.")
            pywhatkit.playonyt(song)

        # --- 4. إيقاف النظام ---
        elif 'go to sleep' in query or 'exit' in query:
            speak("Powering down to standby mode. Have a productive day, sir.")
            break

        # --- 5. النقاش المفتوح وإبداء الرأي (أي سؤال آخر يذهب للعقل الذكي) ---
        else:
            ai_reply = ask_jarvis_brain(query)
            speak(ai_reply)

if __name__ == "__main__":
    run_jarvis()
from dotenv import load_dotenv
load_dotenv()  # هذا السطر يقرأ ملف .env السري من جهازك تلقائياً
