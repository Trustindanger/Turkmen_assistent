"""
JARVIS Agent - Esasy Programma (Main)
UI we Core Engine-i birleşdirýär
"""

import customtkinter as ctk
import threading
import datetime
from ui_design import JarvisUI
from core_engine import CoreEngine
from config import THEME_COLOR

class JarvisAssistant(JarvisUI):
    def __init__(self):
        super().__init__()
        
        # Core engine-i işe düşürmek
        self.core = CoreEngine()
        
        # UI hadysalary baglamak
        self.trigger_send = self.process_command
        self.trigger_voice = self.start_voice_input
        
        # Status bar täzelemek üçin thread
        self.running = True
        self.update_status_bar()
        
        # Başlangyç salamlaşyk
        self.core.speak("Salam! Men JARVIS. Size nähili kömek edip bilerin?")
    
    def process_command(self, text=None):
        """Buýrugy işlemek"""
        if not text:
            text = self.get_input()
        
        if not text:
            return
        
        # Ekrana çap etmek
        self.add_message("Siz", text)
        self.clear_input()
        self.update_status(status="🔄 İşlenýär...")
        
        # Buýrugy thread-de işlemek (GUI doňmazlygy üçin)
        threading.Thread(target=self._execute_command, args=(text,), daemon=True).start()
    
    def _execute_command(self, text):
        """Esasy buýruk logikasy"""
        text_lower = text.lower()
        response = ""
        
        try:
            # 1. Sesli giriş / toka
            if "toka" in text_lower or "sesli" in text_lower:
                self.core.speak("Diňleýärin, gürleň!")
                voice_text = self.core.listen()
                if voice_text:
                    self.process_command(voice_text)
                else:
                    self.core.speak("Sesi eşitmedim.")
                return
            
            # 2. Hawa maglumaty
            elif "hawa" in text_lower or "howa" in text_lower or "temperatura" in text_lower:
                city = None
                if "aşgabat" in text_lower:
                    city = "Ashgabat"
                elif "mary" in text_lower:
                    city = "Mary"
                elif "türkmenbaşy" in text_lower or "balkan" in text_lower:
                    city = "Turkmenbashi"
                elif "daşoguz" in text_lower:
                    city = "Dashoguz"
                elif "lebap" in text_lower or "türkmenabat" in text_lower:
                    city = "Lebap"
                
                weather_info = self.core.get_weather(city)
                response = weather_info
                self.core.speak(response)
            
            # 3. Google gözleg
            elif "google" in text_lower:
                query = text_lower.replace("google", "").replace("gözle", "").strip()
                if query:
                    self.core.google_search(query)
                    response = f"Google'da '{query}' gözlenýär."
                else:
                    response = "Näme gözlemeli?"
                    self.core.speak(response)
                    return
            
            # 4. YouTube gözleg
            elif "youtube" in text_lower or "ýutub" in text_lower:
                query = text_lower.replace("youtube", "").replace("ýutub", "").replace("gözle", "").strip()
                if query:
                    self.core.youtube_search(query)
                    response = f"YouTube'da '{query}' gözlenýär."
                else:
                    response = "YouTube'da näme gözlemeli?"
                    self.core.speak(response)
                    return
            
            # 5. Programma açmak
            elif "aç" in text_lower or "işjeňleşdir" in text_lower:
                app_map = {
                    "notepad": "notepad",
                    "bloknot": "notepad",
                    "kalkulýator": "kalkulýator",
                    "kaluklýator": "kalkulýator",
                    "terminal": "terminal",
                    "cmd": "cmd",
                    "komanda": "cmd",
                    "paint": "paint"
                }
                
                app_found = None
                for key, value in app_map.items():
                    if key in text_lower:
                        app_found = value
                        break
                
                if app_found:
                    self.core.open_app(app_found)
                    response = f"{app_found} açylýar."
                else:
                    response = "Haýsy programmny açmaly?"
                    self.core.speak(response)
                    return
            
            # 6. Ulgam maglumatlary
            elif "ulgam" in text_lower or "cpu" in text_lower or "ram" in text_lower:
                info = self.core.get_system_info()
                response = f"CPU: {info['cpu']}%, RAM: {info['ram']}%, Disk: {info['disk']}%"
                self.core.speak(response)
            
            # 7. Wagt we sene
            elif "wagt" in text_lower or "sagat" in text_lower:
                now = datetime.datetime.now()
                response = f"Hazirki wagt: {now.strftime('%H:%M:%S')}"
                self.core.speak(response)
            
            elif "sene" in text_lower or "sene" in text_lower or "tarih" in text_lower:
                now = datetime.datetime.now()
                response = f"Bügün: {now.strftime('%d.%m.%Y')}"
                self.core.speak(response)
            
            # 8. Çykmak
            elif "çyk" in text_lower or "gutarnyk" in text_lower or "soňuna ýet" in text_lower:
                response = "Hoş galyn! Size kömek edenime şat."
                self.core.speak(response)
                self.running = False
                self.after(1000, self.quit)
                return
            
            # 9. Akylly jogaplar (default)
            else:
                response = self.core.smart_response(text_lower)
                self.core.speak(response)
            
            # Jogaby ekrana çap etmek
            self.after(0, lambda: self.add_message("JARVIS", response))
            self.after(0, lambda: self.update_status(status="✅ Taýýar"))
            
        except Exception as e:
            error_msg = f"Ýalňyşlyk ýüze çykdy: {str(e)}"
            print(error_msg)
            self.after(0, lambda: self.add_message("JARVIS", error_msg))
            self.after(0, lambda: self.update_status(status="❌ Ýalňyşlyk"))
    
    def start_voice_input(self):
        """Sesli girişi başlatmak"""
        self.set_voice_active(True)
        self.update_status(status="🎤 Diňleýär...")
        
        # Thread-de sesi diňlemek
        threading.Thread(target=self._voice_listener, daemon=True).start()
    
    def _voice_listener(self):
        """Sesi diňläp, netijeni işlemek"""
        try:
            voice_text = self.core.listen()
            
            if voice_text:
                self.after(0, lambda: self.process_command(voice_text))
            else:
                self.after(0, lambda: self.core.speak("Sesi eşitmedim, gaýtadan synanyşyň."))
                self.after(0, lambda: self.update_status(status="⚠️ Sesi eşitmedim"))
        except Exception as e:
            print(f"Ses ýalňyşlygy: {e}")
            self.after(0, lambda: self.core.speak("Mikrofon ýalňyşlygy."))
        finally:
            self.after(0, lambda: self.set_voice_active(False))
            self.after(0, lambda: self.update_status(status="✅ Taýýar"))
    
    def update_status_bar(self):
        """Status bar-y yzygiderli täzelemek"""
        if self.running:
            try:
                info = self.core.get_system_info()
                self.update_status(
                    cpu=info['cpu'],
                    ram=info['ram'],
                    time_str=info['time']
                )
            except:
                pass
            
            # Her 2 sekuntdan täzelemek
            self.after(2000, self.update_status_bar)


if __name__ == "__main__":
    # CustomTkinter tema sazlamalary
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Programmany işe düşürmek
    app = JarvisAssistant()
    app.mainloop()
