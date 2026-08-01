# -*- coding: utf-8 -*-
"""
JARVIS Stilinde Döwrebap Kompýuter Agent-Assistent
Doly Türkmen dilinde, OOP stilinde, Threading ulanyp ýazylan.
"""

import customtkinter as ctk
import psutil
import pyttsx3
import webbrowser
import os
import threading
import time
import datetime
import re
from typing import Optional

# --- Dizaýn Sazlamalary ---
ctk.set_appearance_mode("Dark")  # Gara tema
ctk.set_default_color_theme("blue")  # Neony gök reňk

class JarvisAssistant:
    def __init__(self):
        # Esasy penjire
        self.root = ctk.CTk()
        self.root.title("JARVIS - Türkmen Kömekçisi")
        self.root.geometry("900x700")
        self.root.configure(fg_color="#0a0a12")  # Örän gara fon
        
        # Ses motoryny sazlamak
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Sözleýiş tizligi
        self.is_speaking = False
        
        # UI komponentlerini döretmek
        self._create_ui()
        
        # Status bar täzelemek üçin thread
        self.stop_status = False
        self.status_thread = threading.Thread(target=self._update_status_loop, daemon=True)
        self.status_thread.start()

    def _create_ui(self):
        """Interfeýsi döretmek"""
        
        # 1. Ýokarky bölek (Header)
        self.header_frame = ctk.CTkFrame(self.root, height=100, fg_color="#0f0f1a", corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="JARVIS", 
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#00e5ff"  # Neony gök
        )
        self.title_label.pack(pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame, 
            text="Türkmen Akylly Kömekçi", 
            font=ctk.CTkFont(size=16),
            text_color="#aaaaaa"
        )
        self.subtitle_label.pack(pady=(0, 10))

        # 2. Ortaky bölek (Çat meýdany)
        self.chat_frame = ctk.CTkFrame(self.root, fg_color="#12121f", corner_radius=15)
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.chat_display = ctk.CTkTextbox(
            self.chat_frame, 
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            fg_color="#12121f",
            scrollbar_button_color="#00e5ff",
            state="disabled"  # Ulanyjy editlep bilmez
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Ilkinji salamlaşyk
        self._add_to_chat("JARVIS", "Salam! Men JARVIS. Size nähili kömek edip bilerin?")
        self._speak_async("Salam! Men JARVIS. Size nähili kömek edip bilerin?")

        # 3. Aşaky bölek (Giriş we Düwmeler)
        self.input_frame = ctk.CTkFrame(self.root, fg_color="#0f0f1a", height=120, corner_radius=0)
        self.input_frame.pack(fill="x", padx=0, pady=0)
        
        # Giriş meýdany
        self.entry_box = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Bu ýere ýazyň ýa-da buýruk beriň...",
            height=50,
            font=ctk.CTkFont(size=16),
            border_width=2,
            border_color="#00e5ff",
            fg_color="#1a1a2e"
        )
        self.entry_box.pack(pady=(20, 10), padx=20, fill="x")
        self.entry_box.bind("<Return>", lambda e: self.process_command())
        
        # Düwmeler
        self.btn_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.btn_frame.pack(pady=(0, 10))
        
        self.send_btn = ctk.CTkButton(
            self.btn_frame,
            text="Ýiber",
            command=self.process_command,
            width=150,
            height=40,
            fg_color="#00e5ff",
            hover_color="#00b8cc",
            text_color="#000000",
            font=ctk.CTkFont(weight="bold")
        )
        self.send_btn.pack(side="left", padx=20)
        
        self.clear_btn = ctk.CTkButton(
            self.btn_frame,
            text="Arassala",
            command=self._clear_chat,
            width=150,
            height=40,
            fg_color="#333344",
            hover_color="#444455",
            text_color="#ffffff"
        )
        self.clear_btn.pack(side="right", padx=20)

        # 4. Status Bar (CPU/RAM/Wagt)
        self.status_frame = ctk.CTkFrame(self.root, height=30, fg_color="#000000", corner_radius=0)
        self.status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ulgam: Ýüklenýär...",
            font=ctk.CTkFont(size=12),
            text_color="#00ff00",  # Ýaşyl tekst
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10)
        
        self.time_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff",
            anchor="e"
        )
        self.time_label.pack(side="right", padx=10)

    def _add_to_chat(self, sender: str, message: str):
        """Çat meýdanyna habar goşmak"""
        self.chat_display.configure(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M")
        formatted_msg = f"[{timestamp}] {sender}: {message}\n\n"
        
        # Reňkleri sazlamak (JARVIS gök, Ulanyjy ak)
        if sender == "JARVIS":
            self.chat_display.insert("end", formatted_msg, "jarvis")
            self.chat_display.tag_config("jarvis", foreground="#00e5ff")
        else:
            self.chat_display.insert("end", formatted_msg, "user")
            self.chat_display.tag_config("user", foreground="#ffffff")
            
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def _speak_async(self, text: str):
        """Aýratyn threadde seslendirmek (GUI doňmazlygy üçin)"""
        def speak_thread():
            while self.is_speaking:
                time.sleep(0.1)
            self.is_speaking = True
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Ses ýalňyşlygy: {e}")
            finally:
                self.is_speaking = False
        
        threading.Thread(target=speak_thread, daemon=True).start()

    def _update_status_loop(self):
        """Real-wagtda CPU we RAM maglumatlaryny täzelemek"""
        while not self.stop_status:
            try:
                cpu = psutil.cpu_percent(interval=1)
                ram = psutil.virtual_memory().percent
                now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                
                status_text = f"CPU: {cpu}% | RAM: {ram}% | Ulgam: Aktiw"
                
                # Renkleri üýtgetmek (Ýokary ýük bolsa gyzyl)
                if cpu > 80 or ram > 80:
                    color = "#ff3333"
                else:
                    color = "#00ff00"
                
                self.status_label.configure(text=status_text, text_color=color)
                self.time_label.configure(text=now)
            except Exception:
                pass
            time.sleep(2)

    def process_command(self):
        """Ulanyjynyň buýrugyny işlemek"""
        user_input = self.entry_box.get().strip()
        if not user_input:
            return
        
        # Ekrana çykarmak
        self._add_to_chat("Siz", user_input)
        self.entry_box.delete(0, "end")
        
        # Jogaby tapmak we işlemek
        response = self._analyze_command(user_input)
        
        # Jogaby ekrana we sese bermek
        if response:
            self._add_to_chat("JARVIS", response)
            self._speak_async(response)

    def _analyze_command(self, command: str) -> str:
        """Buýrugy analiz etmek we jogap gaýtarmak"""
        cmd_lower = command.lower()
        
        # 1. Salamlaşyk
        if any(word in cmd_lower for word in ["salam", "sag bol", "gowmy", "habarlar"]):
            return "Salam! Hoş geldiňiz. Size nähili kömek edip bilerin?"
        
        # 2. Wagt we Sene
        if "wagt" in cmd_lower or "sagat" in cmd_lower:
            now = datetime.datetime.now().strftime("%H:%M")
            return f"Häzirki wagt: {now}"
        
        if "sene" in cmd_lower or "tarih" in cmd_lower:
            today = datetime.datetime.now().strftime("%d.%m.%Y")
            return f"Bügün: {today}"
        
        # 3. Google Gözleg
        if "google" in cmd_lower or "gözle" in cmd_lower:
            query = command.replace("google", "").replace("gözle", "").strip()
            if not query:
                return "Näme gözlemeli? Haýyş, gözleg sözlerini ýazyň."
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Google'da '{query}' boýunça gözleg açyldy."
        
        # 4. YouTube
        if "youtube" in cmd_lower or "video" in cmd_lower:
            query = command.replace("youtube", "").replace("video", "").strip()
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            return "YouTube'da wideo gözleg açyldy."
        
        # 5. Programma açmak (CMD, Notepad, Kalkulýator)
        if "cmd" in cmd_lower or "komanda" in cmd_lower or "terminal" in cmd_lower:
            try:
                os.system("start cmd" if os.name == 'nt' else "gnome-terminal")
                return "Komanda setiri (CMD) açyldy."
            except Exception:
                return "Komanda setirini açyp bolmady."
        
        if "notepad" in cmd_lower or "bloknot" in cmd_lower:
            try:
                os.system("notepad" if os.name == 'nt' else "gedit")
                return "Notepad açyldy."
            except Exception:
                return "Notepad'i açyp bolmady."
        
        if "kalkulýator" in cmd_lower or "hasapla" in cmd_lower:
            try:
                os.system("calc" if os.name == 'nt' else "gnome-calculator")
                return "Kalkulýator açyldy."
            except Exception:
                return "Kalkulýatory açyp bolmady."

        # 6. Ulgam maglumatlary
        if "cpu" in cmd_lower or "protsessor" in cmd_lower:
            cpu = psutil.cpu_percent(interval=1)
            return f"Häzirki CPU ulanylyşy: {cpu}%"
        
        if "ram" in cmd_lower or "operatiw" in cmd_lower:
            ram = psutil.virtual_memory().percent
            return f"Häzirki RAM ulanylyşy: {ram}%"
        
        # 7. Sag bol / Çykmak
        if "sag bol" in cmd_lower or "rahmat" in cmd_lower:
            return "Arzuw etmeýärin! Başga soragyňyz barmy?"
        
        if "çyk" in cmd_lower or "gutbyr" in cmd_lower or "tamam" in cmd_lower:
            self.root.quit()
            return "Hoş sag boluň! JARVIS öçürilýär..."
        
        # Default jogap
        return "Bagyşlaň, men bu buýrugy düşünmedim. 'Google', 'YouTube', 'CMD', 'Wagt' ýaly sözleri ulanyp bilersiňiz."

    def _clear_chat(self):
        """Çaty arassalamak"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
        self._add_to_chat("JARVIS", "Çat arassalandy. Täze buýruk berip bilersiňiz.")

    def run(self):
        """Programmany işletmek"""
        try:
            self.root.mainloop()
        finally:
            self.stop_status = True

if __name__ == "__main__":
    app = JarvisAssistant()
    app.run()
