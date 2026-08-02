"""
JARVIS Agent - Esasy Logika (Core Engine)
Ses, Internet, Ulgam we Akylly Jogaplar
"""

import os
import sys
import webbrowser
import subprocess
import threading
import datetime
import requests
import speech_recognition as sr
import pyttsx3
import psutil
from config import VOICE_RATE, VOICE_VOLUME, WEATHER_API_URL, DEFAULT_CITY

class CoreEngine:
    def __init__(self):
        # Ses motoryny gurmak
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', VOICE_RATE)
        self.engine.setProperty('volume', VOICE_VOLUME)
        
        # Türkmen dilinde ses (bar bolsa) ýa-da iňlisçe
        voices = self.engine.getProperty('voices')
        # Ilkinji sesi saýlaýarys (köplenç erkek ses)
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        # Mikrofon we tanama
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Kalibrasiýa (gürültüni aýyrmak)
        with self.microphone as source:
            print("🎤 Mikrofon kalibrirlenýär... (Garaşyň)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def speak(self, text):
        """Teksti sesli okap berýär"""
        print(f"🤖 JARVIS: {text}")
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
    
    def _speak_thread(self, text):
        """Sesi doňmazlyk üçin aýratyn thread-de okaýar"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Ses ýalňyşlygy: {e}")
    
    def listen(self):
        """Mikrofondan sesi diňläp, tekste öwrýär"""
        try:
            with self.microphone as source:
                print("👂 Diňleýärin...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Google ses tanama hyzmaty (iň takyk)
            text = self.recognizer.recognize_google(audio, language='tk-TM')
            print(f"🗣️ Siz: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            self.speak("Internet baglanyşygyny barlaň.")
            return None
        except Exception as e:
            print(f"Ýalňyşlyk: {e}")
            return None
    
    def get_weather(self, city=None):
        """Hawa maglumatyny alýar (Open-Meteo API - mugt)"""
        if city is None:
            city = DEFAULT_CITY
        
        # Şäherleriň koordinatalary (mugt API üçin gerek)
        cities = {
            "ashgabat": {"lat": 37.96, "lon": 58.33},
            "mary": {"lat": 37.59, "lon": 61.83},
            "turkmenbashi": {"lat": 40.02, "lon": 53.00},
            "dashoguz": {"lat": 41.83, "lon": 59.97},
            "lebap": {"lat": 39.07, "lon": 63.58}
        }
        
        coords = cities.get(city.lower(), cities["ashgabat"])
        
        try:
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current_weather": True
            }
            response = requests.get(WEATHER_API_URL, params=params, timeout=5)
            data = response.json()
            
            if "current_weather" in data:
                weather = data["current_weather"]
                temp = weather["temperature"]
                wind = weather["windspeed"]
                code = weather["weathercode"]
                
                # Howa koduny düşündirmek
                status = "Açyk"
                if code > 3:
                    status = "Bulutly"
                if code > 45:
                    status = "Dumanly"
                if code >= 61:
                    status = "Ýagynly"
                if code >= 71:
                    status = "Garly"
                
                return f"{city} şäherinde howa {status}. Temperatura {temp} gradus. Rüzgär tizligi {wind} km/s."
            else:
                return "Hawa maglumatyny almak başartmedi."
        except Exception as e:
            return f"Hawa maglumatynda ýalňyşlyk: {str(e)}"
    
    def google_search(self, query):
        """Google gözleg açýar"""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        self.speak(f"Google'da '{query}' gözlenýär.")
    
    def youtube_search(self, query):
        """YouTube gözleg açýar"""
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        self.speak(f"YouTube'da '{query}' gözlenýär.")
    
    def open_app(self, app_name):
        """Programma açýar (Windows/Linux/Mac)"""
        system = sys.platform
        
        if system == "win32":
            apps = {
                "notepad": "notepad.exe",
                "kalkulýator": "calc.exe",
                "paint": "mspaint.exe",
                "cmd": "cmd.exe"
            }
            app = apps.get(app_name.lower())
            if app:
                subprocess.Popen(app)
                self.speak(f"{app_name} açylýar.")
            else:
                self.speak("Bu programma tapylmady.")
        
        elif system == "darwin":  # Mac
            apps = {
                "notepad": "TextEdit",
                "kalkulýator": "Calculator",
                "terminal": "Terminal"
            }
            app = apps.get(app_name.lower())
            if app:
                subprocess.Popen(["open", "-a", app])
                self.speak(f"{app_name} açylýar.")
        
        elif system == "linux":
            apps = {
                "notepad": "gedit",
                "kalkulýator": "gnome-calculator",
                "terminal": "gnome-terminal"
            }
            app = apps.get(app_name.lower())
            if app:
                subprocess.Popen([app])
                self.speak(f"{app_name} açylýar.")
            else:
                self.speak("Linux'da bu programma başgaça atlandyrylýar.")
    
    def get_system_info(self):
        """Ulgam maglumatlaryny gaýtarýar"""
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        return {
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "date": datetime.datetime.now().strftime("%d.%m.%Y")
        }
    
    def smart_response(self, text):
        """Akylly jogaplar (Gowşak AI)"""
        text = text.lower()
        
        responses = {
            "salam": "Salam! Size nähili kömek edip bilerin?",
            "nähili": "Men gowy, sag boluň! Siz nähili?",
            "kim": "Men JARVIS, siziň şahsy kompýuter agentiňiz.",
            "näme edip": "Men size gözleg edip, programma aÇyp, hawa maglumatyny aýdyp bilerin.",
            "sag bol": "Arzuw etmeýärin! Başga kömek gerekmi?",
            "hoş": "Hoş galyn! Eger kömek gerek bolsa, meni çagyryň.",
            "wagt": f"Hazirki wagt: {datetime.datetime.now().strftime('%H:%M')}",
            "sene": f"Bügün: {datetime.datetime.now().strftime('%d.%m.%Y')}",
            "adyn": "Meniň adym JARVIS. Just A Rather Very Intelligent System.",
            "işle": "Men işjeň we size kömek etmäge taýýar!",
            "ukyla": "Ukulýan... (Şutka! Men ukulamok, men robot!)"
        }
        
        for key, value in responses.items():
            if key in text:
                return value
        
        return "Bu barada maglumatym ýok. Başga soragyňyz barmy?"
