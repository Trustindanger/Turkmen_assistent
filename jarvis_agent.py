#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Stilinde Döwrebap Kompýuter Agent-Assistent
OOP Arhitektura, CustomTkinter, Türkmen Dili
"""

import customtkinter as ctk
import psutil
import pyttsx3
import webbrowser
import os
import threading
import time
from datetime import datetime

# --- Konfigurasiýa ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JarvisAssistant:
    """JARVIS Agentiniň Esasy Klaspy"""
    
    def __init__(self):
        # Ses injeneri
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # GUI gurulşy
        self.root = ctk.CTk()
        self.root.title("JARVIS - Türkmen Kömekçisi")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # UI elementleri
        self.chat_history = None
        self.user_input = None
        self.status_label = None
        self.cpu_bar = None
        self.ram_bar = None
        
        self.build_ui()
        self.start_system_monitor()
        
        # Salamlaşyk
        self.speak("Salam! Men JARVIS, siziň şahsy kömekçiňiz. Size nähili kömek edip bilerin?")
        self.add_to_chat("JARVIS", "Salam! Men JARVIS, siziň şahsy kömekçiňiz. Size nähili kömek edip bilerin?")
    
    def setup_voice(self):
        """Ses sazlamalary"""
        voices = self.engine.getProperty('voices')
        # Iň soňky sesi saýla (köplenç erkek ses)
        if voices:
            self.engine.setProperty('voice', voices[-1].id)
        self.engine.setProperty('rate', 150)  # Tizlik
        self.engine.setProperty('volume', 0.9)  # Göwrüm
    
    def speak(self, text):
        """Teksti sese öwürmek (Threadde)"""
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Ses ýalňyşlygy: {e}")
        
        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()
    
    def build_ui(self):
        """Interfeýsi gurmak"""
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # 1. Başlyk (Header)
        header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🤖 JARVIS", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00ffff"
        )
        title_label.grid(row=0, column=0, pady=15)
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Döwrebap Kompýuter Agent-Assistent",
            font=ctk.CTkFont(size=14),
            text_color="#aaaaaa"
        )
        subtitle.grid(row=1, column=0, pady=(0, 10))
        
        # 2. Çat Meýdany (Chat Area)
        chat_frame = ctk.CTkFrame(self.root, corner_radius=10)
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_history = ctk.CTkTextbox(
            chat_frame,
            font=ctk.CTkFont(size=14),
            text_color="#ffffff",
            state="disabled"
        )
        self.chat_history.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 3. Giriş Meýdany (Input Area)
        input_frame = ctk.CTkFrame(self.root, height=100, corner_radius=0)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.user_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Bu ýere ýazyň... (mysal: 'Google-de Python gözle')",
            font=ctk.CTkFont(size=16),
            height=45
        )
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self.process_command())
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="Ugrat",
            command=self.process_command,
            width=100,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#0088ff",
            hover_color="#0066cc"
        )
        send_btn.grid(row=0, column=1)
        
        # 4. Status Bar (CPU we RAM)
        status_frame = ctk.CTkFrame(self.root, height=120, corner_radius=0)
        status_frame.grid(row=3, column=0, sticky="ew", padx=0, pady=0)
        status_frame.grid_columnconfigure((0, 1), weight=1)
        
        # CPU
        cpu_label = ctk.CTkLabel(
            status_frame, 
            text="CPU Ulanyşy:", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ffff"
        )
        cpu_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.cpu_bar = ctk.CTkProgressBar(
            status_frame,
            width=300,
            height=20,
            corner_radius=10,
            fg_color="#333333",
            progress_color="#00ff00"
        )
        self.cpu_bar.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.cpu_bar.set(0)
        
        self.cpu_percent_label = ctk.CTkLabel(
            status_frame,
            text="%0",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff"
        )
        self.cpu_percent_label.grid(row=1, column=0, padx=(330, 0), pady=5, sticky="w")
        
        # RAM
        ram_label = ctk.CTkLabel(
            status_frame,
            text="RAM Ulanyşy:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ffff"
        )
        ram_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.ram_bar = ctk.CTkProgressBar(
            status_frame,
            width=300,
            height=20,
            corner_radius=10,
            fg_color="#333333",
            progress_color="#ff00ff"
        )
        self.ram_bar.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="w")
        self.ram_bar.set(0)
        
        self.ram_percent_label = ctk.CTkLabel(
            status_frame,
            text="%0",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff"
        )
        self.ram_percent_label.grid(row=3, column=0, padx=(330, 0), pady=(5, 15), sticky="w")
        
        # Wagt
        self.time_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="#aaaaaa"
        )
        self.time_label.grid(row=0, column=1, rowspan=4, padx=20, sticky="e")
    
    def add_to_chat(self, sender, message):
        """Çata habar goşmak"""
        self.chat_history.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "Siz":
            self.chat_history.insert("end", f"\n[{timestamp}] {sender}: {message}\n", "user")
        else:
            self.chat_history.insert("end", f"\n[{timestamp}] {sender}: {message}\n", "jarvis")
        
        self.chat_history.see("end")
        self.chat_history.configure(state="disabled")
    
    def process_command(self):
        """Buýrugy işlemek"""
        command = self.user_input.get().strip()
        if not command:
            return
        
        self.user_input.delete(0, "end")
        self.add_to_chat("Siz", command)
        
        # Buýrugy işlemek üçin thread
        thread = threading.Thread(target=self.execute_command, args=(command,), daemon=True)
        thread.start()
    
    def execute_command(self, command):
        """Buýrugy ýerine ýetirmek"""
        command_lower = command.lower()
        response = ""
        
        # Salamlaşyk
        if any(word in command_lower for word in ["salam", "hello", "hi", "günortanyz haýyrly bolsun"]):
            response = "Salam! Size nähili kömek edip bilerin?"
        
        # Google gözleg
        elif "google" in command_lower and "gözle" in command_lower:
            query = command_lower.replace("google-de", "").replace("gözle", "").strip()
            if query:
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                response = f"Google-de '{query}' boýunça gözleg açyldy."
            else:
                response = "Näme gözlemeli? Diýip görkeziň."
        
        # YouTube gözleg
        elif "youtube" in command_lower and "gözle" in command_lower:
            query = command_lower.replace("youtube-da", "").replace("gözle", "").strip()
            if query:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(url)
                response = f"YouTube-da '{query}' boýunça gözleg açyldy."
            else:
                response = "Näme gözlemeli? Diýip görkeziň."
        
        # Web sahypa açmak
        elif "aç" in command_lower and ("saýt" in command_lower or "web" in command_lower):
            if "google.com" in command_lower:
                webbrowser.open("https://google.com")
                response = "Google sahypasy açyldy."
            elif "youtube.com" in command_lower:
                webbrowser.open("https://youtube.com")
                response = "YouTube sahypasy açyldy."
        
        # CMD açmak
        elif "cmd" in command_lower or "komanda setiri" in command_lower or "terminal" in command_lower:
            try:
                os.system("start cmd" if os.name == "nt" else "gnome-terminal")
                response = "Komanda setiri (CMD) açyldy."
            except Exception as e:
                response = f"CMD açyp bolmady: {str(e)}"
        
        # Programma açmak
        elif "notepad" in command_lower or "bellik" in command_lower:
            try:
                os.system("notepad" if os.name == "nt" else "gedit")
                response = "Notepad açyldy."
            except Exception as e:
                response = f"Notepad açyp bolmady: {str(e)}"
        
        # Wagt
        elif "wagt" in command_lower or "sagat" in command_lower:
            now = datetime.now().strftime("%H:%M:%S")
            response = f"Häzirki wagt: {now}"
        
        # Sene
        elif "sene" in command_lower or "tarih" in command_lower:
            today = datetime.now().strftime("%d.%m.%Y")
            response = f"Bugün: {today}"
        
        # Howa
        elif "howa" in command_lower:
            response = "Men häzirki wagtda howa maglumatlaryny getirip bilmeýärin, ýöne internetden gözläp bilerin."
            webbrowser.open("https://www.google.com/search?q=howa+maglumaty")
        
        # Kömek
        elif "kömek" in command_lower or "näme edip bilersiň" in command_lower:
            response = (
                "Men size aşakdakylarda kömek edip bilerin:\n"
                "• Google we YouTube-da gözleg etmek\n"
                "• Web sahypalary açmak\n"
                "• CMD we Notepad ýaly programmalary açmak\n"
                "• Wagty we senäni aýtmak\n"
                "• Ulgamyň ýagdaýyny yzarlamak"
            )
        
        # Sagbol
        elif "sagbol" in command_lower or "rahmet" in command_lower:
            response = "Haçan-da bolsa kömek etmäge taýýar!"
        
        # Çykmak
        elif "çyk" in command_lower or "gutap" in command_lower or "stop" in command_lower:
            response = "Hoş sag boluň! Ýene-de kömek gerek bolsa, meni çagyryň."
            self.root.after(2000, self.root.quit)
        
        # Default jogap
        else:
            response = f"Bagyşlaň, '{command}' buýrugyny düşünmedim. 'Kömek' diýip sorap bilersiňiz."
        
        # Jogaby çata goş we sesli aýt
        self.root.after(0, lambda: self.add_to_chat("JARVIS", response))
        self.root.after(500, lambda: self.speak(response))
    
    def update_system_status(self):
        """Ulgam ýagdaýyny täzelemek"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            
            # Progress barlary täzelemek
            self.cpu_bar.set(cpu_percent / 100.0)
            self.cpu_percent_label.configure(text=f"%{cpu_percent:.1f}")
            
            self.ram_bar.set(ram_percent / 100.0)
            self.ram_percent_label.configure(text=f"%{ram_percent:.1f}")
            
            # Reňk üýtgetmek (ýokary ulanyşda gyzyl)
            if cpu_percent > 80:
                self.cpu_bar.configure(progress_color="#ff0000")
            else:
                self.cpu_bar.configure(progress_color="#00ff00")
            
            if ram_percent > 80:
                self.ram_bar.configure(progress_color="#ff0000")
            else:
                self.ram_bar.configure(progress_color="#ff00ff")
            
            # Wagt
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            self.time_label.configure(text=current_time)
            
        except Exception as e:
            print(f"Ulgam ýagdaýyny täzeläp bolmady: {e}")
        
        # 2 sekuntdan soňra gaýtadan çagyrmak
        self.root.after(2000, self.update_system_status)
    
    def start_system_monitor(self):
        """Ulgam monitorini başlatmak"""
        self.update_system_status()
    
    def run(self):
        """Programmany işledmek"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        jarvis = JarvisAssistant()
        jarvis.run()
    except KeyboardInterrupt:
        print("\nProgramma tamamlandy.")
    except Exception as e:
        print(f"Ýalňyşlyk: {e}")
