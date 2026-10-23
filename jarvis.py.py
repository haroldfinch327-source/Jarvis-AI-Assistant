import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import pywhatkit

# 1. إعداد محرك الصوت (اللسان)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # صوت رجالي (Jarvis style)
engine.setProperty('rate', 175)            # سرعة الكلام

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. إعداد الميكروفون (الأذن)
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        # يمكنك تغيير اللغة إلى 'ar-EG' للعربية أو 'en-GB' للإنجليزية البريطانية
        query = recognizer.recognize_google(audio, language='en-GB')
        print(f"User: {query}\n")
        return query.lower()
    except Exception:
        return "none"

# 3. العقل وتنفيذ الأوامر (التحكم والبحث والاتصال)
def run_jarvis():
    speak("Systems online. Good day sir, how can I assist you?")
    
    while True:
        query = listen()
        if query == "none":
            continue

        # --- أوامر التحكم في اللاب توب ---
        if 'open notepad' in query:
            speak("Opening Notepad, sir.")
            os.system("notepad.exe")
            
        elif 'open calculator' in query:
            speak("Launching calculator.")
            os.system("calc.exe")

        elif 'shutdown laptop' in query:
            speak("Shutting down the system in 10 seconds.")
            os.system("shutdown /s /t 10")

        # --- أوامر البحث في الإنترنت واليوتيوب ---
        elif 'search for' in query:
            search_term = query.replace('search for', '').strip()
            speak(f"Searching the web for {search_term}")
            pywhatkit.search(search_term)

        elif 'play' in query:
            song = query.replace('play', '').strip()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        # --- أوامر الوقت والمواعيد المبدئية ---
        elif 'time' in query:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"Sir, the current time is {time_now}")

        # --- إيقاف جارفيس ---
        elif 'sleep' in query or 'exit' in query:
            speak("Going to standby mode. Call me when you need me, sir.")
            break

if __name__ == "__main__":
    run_jarvis()