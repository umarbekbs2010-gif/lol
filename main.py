import datetime
import os
import subprocess
import webbrowser

# Ixtiyoriy ovozli modullar (o'rnatilmagan bo'lsa ham kod ishlayveradi)
try:
    import pyttsx3
    HAS_TTS = True
except ImportError:
    HAS_TTS = False

try:
    import speech_recognition as sr
    HAS_STT = True
except ImportError:
    HAS_STT = False


class Jarvis:
    def __init__(self, voice_enabled: bool = False):
        self.name = "JARVIS"
        self.voice_enabled = voice_enabled and HAS_TTS
        self.engine = None

        if self.voice_enabled:
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 175)

    def speak(self, text: str):
        print(f"{self.name}: {text}")
        if self.voice_enabled and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen_voice(self) -> str:
        if not HAS_STT:
            self.speak("SpeechRecognition kutubxonasi o'rnatilmagan. Matn kiriting.")
            return input("Siz: ").strip().lower()

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Tinglayapman...")
            recognizer.pause_threshold = 0.8
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="uz-UZ")
            print(f"Siz (ovoz): {command}")
            return command.lower().strip()
        except Exception:
            self.speak("Ovozni aniqlab bo'lmadi, qaytadan urining.")
            return ""

    def get_command(self, use_microphone: bool = False) -> str:
        if use_microphone:
            return self.listen_voice()
        return input("Siz: ").strip().lower()

    def handle_command(self, cmd: str) -> bool:
        if not cmd:
            return True

        if any(word in cmd for word in ["chiqish", "xayr", "to'xta", "exit", "quit"]):
            self.speak("Xayr, janob. Kerak bo'lsa yana chaqiring.")
            return False

        elif any(word in cmd for word in ["salom", "assalomu alaykum", "hello", "hi"]):
            self.speak("Assalomu alaykum! Bugun sizga qanday yordam bera olaman?")

        elif "soat" in cmd or "vaqt" in cmd:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"Hozirgi vaqt: {now}")

        elif "sana" in cmd or "bugun" in cmd:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            self.speak(f"Bugungi sana: {today}")

        elif "google" in cmd or "qidir" in cmd:
            query = cmd.replace("google", "").replace("qidir", "").strip()
            if query:
                url = f"https://www.google.com/search?q={query}"
                self.speak(f"Google'da '{query}' bo'yicha qidiryapman.")
                webbrowser.open(url)
            else:
                self.speak("Google saytini ochyapman.")
                webbrowser.open("https://www.google.com")

        elif "youtube" in cmd:
            self.speak("YouTube ochilmoqda.")
            webbrowser.open("https://www.youtube.com")

        elif "kalkulyator" in cmd or "hisobla" in cmd:
            expr = cmd.replace("kalkulyator", "").replace("hisobla", "").strip()
            if expr:
                try:
                    # Faqat matematik ifodalarni xavfsiz hisoblash
                    allowed = set("0123456789+-*/(). ")
                    if set(expr) <= allowed:
                        result = eval(expr)
                        self.speak(f"Natija: {result}")
                    else:
                        self.speak("Noto'g'ri matematik ifoda.")
                except Exception:
                    self.speak("Hisoblashda xatolik yuz berdi.")
            else:
                self.speak("Kalkulyator ishga tushirilmoqda.")
                if os.name == "nt":
                    subprocess.Popen("calc.exe")

        elif "yordam" in cmd or "buyruqlar" in cmd:
            self.speak(
                "Buyruqlar: 'soat', 'sana', 'google [so'z]', 'youtube', "
                "'hisobla [ifoda]', 'chiqish'."
            )

        else:
            self.speak(
                "Bu buyruqni hali o'rganmaganman. 'yordam' deb yozing yoki "
                "boshqa buyruq bering."
            )

        return True


def main():
    # Ovozli rejimni yoqish uchun voice_enabled=True qiling
    jarvis = Jarvis(voice_enabled=False)
    jarvis.speak("JARVIS ishga tushdi. Buyruq kutmoqdaman...")

    running = True
    while running:
        command = jarvis.get_command(use_microphone=False)
        running = jarvis.handle_command(command)


if __name__ == "__main__":
    main()