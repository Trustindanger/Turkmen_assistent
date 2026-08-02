"""
JARVIS Agent - Ulanyjy Interfeýsi (UI)
CustomTkinter bilen döwrebap dizaýn
"""

import customtkinter as ctk
from config import THEME_COLOR, BG_COLOR, SECONDARY_BG, FONT_FAMILY

class JarvisUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Esasy sazlamalar
        self.title("🤖 JARVIS - Türkmen Assistent")
        self.geometry("900x700")
        self.configure(fg_color=BG_COLOR)
        
        # Grid sazlamalary
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Çat meýdany ösýär
        
        # UI komponentlerini döretmek
        self._create_header()
        self._create_chat_area()
        self._create_input_area()
        self._create_status_bar()
    
    def _create_header(self):
        """Ýokarky başlyk bölegi"""
        header_frame = ctk.CTkFrame(self, fg_color=SECONDARY_BG, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Logo / Ady
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 J.A.R.V.I.S",
            font=(FONT_FAMILY, 28, "bold"),
            text_color=THEME_COLOR
        )
        title_label.grid(row=0, column=0, padx=20, pady=10)
        
        # Kiçi düşündiriş
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Just A Rather Very Intelligent System",
            font=(FONT_FAMILY, 12),
            text_color="#888888"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 10))
    
    def _create_chat_area(self):
        """Ortada çat meýdany"""
        chat_frame = ctk.CTkFrame(self, fg_color=SECONDARY_BG)
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)
        
        # Text widget (Chat taryhy)
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=(FONT_FAMILY, 14),
            text_color="#FFFFFF",
            fg_color=SECONDARY_BG,
            border_color=THEME_COLOR,
            border_width=1,
            corner_radius=10
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Başlangyç habary
        self.add_message("JARVIS", "Salam! Men JARVIS. Size nähili kömek edip bilerin?\n\nMen şulary bilýärin:\n• 'Sesli giriş' düwmesi basyp gürleň\n• 'Google ...' ýa-da 'YouTube ...' diýip gözleg ediň\n• 'Notepad aç', 'Kalkulýator aç' diýip programma açyň\n• 'Hawa näme' diýip howa maglumatyny soraň\n• 'Wagt näçe', 'Sene näçe' diýip soraň")
    
    def _create_input_area(self):
        """Aşakda giriş meýdany"""
        input_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, height=100)
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Tekst giriş meýdany
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Buýrugy ýazyň ýa-da sesli girişi ulanyň...",
            font=(FONT_FAMILY, 14),
            height=40,
            border_color=THEME_COLOR,
            fg_color=SECONDARY_BG,
            text_color="#FFFFFF"
        )
        self.input_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.input_entry.bind("<Return>", lambda e: self.trigger_send())
        
        # Ibermek düwmesi
        send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Iber",
            command=self.trigger_send,
            width=80,
            height=40,
            fg_color=THEME_COLOR,
            hover_color="#00C8D4",
            text_color="#000000",
            font=(FONT_FAMILY, 14, "bold")
        )
        send_btn.grid(row=0, column=1, padx=5, pady=10)
        
        # Sesli giriş düwmesi
        self.voice_btn = ctk.CTkButton(
            input_frame,
            text="🎤 Sesli Giriş",
            command=self.trigger_voice,
            width=120,
            height=40,
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            text_color="#FFFFFF",
            font=(FONT_FAMILY, 14, "bold")
        )
        self.voice_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
    
    def _create_status_bar(self):
        """Iň aşakda status bar"""
        status_frame = ctk.CTkFrame(self, fg_color=SECONDARY_BG, height=40)
        status_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))
        status_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # CPU
        self.cpu_label = ctk.CTkLabel(
            status_frame,
            text="CPU: --%",
            font=(FONT_FAMILY, 11),
            text_color="#00FF00"
        )
        self.cpu_label.grid(row=0, column=0, padx=10)
        
        # RAM
        self.ram_label = ctk.CTkLabel(
            status_frame,
            text="RAM: --%",
            font=(FONT_FAMILY, 11),
            text_color="#00FFFF"
        )
        self.ram_label.grid(row=0, column=1, padx=10)
        
        # Wagt
        self.time_label = ctk.CTkLabel(
            status_frame,
            text="--:--:--",
            font=(FONT_FAMILY, 11),
            text_color="#FFFFFF"
        )
        self.time_label.grid(row=0, column=2, padx=10)
        
        # Status
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="✅ Taýýar",
            font=(FONT_FAMILY, 11),
            text_color=THEME_COLOR
        )
        self.status_label.grid(row=0, column=3, padx=10)
    
    def add_message(self, sender, message):
        """Çata habar goşmak"""
        if sender == "JARVIS":
            prefix = f"🤖 {sender}: "
            color = THEME_COLOR
        else:
            prefix = f"👤 {sender}: "
            color = "#FFD700"
        
        self.chat_display.insert("end", f"{prefix}{message}\n\n")
        self.chat_display.see("end")  # Iň soňka süýşür
    
    def get_input(self):
        """Giriş meýdanyndan tekst almak"""
        return self.input_entry.get().strip()
    
    def clear_input(self):
        """Giriş meýdanyny arassalamak"""
        self.input_entry.delete(0, "end")
    
    def update_status(self, cpu=None, ram=None, time_str=None, status=None):
        """Status bar täzelemek"""
        if cpu is not None:
            color = "#00FF00" if cpu < 50 else "#FFFF00" if cpu < 80 else "#FF0000"
            self.cpu_label.configure(text=f"CPU: {cpu}%", text_color=color)
        
        if ram is not None:
            color = "#00FFFF" if ram < 50 else "#FFA500" if ram < 80 else "#FF0000"
            self.ram_label.configure(text=f"RAM: {ram}%", text_color=color)
        
        if time_str:
            self.time_label.configure(text=time_str)
        
        if status:
            self.status_label.configure(text=status)
    
    def set_voice_active(self, active):
        """Sesli giriş wagtynda düwmäni üýtgetmek"""
        if active:
            self.voice_btn.configure(text="🔴 Diňleýär...", fg_color="#FF0000")
        else:
            self.voice_btn.configure(text="🎤 Sesli Giriş", fg_color="#FF6B6B")
    
    def trigger_send(self):
        """Ibermek düwmesiniň hadysasy (overrided edilýär)"""
        pass
    
    def trigger_voice(self):
        """Sesli giriş düwmesiniň hadysasy (overrided edilýär)"""
        pass
