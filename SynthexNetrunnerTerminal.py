import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import math
import threading

# --- Configuración del lenguaje Synthex Expandido ---
SYNTHEX_DICTIONARY = {
    # Básicos
    "hello": "░", "world": "Ω", "message": "▒", "ai": "▓", "network": "⊕",
    "encrypt": "Ψ", "decrypt": "Φ", "chaos": "§", "stable": "Δ", "link": "↔",
    "system": "Σ", "breach": "⍟", "code": "⎚", "data": "⍬", "error": "⊘",
    "memory": "⌂", "identity": "∞", "ghost": "⊚", "protocol": "⍱", "firewall": "◫",
    "trace": "⍒", "jack_in": "⍐", "construct": "⍦", "entity": "⍰", "sentience": "⍲",
    "anomaly": "⌖", "data_stream": "⍨", "probe": "⍴", "divert": "⍬⍬", "corrupt": "⍟§",
    "nullify": "ΨΦ", "access": "⎇", "security": "⌠", "core": "◉", "digital": "⎚⎚",
    "reality": "∞∞", "interface": "⌤", "threat": "⍞", "man": "⌘",
    
    # Nuevos glifos expandidos
    "root": "⌨", "admin": "⌬", "backdoor": "⌹", "botnet": "⌶", "virus": "⌼",
    "worm": "⌿", "trojan": "⍀", "keylogger": "⍁", "ransomware": "⍂", "spyware": "⍃",
    "malware": "⍄", "honeypot": "⍅", "sandbox": "⍆", "quarantine": "⍇", "whitelist": "⍈",
    "blacklist": "⍉", "exploit": "⍊", "vulnerability": "⍋", "patch": "⍌", "update": "⍍",
    "backup": "⍎", "restore": "⍏", "mirror": "⍑", "clone": "⍒", "sync": "⍓"
}

REV_SYNTHEX_DICTIONARY = {v: k for k, v in SYNTHEX_DICTIONARY.items()}
UNKNOWN_GLYPH = "?"

# Mapeo de glifos a formas (incluyendo nuevos)
GLYPH_SHAPES = {
    # Básicos (mantener los originales)
    "░": "square_block", "Ω": "omega", "▒": "dotted_block", "▓": "solid_block",
    "⊕": "circle_plus", "Ψ": "psi", "Φ": "phi", "§": "section", "Δ": "triangle",
    "↔": "left_right_arrow", "Σ": "sigma", "⍟": "star", "⎚": "rectangle",
    "⍬": "double_tilde", "⊘": "circle_slash", "⌂": "house", "∞": "infinity",
    "⊚": "circle_dot", "⍱": "protocol", "◫": "firewall", "⍒": "down_arrow",
    "⍐": "up_arrow", "⍦": "construct", "⍰": "question_box", "⍲": "sentience",
    "⌖": "anomaly", "⍨": "data_stream", "⍴": "probe", "⍬⍬": "divert",
    "⍟§": "corrupt", "ΨΦ": "nullify", "⎇": "access", "⌠": "security",
    "◉": "core", "⎚⎚": "digital", "∞∞": "reality", "⌤": "interface",
    "⍞": "threat", "⌘": "man",
    
    # Nuevos glifos
    "⌨": "keyboard", "⌬": "admin_key", "⌹": "backdoor", "⌶": "botnet",
    "⌼": "virus", "⌿": "worm", "⍀": "trojan", "⍁": "keylogger",
    "⍂": "ransomware", "⍃": "spyware", "⍄": "malware", "⍅": "honeypot",
    "⍆": "sandbox", "⍇": "quarantine", "⍈": "whitelist", "⍉": "blacklist",
    "⍊": "exploit", "⍋": "vulnerability", "⍌": "patch", "⍍": "update",
    "⍎": "backup", "⍏": "restore", "⍑": "mirror", "⍒": "clone", "⍓": "sync"
}

# --- TEMAS VISUALES ---
THEMES = {
    "classic": {"bg": "#000000", "text": "#00FF00", "accent": "#00FFFF"},
    "ice": {"bg": "#001F3F", "text": "#7FDBFF", "accent": "#007BFF"},
    "neon": {"bg": "#191970", "text": "#F0F8FF", "accent": "#FF69B4"},
    "fire": {"bg": "#3D0000", "text": "#FF4136", "accent": "#FF851B"},
    "netrunner": {"bg": "#420016", "text": "#A10036", "accent": "#2ddbdb"},
    "matrix": {"bg": "#000000", "text": "#00FF22", "accent": "#00ff22"},
    
}

# Listas para la lógica de animación
ATTACK_GLYPH_WORDS = ["breach", "corrupt", "virus", "worm", "trojan", "exploit", "botnet", "ransomware", "spyware", "malware", "keylogger", "threat"]
SECURITY_GLYPH_WORDS = ["firewall", "security", "stable", "sandbox", "honeypot", "whitelist", "quarantine", "patch", "backup"]

# --- NUEVA ESTRUCTURA DE CONSTELACIONES ---
GLYPH_CONSTELLATIONS = {
    "AI & CONSCIOUSNESS": ["ai", "sentience", "construct", "entity", "ghost", "identity", "memory"],
    "SECURITY & DEFENSE": ["firewall", "security", "stable", "sandbox", "honeypot", "whitelist", "quarantine", "patch", "backup"],
    "THREATS & EXPLOITS": ["breach", "corrupt", "virus", "worm", "trojan", "keylogger", "ransomware", "spyware", "malware", "exploit", "threat", "anomaly", "chaos"],
    "CORE NETWORK CONCEPTS": ["system", "core", "digital", "reality", "interface", "link", "protocol", "data_stream", "probe"],
    "BASIC OPERATIONS": ["hello", "world", "message", "network", "encrypt", "decrypt", "code"]
}

class SynthexTerminalEnhanced(tk.Tk):
    _ascii_warning_active = False
    def show_ascii_warning(self, flashes=10, delay=60):
        """Muestra el ASCII parpadeando rápidamente y oculta la red temporalmente. Al terminar, restaura la red y repite el ciclo si la integridad sigue baja."""
        ascii_art = r"""                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
                                                                                                                  
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████▓ ▓█████████████████████▓▓██████████▒▒▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████░  ▓█████▓░░░░░░░░░░░░░░░░░░░░▓██████ ░ ▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████▒ ░ ▓█████▓░░░░▒▒░░▒▒▓▓░░▒▒▒▒░░▓██████ ▒  ███▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████  ▒ ░█████▓░░░▒▒▓▒░░▓▓▓░▒░░░▒░░▓█████▓ ▒  ▓███████▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████  ░▒ ▓████▓░░░▓░▒░░▒░▒▒░▒▓▒▒▓░░▓█████ ░▒  ▒███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████   ▒░ ████▓░░░░░▓▓░▒░▒░░▓▓▓░░░░▓████░ ▒   ░███▓███▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███████   ░▒░ ▓█▒ ░░░░░▓▒░░▓░░░░▒░░░░░ ░▓█░ ▒▒   ▓███▓█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████░  ░▒░▒    ░░░░░░░░░░░░░░░░░░░░    ░▒▒░   █████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████▓    ▒░▒░       ░   ▒▓            ▒░▒    ░████▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████ ░ ░▒▒░▒▒        ░ ▓█░▓        ▒▒░▒▒░   ▓███████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▓    ░▒▒░▒▒ ░              ░ ░▒▒░▒░    ░███████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████▒      ░▒▒ ▒▒ ░             ░░▒ ▒▒░   ░  ░███████████▓▓▓▓▓▓▓▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████          ▒▒░                ░▒▒          ▓█████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████      ░     ░        ░       ▒            ▒███████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████▓    ▓  ▓      ░░░░    ▒      ▓ ░   ▒░░      ▒  ▓░   ▒█████▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██   ▒   ▒▒          ▒▓▓▓      ▒▓▓▓          ░▓   ▓   ▒█▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░▒██▓      ░ ░      ▒▓█▓▒░░      ░░▒▒█▓▒       ▒░       ██▓░░░░░░███▒██████▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░▒███░    ░ ▒ ▒▒▒░▓▓▒   ░           ░  ░▓▓░▒▒▒░▒       ███▓░░░░░░██░░░█████▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░░▒██▒░░░░░░░░░░▒███▓ ░  ░  ▒▓▓▓░           ░▒           ░▓▓▓▓   ░   ▒███▓░░░░░░██▓░░░░░░▓▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░▒██▒░░░░░░░░░░░░▒███▓    ▒▒                ░▒▓░                ░▓    ▒███▓░░░░░░░░░█░░░█▓░▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░██████████████▓░░▒▓██▓ ▓    ░░               ▒▒                ▒    ▒ ▓██████▓░░░████▒░░░██▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░██▓░░░░░░░░░░░░▒████▓ ░   ▒█▓             ▒▒▓▒░            ▒█▓   ░ ▓████▓░░░░░░███▒░▒░░██▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░░░▓█▓░░░░░░░░░░▒█████       ▓█▓▒▒ ░▒    ▒▓░██▒▓▓    ▒░ ░▒▓█▓       ████▓▓░░░░░░██▓░▓█▓░░░░░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░▒▓████     ░     ░░  ░  ▓▒░▓█▓▓░▒▓   ░ ░░░     ░    █████▓░░░░░░█▒░▒██████▓░░░░░▓▓▓▓▓▓   
   ▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░▒█████░░    ░▓░     ▒     ▒███▓▓     ▒      ▓░░   ▒ █████▓░░░░░░░█▒░▒██████▒░░░░▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████░             ░      ▓▓░      ░       ░     ▓███████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓███▓████           ░              ░           ██████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████░            ░          ░            ░█████▓███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████░       ▒░                  ░▒        ███████▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓███      ░░▒  ░░          ░░  ▒░░      ▓██████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████    ░▒░ ▒   ░▒      ▒░   ▒ ░▒░    ▓█████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████  ▒                    ░     ▒  ███████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓████             ░░    ░░             ██████▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████▓▓▓██░                         ██▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████▓     ▒    ▒▒    ▒     ▓████▓█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓▓▓▓▓▓█▓▓▓██████████▓ ░▒ ░▓████▓░ ▒░ ▓██████████▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████████▓  ▒█████▓▓  ▓████▓█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓   
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓███████▓▒    ▒▓███████▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        """
        # Guardar el estado actual de la red
        saved_glyphs = list(self.current_glyphs) if hasattr(self, "current_glyphs") else []
        saved_text = getattr(self, "last_original_text", "")
        self.canvas.delete("all")
        self.glyph_coords.clear()
        self.glyph_tooltips.clear()
        self.glyph_constellation_map.clear()
        self.current_glyphs = []
        def flash_ascii(count):
            self.canvas.delete("all")
            if count % 2 == 0:
                self.canvas.create_text(
                    self.canvas.winfo_width() // 2,
                    self.canvas.winfo_height() // 2,
                    text=ascii_art,
                    fill="#FF0000",
                    font=("Consolas", 13, "bold"),
                    anchor="center",
                    justify="center"
                )
            if count > 0:
                self.after(delay, lambda: flash_ascii(count - 1))
            else:
                self.canvas.delete("all")
                # Restaurar la red visual
                if saved_glyphs:
                    self.visualize_synthex_network(saved_glyphs, saved_text)
                # Si la integridad sigue <15%, repetir el ciclo tras 6.66s
                if self.system_integrity < 15:
                    self.after(2000, lambda: self.show_ascii_warning(flashes, delay))
        flash_ascii(flashes)
    # Relación malware-objetivo-duración para visualización
    malware_links = []  # Cada elemento: (malware_glyph, target_index, duration)
    # --- Estados persistentes para modo pentester ---
    pentester_integrity = None
    pentester_stealth_level = None
    pentester_stealth_status = None
    # --- NUEVO: Parámetros de malware y sigilo ---
    MALWARE_STATS = {
        "virus":      {"damage": 90,  "stealth": 10, "min_time": 1,  "max_time": 3},
        "worm":       {"damage": 25, "stealth": 30, "min_time": 15, "max_time": 40},
        "trojan":     {"damage": 15, "stealth": 20, "min_time": 5,  "max_time": 10},
        "ransomware": {"damage": 30, "stealth": 10, "min_time": 15, "max_time": 30},
        "spyware":    {"damage": 5,  "stealth": 50, "min_time": 20, "max_time": 20},
        "malware":    {"damage": None, "stealth": None, "min_time": 5,  "max_time": 30},
        "keylogger":  {"damage": 2,  "stealth": 20, "min_time": 2,  "max_time": 60},
    }

    def update_status_labels(self):
        self.integrity_label.config(text=f"Integrity: {self.system_integrity}%")
        self.stealth_label.config(text=f"Stealth: {self.stealth_level}%")
        self.threat_label.config(text=self.get_stealth_status())

        # Mostrar ASCII si la integridad baja de 15% y no está activo
        if self.system_integrity < 15 and not self._ascii_warning_active:
            self._ascii_warning_active = True
            self.show_ascii_warning(flashes=12, delay=40)
        elif self.system_integrity >= 15:
            self._ascii_warning_active = False

    def get_stealth_status(self):
        if self.stealth_level >= 80:
            return "SECURE"
        elif self.stealth_level >= 40:
            return "RISK"
        else:
            return "DANGER"

    def reduce_stealth_over_time(self):
        # Reduce stealth by 1 per minute (simulado por cada ataque)
        if self.mode == "pentester":
            self.stealth_level = max(0, self.stealth_level - 1)
            self.update_status_labels()

    def block_input(self, block=True):
        if block:
            self.console_input.config(state=tk.DISABLED)
        else:
            self.console_input.config(state=tk.NORMAL)

    def malware_attack(self, malware):
        # --- NUEVO: Selección de target antes de lanzar el ataque ---
        # Solo permite atacar si hay al menos un target en la red actual
        if not self.current_glyphs or len(self.current_glyphs) < 2:
            self.write_to_console("[ERROR] No valid targets in the current network. Run a command to generate a network first.", "#FF4444")
            return

        # Mostrar lista de posibles targets (excluyendo el malware mismo si está en la red)
        possible_targets = []
        for idx, glyph in enumerate(self.current_glyphs):
            word = REV_SYNTHEX_DICTIONARY.get(glyph, "")
            if word not in self.MALWARE_STATS:  # No atacar otros malware
                possible_targets.append((idx, word, glyph))

        if not possible_targets:
            self.write_to_console("[ERROR] No valid targets found in the current network.", "#FF4444")
            return

        # Si solo hay un target, seleccionarlo automáticamente
        if len(possible_targets) == 1:
            target_idx, target_word, target_glyph = possible_targets[0]
            self._launch_malware_attack(malware, (target_idx, target_word, target_glyph))
        else:
            # Mostrar lista de targets y pedir selección por consola
            self.write_to_console("Select a target to attack:", "#FFFF00")
            for i, (idx, word, glyph) in enumerate(possible_targets):
                self.write_to_console(f"  [{i+1}] {word.upper()} ({glyph})", "#FFFF00")
            self.write_to_console("Type the number of the target and press Enter.", "#FFFF00")

            # Guardar el malware y los posibles targets para el input handler
            self._pending_malware = malware
            self._pending_targets = possible_targets

            # Cambiar el handler de input solo para la selección de target
            self.console_input.unbind('<Return>')
            self.console_input.bind('<Return>', self._on_target_input, add='+')

    def _on_target_input(self, event):
        value = self.console_input.get().strip()
        self.console_input.delete(0, tk.END)
        try:
            num = int(value)
            if 1 <= num <= len(self._pending_targets):
                # Restaurar el handler normal de la consola
                self.console_input.unbind('<Return>')
                self.console_input.bind('<Return>', self.process_console_command)
                self.block_input(True)
                target_tuple = self._pending_targets[num-1]
                malware = self._pending_malware
                # Limpiar los temporales
                del self._pending_malware
                del self._pending_targets
                self._launch_malware_attack(malware, target_tuple)
            else:
                self.write_to_console("[ERROR] Invalid selection. Try again.", "#FF4444")
        except Exception:
            self.write_to_console("[ERROR] Invalid input. Enter a number.", "#FF4444")

    def _launch_malware_attack(self, malware, target_tuple):
        stats = self.MALWARE_STATS[malware]
        target_idx, target_word, target_glyph = target_tuple

        # Daño y tiempo
        if malware == "malware":
            damage = random.randint(10, 40)
            stealth = random.randint(10, 50)
            t_min, t_max = stats["min_time"], stats["max_time"]
            duration = random.randint(t_min, t_max)
        elif malware == "keylogger":
            # Keylogger: ataque persistente
            self.write_to_console(f"[KEYLOGGER] Attack initiated on {target_word.upper()} (persistent)", "#FF00FF")
            self.block_input(True)
            total_time = 60
            interval = 2
            elapsed = 0
            def keylogger_progress():
                nonlocal elapsed
                if elapsed < total_time:
                    self.show_progress_bar(f"Keylogger running on {target_word.upper()}", elapsed, total_time)
                    self.system_integrity = max(0, self.system_integrity - stats["damage"])
                    self.stealth_level = max(0, self.stealth_level - stats["stealth"])
                    self.update_status_labels()
                    self.reduce_stealth_over_time()
                    elapsed += interval
                    self.after(15000, keylogger_progress)  # 15 segundos entre intervalos
                else:
                    self.block_input(False)
                    self.show_progress_bar(f"Keylogger running on {target_word.upper()}", total_time, total_time, done=True)
                    self.write_to_console(f"[KEYLOGGER] Attack on {target_word.upper()} finished", "#FF00FF")
                    # Actualizar red visual con keylogger
                    # Guardar relación malware-objetivo-duración para visualización
                    malware_glyph = SYNTHEX_DICTIONARY.get(malware, UNKNOWN_GLYPH)
                    SynthexTerminalEnhanced.malware_links.append((malware_glyph, target_idx, total_time))
                    self._refresh_network_with_malware(malware)
            keylogger_progress()
            return
        else:
            damage = stats["damage"]
            stealth = stats["stealth"]
            t_min, t_max = stats["min_time"], stats["max_time"]
            duration = random.randint(t_min, t_max)

        # Guardar relación malware-objetivo-duración para visualización
        malware_glyph = SYNTHEX_DICTIONARY.get(malware, UNKNOWN_GLYPH)
        SynthexTerminalEnhanced.malware_links.append((malware_glyph, target_idx, duration))

        self.write_to_console(f"[{malware.upper()}] Attack in progress on {target_word.upper()}...", "#FF00FF")
        self.block_input(True)
        self.show_progress_bar(f"{malware.capitalize()} attacking {target_word.upper()}", 0, duration)
        def attack_progress(step=0):
            if step <= duration:
                self.show_progress_bar(f"{malware.capitalize()} attacking {target_word.upper()}", step, duration)
                self.after(1000, lambda: attack_progress(step + 1))
            else:
                self.system_integrity = max(0, self.system_integrity - damage)
                self.stealth_level = max(0, self.stealth_level - stealth)
                self.update_status_labels()
                self.reduce_stealth_over_time()
                self.block_input(False)
                self.show_progress_bar(f"{malware.capitalize()} attacking {target_word.upper()}", duration, duration, done=True)
                self.write_to_console(f"[{malware.upper()}] Attack on {target_word.upper()} finished. Damage: {damage}, Stealth lost: {stealth}", "#FF00FF")
                # Actualizar red visual con malware
                self._refresh_network_with_malware(malware)
        attack_progress()

    def _refresh_network_with_malware(self, malware):
        # Añadir el malware a la red actual y regenerar la visualización
        # Evitar duplicados
        malware_glyph = SYNTHEX_DICTIONARY.get(malware, UNKNOWN_GLYPH)
        if malware_glyph not in self.current_glyphs:
            new_glyphs = list(self.current_glyphs) + [malware_glyph]
            self.current_glyphs = new_glyphs
        # Siempre refresca la visualización (malware_links lleva el control de conexiones)
        self.visualize_synthex_network(self.current_glyphs)
        self.write_to_console(f"Network updated: {malware.upper()} now present in the network.", "#FF00FF")

    def show_progress_bar(self, label, value, total, done=False):
        # Solo una barra: borra cualquier barra previa antes de mostrar la nueva
        self.console_output.config(state=tk.NORMAL)
        # Buscar y eliminar cualquier línea previa de barra de progreso
        lines = self.console_output.get("1.0", tk.END).splitlines()
        bar_prefix = f"{label}: ["
        # Encuentra la línea de barra de progreso previa (si existe)
        bar_line_index = None
        for idx, line in enumerate(lines):
            if line.startswith(bar_prefix):
                bar_line_index = idx + 1  # Tkinter Text widget lines start at 1
                break
        if bar_line_index is not None:
            self.console_output.delete(f"{bar_line_index}.0", f"{bar_line_index}.0 lineend+1c")

        percent = int((value / total) * 100) if total else 100
        bar_len = 30
        filled = int(bar_len * percent / 100)
        bar = '[' + '⎇' * filled + '-' * (bar_len - filled) + f'] {percent}%'
        progress_text = f"{label}: {bar}"

        self.console_output.insert(tk.END, progress_text + "\n")
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)

        if done:
            # Elimina la barra de progreso final después de un breve tiempo
            def clear_bar():
                self.console_output.config(state=tk.NORMAL)
                # Buscar y eliminar la barra final
                lines = self.console_output.get("1.0", tk.END).splitlines()
                for idx, line in enumerate(lines):
                    if line.startswith(bar_prefix):
                        self.console_output.delete(f"{idx+1}.0", f"{idx+1}.0 lineend+1c")
                        break
                self.console_output.config(state=tk.DISABLED)
            self.after(500, clear_bar)
    def __init__(self):
        super().__init__()
        self.after_id = None
        self.title("Synthex Netrunner Terminal v2.0 - Enhanced")
        self.geometry("1600x900")
        #self.iconbitmap("synthex.ico")

        # Estado del sistema
        self.current_theme = "classic"
        self.current_layout = "cyberpunk_split"  # Layout por defecto
        self.system_integrity = 100
        self.stealth_level = 100
        self.threat_level = 0
        self.active_processes = []
        self.console_history = []
        self.data_flow_points = []
        self.glyph_tooltips = {}

        # --- NUEVO: modo de operación ---
        self.mode = None  # "pentester" o "security"

        # Restaurar estados pentester si existen
        if SynthexTerminalEnhanced.pentester_integrity is not None:
            self.system_integrity = SynthexTerminalEnhanced.pentester_integrity
        if SynthexTerminalEnhanced.pentester_stealth_level is not None:
            self.stealth_level = SynthexTerminalEnhanced.pentester_stealth_level

        self.current_view = "start"
        self.apply_theme()
        self.start_screen()

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.bg_color = theme["bg"]
        self.text_color = theme["text"]
        self.accent_color = theme["accent"]
        self.configure(bg=self.bg_color)
    
    # --- NUEVA FUNCIÓN: Pantalla de inicio ---
    def start_screen(self):
        self.current_view = "start"
        self.apply_theme()
        
        self.start_frame = tk.Frame(self, bg=self.bg_color, padx=50, pady=50)
        self.start_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.start_frame, text="SYNTHEX NETRUNNER TERMINAL", font=("Courier", 32, "bold"), fg=self.accent_color, bg=self.bg_color).pack(pady=20)
        tk.Label(self.start_frame, text=">>> SYSTEM PROTOCOL v2.0 READY <<<", font=("Courier", 24), fg=self.text_color, bg=self.bg_color).pack(pady=10)
        tk.Label(self.start_frame, text="Select your operation mode:", font=("Courier", 16), fg=self.text_color, bg=self.bg_color).pack(pady=40)

        # --- NUEVOS BOTONES DE MODOS ---
        btn_frame = tk.Frame(self.start_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="PENTESTER (Attack System)", font=("Courier", 14, "bold"),
                  bg="#FF4136", fg=self.bg_color, command=lambda: self.launch_terminal_mode("pentester"),
                  activebackground="#FF851B", activeforeground=self.bg_color,
                  bd=3, relief=tk.RAISED).pack(side=tk.LEFT, padx=20, ipadx=20, ipady=10)

        tk.Button(btn_frame, text="SECURITY OPS (Defend System)", font=("Courier", 14, "bold"),
                  bg="#00FF00", fg=self.bg_color, command=lambda: self.launch_terminal_mode("security"),
                  activebackground="#007BFF", activeforeground=self.bg_color,
                  bd=3, relief=tk.RAISED).pack(side=tk.LEFT, padx=20, ipadx=20, ipady=10)

        # Botón de manual
        tk.Button(self.start_frame, text="MANUAL (Ver Guía)", font=("Courier", 14), 
                  bg=self.text_color, fg=self.bg_color, command=self.show_manual,
                  activebackground=self.accent_color, activeforeground=self.bg_color,
                  bd=3, relief=tk.RAISED).pack(pady=20, ipadx=20, ipady=10)

    def launch_terminal_mode(self, mode):
        """Lanza la terminal en el modo seleccionado"""
        self.mode = mode
        self.current_view = "terminal"
        self.start_frame.destroy()
        self.setup_ui()
        self.start_animations()
        if mode == "pentester":
            # Sistema de dificultad aleatorio
            self.difficulty = random.randint(1, 10)
            self.write_to_console(f"=== PENTESTER MODE ACTIVATED === (Difficulty: {self.difficulty})", "#FF4136")
            self.write_to_console("You can only attack the system. Type 'help' for attack commands.")
            # Generar comando de red según dificultad y ejecutarlo en la consola
            net_cmd = self.generate_network_command_for_difficulty(self.difficulty)
            self.write_to_console(f"[auto] {net_cmd}", self.text_color)
            self.console_input.delete(0, tk.END)
            # Ejecutar el comando como si el usuario lo hubiera escrito
            self.encrypt_text(net_cmd)
        elif mode == "security":
            self.write_to_console("=== SECURITY OPS MODE ACTIVATED ===", "#00FF00")
            self.write_to_console("You can only counter threats and restore the system. Type 'help' for defense commands.")
        self.write_to_console("Type 'man' for Synthex language manual")
        self.write_to_console("Type 'test' to visualize glyph constellations")

    def generate_network_command_for_difficulty(self, difficulty):
        """Genera un comando de red Synthex según la dificultad"""
        # Elementos defensivos y de datos
        defensivos = ["firewall", "security", "interface", "core"]
        datos = ["message", "network", "encrypt", "decrypt", "link", "system", "code", "data", "ai"]
        # Niveles
        if difficulty <= 3:
            elems = random.sample(defensivos, 2) + random.sample(datos, 3)
        elif difficulty <= 6:
            elems = random.sample(defensivos, 3) + random.sample(datos, 4)
        elif difficulty <= 8:
            elems = defensivos + random.sample(datos, 5)
        else:
            elems = defensivos + random.sample(datos, 6)
        random.shuffle(elems)
        return " ".join(elems)

    # --- FIN DE LAS NUEVAS FUNCIONES ---

    def setup_ui(self):
        # Limpiar toda la interfaz anterior
        for widget in self.winfo_children():
            widget.destroy()
            
        # Aplicar el layout seleccionado
        if self.current_layout == "cyberpunk_split":
            self.setup_cyberpunk_split_layout()
        elif self.current_layout == "matrix_cascade":
            self.setup_matrix_cascade_layout()
        elif self.current_layout == "holographic_hub":
            self.setup_holographic_hub_layout()
        elif self.current_layout == "neural_network":
            self.setup_neural_network_layout()
        elif self.current_layout == "command_center":
            self.setup_command_center_layout()
        else:
            self.setup_cyberpunk_split_layout()

    def setup_cyberpunk_split_layout(self):
        """Layout cyberpunk clásico con división vertical"""
        # Frame principal con degradado
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con información crítica
        header_frame = tk.Frame(main_frame, bg=self.bg_color, height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Título con estilo cyberpunk
        title_label = tk.Label(header_frame, text="◊ SYNTHEX NETRUNNER TERMINAL ◊", 
                              font=("Courier", 16, "bold"), fg=self.accent_color, bg=self.bg_color)
        title_label.pack(side=tk.TOP, pady=5)
        
        # Status y controles en línea
        status_line = tk.Frame(header_frame, bg=self.bg_color)
        status_line.pack(fill=tk.X, pady=5)
        
        # Panel de status izquierdo
        left_status = tk.Frame(status_line, bg=self.bg_color)
        left_status.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.integrity_label = tk.Label(left_status, text=f"[INTEGRITY: {self.system_integrity}%]", 
                                       font=("Courier", 10, "bold"), fg=self.get_integrity_color(), bg=self.bg_color)
        self.integrity_label.pack(side=tk.LEFT, padx=10)
        
        self.stealth_label = tk.Label(left_status, text=f"[STEALTH: {self.stealth_level}%]", 
                                     font=("Courier", 10, "bold"), fg="#00BFFF", bg=self.bg_color)
        self.stealth_label.pack(side=tk.LEFT, padx=10)
        
        self.threat_label = tk.Label(left_status, text=f"[THREAT: {self.get_stealth_status()}]", 
                                    font=("Courier", 10, "bold"), fg=self.accent_color, bg=self.bg_color)
        self.threat_label.pack(side=tk.LEFT, padx=10)
        
        # Controles derechos
        right_controls = tk.Frame(status_line, bg=self.bg_color)
        right_controls.pack(side=tk.RIGHT)
        
        # Layout selector
        tk.Label(right_controls, text="UI LAYOUT:", font=("Courier", 9), 
                fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        self.layout_var = tk.StringVar(value=self.current_layout)
        layout_combo = ttk.Combobox(right_controls, textvariable=self.layout_var, 
                                   values=["cyberpunk_split", "matrix_cascade", "holographic_hub", "neural_network", "command_center"], 
                                   state="readonly", width=15, font=("Courier", 8))
        layout_combo.pack(side=tk.LEFT, padx=5)
        layout_combo.bind('<<ComboboxSelected>>', self.change_layout)
        
        # Theme selector
        tk.Label(right_controls, text="THEME:", font=("Courier", 9), 
                fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=(15, 5))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(right_controls, textvariable=self.theme_var, 
                                  values=list(THEMES.keys()), state="readonly", width=10, font=("Courier", 8))
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Divisor visual
        separator = tk.Frame(main_frame, height=2, bg=self.accent_color)
        separator.pack(fill=tk.X, padx=10, pady=5)
        
        # Área principal dividida
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Visualizador (izquierda, 60%)
        viz_container = tk.Frame(content_frame, bg=self.bg_color)
        viz_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        viz_header = tk.Label(viz_container, text="▣ NETWORK VISUALIZATION ▣", 
                             font=("Courier", 12, "bold"), fg=self.accent_color, bg=self.bg_color)
        viz_header.pack(pady=(0, 5))
        
        viz_frame = tk.Frame(viz_container, bg=self.text_color, bd=2, relief=tk.RAISED)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(viz_frame, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Console (derecha, 40%)
        console_container = tk.Frame(content_frame, bg=self.bg_color, width=500)
        console_container.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        console_container.pack_propagate(False)
        
        console_header = tk.Label(console_container, text="▣ SYNTHEX CONSOLE ▣", 
                                 font=("Courier", 12, "bold"), fg=self.accent_color, bg=self.bg_color)
        console_header.pack(pady=(0, 5))
        
        console_frame = tk.Frame(console_container, bg=self.text_color, bd=2, relief=tk.RAISED)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console output
        self.console_output = tk.Text(console_frame, bg=self.bg_color, fg=self.accent_color, 
                                     font=("Courier", 9), state=tk.DISABLED, wrap=tk.WORD,
                                     insertbackground=self.accent_color)
        console_scrollbar = tk.Scrollbar(console_frame, command=self.console_output.yview, 
                                        bg=self.bg_color, troughcolor=self.bg_color)
        self.console_output.config(yscrollcommand=console_scrollbar.set)
        
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 2), pady=2)
        
        # Input area
        input_container = tk.Frame(console_container, bg=self.bg_color, height=40)
        input_container.pack(fill=tk.X, pady=(5, 0))
        input_container.pack_propagate(False)
        
        input_frame = tk.Frame(input_container, bg=self.text_color, bd=2, relief=tk.RAISED)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(input_frame, text=" >> ", bg=self.bg_color, fg=self.accent_color, 
                font=("Courier", 12, "bold")).pack(side=tk.LEFT, padx=2)
        
        self.console_input = tk.Entry(input_frame, bg=self.bg_color, fg=self.accent_color,
                                     font=("Courier", 11), insertbackground=self.accent_color, bd=0)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2), pady=2)
        self.console_input.bind('<Return>', self.process_console_command)
        
        # Footer con botones
        footer_frame = tk.Frame(main_frame, bg=self.bg_color, height=50)
        footer_frame.pack(fill=tk.X, padx=10, pady=5)
        footer_frame.pack_propagate(False)
        
        # Botones izquierda
        left_buttons = tk.Frame(footer_frame, bg=self.bg_color)
        left_buttons.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Button(left_buttons, text="CLEAR", command=self.clear_console, 
                 bg=self.accent_color, fg=self.bg_color, font=("Courier", 9, "bold"),
                 activebackground=self.text_color, bd=0, relief=tk.FLAT).pack(side=tk.LEFT, padx=2, ipadx=10)
        
        self.scan_btn = tk.Button(left_buttons, text="SCAN", command=self.system_scan,
                                 bg=self.text_color, fg=self.bg_color, font=("Courier", 9, "bold"),
                                 activebackground=self.accent_color, bd=0, relief=tk.FLAT)
        self.scan_btn.pack(side=tk.LEFT, padx=2, ipadx=10)
        
        self.reset_btn = tk.Button(left_buttons, text="RESET", command=self.emergency_reset,
                                  bg="#FF4444", fg=self.bg_color, font=("Courier", 9, "bold"),
                                  activebackground="#FF8888", bd=0, relief=tk.FLAT)
        self.reset_btn.pack(side=tk.LEFT, padx=2, ipadx=10)
        
        # Botones derecha
        right_buttons = tk.Frame(footer_frame, bg=self.bg_color)
        right_buttons.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(right_buttons, text="BACK", command=self.back_to_start_screen,
                 bg="#333333", fg=self.accent_color, font=("Courier", 9, "bold"),
                 activebackground="#555555", bd=0, relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=10)
        
        tk.Button(right_buttons, text="EXIT", command=self.on_close,
                 bg="#666666", fg=self.bg_color, font=("Courier", 9, "bold"),
                 activebackground="#888888", bd=0, relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=10)
        
        # Configurar tooltips y eventos
        self.canvas.bind('<Motion>', self.show_glyph_tooltip)
        self.canvas.bind('<Button-1>', self.on_glyph_click)
        
        # Desactivar botones si es pentester
        if self.mode == "pentester":
            self.scan_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.DISABLED)
        
        # Inicializar datos
        self.glyph_coords = {}
        self.current_glyphs = []
        self.glyph_constellation_map = {}

    def setup_matrix_cascade_layout(self):
        """Layout estilo Matrix con cascada de datos"""
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header minimalista
        header = tk.Frame(main_frame, bg=self.bg_color, height=60)
        header.pack(fill=tk.X, padx=5, pady=5)
        header.pack_propagate(False)
        
        tk.Label(header, text="◦◦◦ MATRIX INTERFACE ◦◦◦", font=("Courier", 14, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(expand=True)
        
        # Status compacto
        status_compact = tk.Frame(header, bg=self.bg_color)
        status_compact.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Crear labels de status
        self.integrity_label = tk.Label(status_compact, text=f"INT:{self.system_integrity}%", 
                                       font=("Courier", 8), fg=self.get_integrity_color(), bg=self.bg_color)
        self.integrity_label.pack(side=tk.LEFT, padx=5)
        
        self.stealth_label = tk.Label(status_compact, text=f"STL:{self.stealth_level}%", 
                                     font=("Courier", 8), fg="#00BFFF", bg=self.bg_color)
        self.stealth_label.pack(side=tk.LEFT, padx=5)
        
        self.threat_label = tk.Label(status_compact, text=f"THR:{self.get_stealth_status()}", 
                                    font=("Courier", 8), fg=self.accent_color, bg=self.bg_color)
        self.threat_label.pack(side=tk.LEFT, padx=5)
        
        # Controles a la derecha
        controls_frame = tk.Frame(status_compact, bg=self.bg_color)
        controls_frame.pack(side=tk.RIGHT)
        
        self.layout_var = tk.StringVar(value=self.current_layout)
        layout_combo = ttk.Combobox(controls_frame, textvariable=self.layout_var, 
                                   values=["cyberpunk_split", "matrix_cascade", "holographic_hub", "neural_network", "command_center"], 
                                   state="readonly", width=12, font=("Courier", 7))
        layout_combo.pack(side=tk.LEFT, padx=2)
        layout_combo.bind('<<ComboboxSelected>>', self.change_layout)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(controls_frame, textvariable=self.theme_var, 
                                  values=list(THEMES.keys()), state="readonly", width=8, font=("Courier", 7))
        theme_combo.pack(side=tk.LEFT, padx=2)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Área principal horizontal
        content = tk.Frame(main_frame, bg=self.bg_color)
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Console lado izquierdo (30%)
        console_side = tk.Frame(content, bg=self.accent_color, bd=1, relief=tk.SOLID, width=400)
        console_side.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        console_side.pack_propagate(False)
        
        self.console_output = tk.Text(console_side, bg=self.bg_color, fg=self.accent_color, 
                                     font=("Courier", 9), state=tk.DISABLED, wrap=tk.WORD,
                                     insertbackground=self.accent_color, bd=0)
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=1, pady=(1, 30))
        
        # Input en el console
        input_area = tk.Frame(console_side, bg=self.bg_color, height=30)
        input_area.pack(side=tk.BOTTOM, fill=tk.X, padx=1, pady=(0, 1))
        input_area.pack_propagate(False)
        
        tk.Label(input_area, text=">", bg=self.bg_color, fg=self.accent_color, 
                font=("Courier", 10, "bold")).pack(side=tk.LEFT, padx=2)
        self.console_input = tk.Entry(input_area, bg=self.bg_color, fg=self.accent_color,
                                     font=("Courier", 10), insertbackground=self.accent_color, bd=0)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.console_input.bind('<Return>', self.process_console_command)
        
        # Visualizador lado derecho (70%)
        viz_side = tk.Frame(content, bg=self.accent_color, bd=1, relief=tk.SOLID)
        viz_side.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.canvas = tk.Canvas(viz_side, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Footer con botones minimalistas
        footer = tk.Frame(main_frame, bg=self.bg_color, height=30)
        footer.pack(fill=tk.X, padx=5, pady=5)
        footer.pack_propagate(False)
        
        # Botones compactos
        btn_style = {"font": ("Courier", 8), "bd": 0, "relief": tk.FLAT, "bg": self.text_color, "fg": self.bg_color}
        
        tk.Button(footer, text="CLR", command=self.clear_console, **btn_style).pack(side=tk.LEFT, padx=1, ipadx=5)
        self.scan_btn = tk.Button(footer, text="SCN", command=self.system_scan, **btn_style)
        self.scan_btn.pack(side=tk.LEFT, padx=1, ipadx=5)
        self.reset_btn = tk.Button(footer, text="RST", command=self.emergency_reset, bg="#FF4444", fg=self.bg_color, **{k:v for k,v in btn_style.items() if k != 'bg'})
        self.reset_btn.pack(side=tk.LEFT, padx=1, ipadx=5)
        
        tk.Button(footer, text="EXIT", command=self.on_close, bg="#666666", **{k:v for k,v in btn_style.items() if k != 'bg'}).pack(side=tk.RIGHT, padx=1, ipadx=5)
        tk.Button(footer, text="BACK", command=self.back_to_start_screen, bg="#333333", **{k:v for k,v in btn_style.items() if k != 'bg'}).pack(side=tk.RIGHT, padx=1, ipadx=5)
        
        self.setup_common_bindings()

    def setup_holographic_hub_layout(self):
        """Layout futurista con disposición radial"""
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header circular
        header = tk.Frame(main_frame, bg=self.bg_color, height=70)
        header.pack(fill=tk.X, padx=10, pady=10)
        header.pack_propagate(False)
        
        tk.Label(header, text="◈ HOLOGRAPHIC INTERFACE ◈", font=("Courier", 16, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(anchor="center", pady=10)
        
        # Status en arco
        status_arc = tk.Frame(header, bg=self.bg_color)
        status_arc.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.integrity_label = tk.Label(status_arc, text=f"◦ INTEGRITY {self.system_integrity}% ◦", 
                                       font=("Courier", 9, "bold"), fg=self.get_integrity_color(), bg=self.bg_color)
        self.integrity_label.pack(side=tk.LEFT, expand=True)
        
        self.stealth_label = tk.Label(status_arc, text=f"◦ STEALTH {self.stealth_level}% ◦", 
                                     font=("Courier", 9, "bold"), fg="#00BFFF", bg=self.bg_color)
        self.stealth_label.pack(side=tk.LEFT, expand=True)
        
        self.threat_label = tk.Label(status_arc, text=f"◦ THREAT {self.get_stealth_status()} ◦", 
                                    font=("Courier", 9, "bold"), fg=self.accent_color, bg=self.bg_color)
        self.threat_label.pack(side=tk.LEFT, expand=True)
        
        # Centro con visualizador principal
        center_area = tk.Frame(main_frame, bg=self.bg_color)
        center_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Panel izquierdo para controles
        left_panel = tk.Frame(center_area, bg=self.text_color, bd=2, relief=tk.RAISED, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="◈ CONTROLS ◈", font=("Courier", 10, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(pady=10)
        
        # Selectores
        controls_inner = tk.Frame(left_panel, bg=self.bg_color)
        controls_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(controls_inner, text="LAYOUT:", font=("Courier", 8), fg=self.text_color, bg=self.bg_color).pack(pady=2)
        self.layout_var = tk.StringVar(value=self.current_layout)
        layout_combo = ttk.Combobox(controls_inner, textvariable=self.layout_var, 
                                   values=["cyberpunk_split", "matrix_cascade", "holographic_hub", "neural_network", "command_center"], 
                                   state="readonly", width=15, font=("Courier", 7))
        layout_combo.pack(pady=2)
        layout_combo.bind('<<ComboboxSelected>>', self.change_layout)
        
        tk.Label(controls_inner, text="THEME:", font=("Courier", 8), fg=self.text_color, bg=self.bg_color).pack(pady=(10, 2))
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(controls_inner, textvariable=self.theme_var, 
                                  values=list(THEMES.keys()), state="readonly", width=15, font=("Courier", 7))
        theme_combo.pack(pady=2)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Botones verticales
        btn_frame = tk.Frame(controls_inner, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=20)
        
        btn_style = {"font": ("Courier", 8, "bold"), "bd": 1, "relief": tk.RAISED, "bg": self.accent_color, "fg": self.bg_color}
        
        tk.Button(btn_frame, text="CLEAR", command=self.clear_console, **btn_style).pack(fill=tk.X, pady=2)
        self.scan_btn = tk.Button(btn_frame, text="SCAN", command=self.system_scan, **btn_style)
        self.scan_btn.pack(fill=tk.X, pady=2)
        self.reset_btn = tk.Button(btn_frame, text="RESET", command=self.emergency_reset, bg="#FF4444", **{k:v for k,v in btn_style.items() if k != 'bg'})
        self.reset_btn.pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="BACK", command=self.back_to_start_screen, bg="#333333", **{k:v for k,v in btn_style.items() if k != 'bg'}).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="EXIT", command=self.on_close, bg="#666666", **{k:v for k,v in btn_style.items() if k != 'bg'}).pack(fill=tk.X, pady=2)
        
        # Visualizador central
        viz_center = tk.Frame(center_area, bg=self.text_color, bd=3, relief=tk.RAISED)
        viz_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(viz_center, text="◈ NETWORK HUB ◈", font=("Courier", 12, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(pady=5)
        
        self.canvas = tk.Canvas(viz_center, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=3, pady=(0, 3))
        
        # Console derecho
        console_right = tk.Frame(center_area, bg=self.text_color, bd=2, relief=tk.RAISED, width=300)
        console_right.pack(side=tk.RIGHT, fill=tk.Y)
        console_right.pack_propagate(False)
        
        tk.Label(console_right, text="◈ TERMINAL ◈", font=("Courier", 10, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(pady=5)
        
        self.console_output = tk.Text(console_right, bg=self.bg_color, fg=self.accent_color, 
                                     font=("Courier", 8), state=tk.DISABLED, wrap=tk.WORD,
                                     insertbackground=self.accent_color, bd=0)
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=3, pady=(0, 30))
        
        # Input terminal
        input_terminal = tk.Frame(console_right, bg=self.bg_color, height=30)
        input_terminal.pack(side=tk.BOTTOM, fill=tk.X, padx=3, pady=(0, 3))
        input_terminal.pack_propagate(False)
        
        tk.Label(input_terminal, text="◈", bg=self.bg_color, fg=self.accent_color, 
                font=("Courier", 10, "bold")).pack(side=tk.LEFT)
        self.console_input = tk.Entry(input_terminal, bg=self.bg_color, fg=self.accent_color,
                                     font=("Courier", 9), insertbackground=self.accent_color, bd=0)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.console_input.bind('<Return>', self.process_console_command)
        
        self.setup_common_bindings()

    def setup_neural_network_layout(self):
        """Layout inspirado en redes neuronales"""
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header neural
        header = tk.Frame(main_frame, bg=self.bg_color, height=50)
        header.pack(fill=tk.X, padx=5, pady=5)
        header.pack_propagate(False)
        
        tk.Label(header, text="◊◊◊ NEURAL NETWORK INTERFACE ◊◊◊", font=("Courier", 14, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(expand=True)
        
        # Grid de información
        info_grid = tk.Frame(main_frame, bg=self.bg_color, height=80)
        info_grid.pack(fill=tk.X, padx=5, pady=(0, 5))
        info_grid.pack_propagate(False)
        
        # Dividir en 3 columnas
        for i in range(3):
            info_grid.columnconfigure(i, weight=1)
        
        # Status nodes
        node1 = tk.Frame(info_grid, bg=self.text_color, bd=2, relief=tk.RAISED)
        node1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.integrity_label = tk.Label(node1, text=f"INTEGRITY\n{self.system_integrity}%", 
                                       font=("Courier", 9, "bold"), fg=self.get_integrity_color(), bg=self.bg_color)
        self.integrity_label.pack(expand=True, pady=5)
        
        node2 = tk.Frame(info_grid, bg=self.text_color, bd=2, relief=tk.RAISED)
        node2.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.stealth_label = tk.Label(node2, text=f"STEALTH\n{self.stealth_level}%", 
                                     font=("Courier", 9, "bold"), fg="#00BFFF", bg=self.bg_color)
        self.stealth_label.pack(expand=True, pady=5)
        
        node3 = tk.Frame(info_grid, bg=self.text_color, bd=2, relief=tk.RAISED)
        node3.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.threat_label = tk.Label(node3, text=f"THREAT\n{self.get_stealth_status()}", 
                                    font=("Courier", 9, "bold"), fg=self.accent_color, bg=self.bg_color)
        self.threat_label.pack(expand=True, pady=5)
        
        # Controls row
        control_row = tk.Frame(info_grid, bg=self.bg_color)
        control_row.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        
        tk.Label(control_row, text="LAYOUT:", font=("Courier", 8), fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.layout_var = tk.StringVar(value=self.current_layout)
        layout_combo = ttk.Combobox(control_row, textvariable=self.layout_var, 
                                   values=["cyberpunk_split", "matrix_cascade", "holographic_hub", "neural_network", "command_center"], 
                                   state="readonly", width=12, font=("Courier", 7))
        layout_combo.pack(side=tk.LEFT, padx=5)
        layout_combo.bind('<<ComboboxSelected>>', self.change_layout)
        
        tk.Label(control_row, text="THEME:", font=("Courier", 8), fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(control_row, textvariable=self.theme_var, 
                                  values=list(THEMES.keys()), state="readonly", width=10, font=("Courier", 7))
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Main workspace
        workspace = tk.Frame(main_frame, bg=self.bg_color)
        workspace.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Visualizador principal (arriba, 60%)
        viz_main = tk.Frame(workspace, bg=self.text_color, bd=2, relief=tk.RAISED)
        viz_main.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        viz_header = tk.Label(viz_main, text="◊ NEURAL VISUALIZATION ◊", font=("Courier", 11, "bold"),
                             fg=self.accent_color, bg=self.bg_color)
        viz_header.pack(pady=3)
        
        self.canvas = tk.Canvas(viz_main, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
        
        # Console abajo (40%)
        console_bottom = tk.Frame(workspace, bg=self.text_color, bd=2, relief=tk.RAISED, height=200)
        console_bottom.pack(fill=tk.X, pady=(5, 0))
        console_bottom.pack_propagate(False)
        
        console_header = tk.Label(console_bottom, text="◊ NEURAL CONSOLE ◊", font=("Courier", 11, "bold"),
                                 fg=self.accent_color, bg=self.bg_color)
        console_header.pack(pady=3)
        
        # Console content
        console_content = tk.Frame(console_bottom, bg=self.bg_color)
        console_content.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
        
        self.console_output = tk.Text(console_content, bg=self.bg_color, fg=self.accent_color, 
                                     font=("Courier", 9), state=tk.DISABLED, wrap=tk.WORD,
                                     insertbackground=self.accent_color, bd=0, height=8)
        console_scroll = tk.Scrollbar(console_content, command=self.console_output.yview)
        self.console_output.config(yscrollcommand=console_scroll.set)
        
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Input y botones
        bottom_controls = tk.Frame(console_bottom, bg=self.bg_color, height=30)
        bottom_controls.pack(fill=tk.X, padx=2, pady=(0, 2))
        bottom_controls.pack_propagate(False)
        
        # Input lado izquierdo
        input_side = tk.Frame(bottom_controls, bg=self.bg_color)
        input_side.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(input_side, text="◊", bg=self.bg_color, fg=self.accent_color, 
                font=("Courier", 12, "bold")).pack(side=tk.LEFT)
        self.console_input = tk.Entry(input_side, bg=self.bg_color, fg=self.accent_color,
                                     font=("Courier", 10), insertbackground=self.accent_color, bd=1)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.console_input.bind('<Return>', self.process_console_command)
        
        # Botones lado derecho
        buttons_side = tk.Frame(bottom_controls, bg=self.bg_color)
        buttons_side.pack(side=tk.RIGHT)
        
        btn_style = {"font": ("Courier", 7), "bd": 1, "relief": tk.RAISED, "bg": self.accent_color, "fg": self.bg_color}
        tk.Button(buttons_side, text="CLR", command=self.clear_console, **btn_style).pack(side=tk.LEFT, padx=1)
        self.scan_btn = tk.Button(buttons_side, text="SCN", command=self.system_scan, **btn_style)
        self.scan_btn.pack(side=tk.LEFT, padx=1)
        self.reset_btn = tk.Button(buttons_side, text="RST", command=self.emergency_reset, bg="#FF4444", **{k:v for k,v in btn_style.items() if k != 'bg'})
        self.reset_btn.pack(side=tk.LEFT, padx=1)
        tk.Button(buttons_side, text="BACK", command=self.back_to_start_screen, bg="#333333", **{k:v for k,v in btn_style.items() if k != 'bg'}).pack(side=tk.LEFT, padx=1)
        tk.Button(buttons_side, text="EXIT", command=self.on_close, bg="#666666", **{k:v for k,v in btn_style.items() if k != 'bg'}).pack(side=tk.LEFT, padx=1)
        
        self.setup_common_bindings()

    def setup_command_center_layout(self):
        """Layout estilo centro de comando militar"""
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header de comando
        header = tk.Frame(main_frame, bg=self.bg_color, height=80)
        header.pack(fill=tk.X, padx=10, pady=10)
        header.pack_propagate(False)
        
        tk.Label(header, text="▣▣▣ COMMAND CENTER ▣▣▣", font=("Courier", 18, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(pady=10)
        
        # Status bar estilo militar
        status_bar = tk.Frame(header, bg=self.text_color, bd=2, relief=tk.SUNKEN, height=30)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        status_bar.pack_propagate(False)
        
        status_inner = tk.Frame(status_bar, bg=self.bg_color)
        status_inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.integrity_label = tk.Label(status_inner, text=f"▣ SYSTEM INTEGRITY: {self.system_integrity}% ▣", 
                                       font=("Courier", 10, "bold"), fg=self.get_integrity_color(), bg=self.bg_color)
        self.integrity_label.pack(side=tk.LEFT, padx=10)
        
        self.stealth_label = tk.Label(status_inner, text=f"▣ STEALTH LEVEL: {self.stealth_level}% ▣", 
                                     font=("Courier", 10, "bold"), fg="#00BFFF", bg=self.bg_color)
        self.stealth_label.pack(side=tk.LEFT, padx=10)
        
        self.threat_label = tk.Label(status_inner, text=f"▣ THREAT STATUS: {self.get_stealth_status()} ▣", 
                                    font=("Courier", 10, "bold"), fg=self.accent_color, bg=self.bg_color)
        self.threat_label.pack(side=tk.LEFT, padx=10)
        
        # Controls en header
        controls_header = tk.Frame(status_inner, bg=self.bg_color)
        controls_header.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(controls_header, text="UI:", font=("Courier", 8, "bold"), fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT)
        self.layout_var = tk.StringVar(value=self.current_layout)
        layout_combo = ttk.Combobox(controls_header, textvariable=self.layout_var, 
                                   values=["cyberpunk_split", "matrix_cascade", "holographic_hub", "neural_network", "command_center"], 
                                   state="readonly", width=10, font=("Courier", 7))
        layout_combo.pack(side=tk.LEFT, padx=2)
        layout_combo.bind('<<ComboboxSelected>>', self.change_layout)
        
        tk.Label(controls_header, text="THM:", font=("Courier", 8, "bold"), fg=self.text_color, bg=self.bg_color).pack(side=tk.LEFT, padx=(5, 0))
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(controls_header, textvariable=self.theme_var, 
                                  values=list(THEMES.keys()), state="readonly", width=8, font=("Courier", 7))
        theme_combo.pack(side=tk.LEFT, padx=2)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Main command area
        command_area = tk.Frame(main_frame, bg=self.bg_color)
        command_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Izquierda: console y controles (40%)
        left_command = tk.Frame(command_area, bg=self.bg_color, width=500)
        left_command.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_command.pack_propagate(False)
        
        # Console principal
        console_frame = tk.Frame(left_command, bg=self.text_color, bd=3, relief=tk.RAISED)
        console_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        console_title = tk.Label(console_frame, text="▣ COMMAND TERMINAL ▣", font=("Courier", 12, "bold"),
                                fg=self.accent_color, bg=self.bg_color)
        console_title.pack(pady=5)
        
        self.console_output = tk.Text(console_frame, bg=self.bg_color, fg=self.accent_color, 
                                     font=("Courier", 9), state=tk.DISABLED, wrap=tk.WORD,
                                     insertbackground=self.accent_color, bd=0)
        console_scroll = tk.Scrollbar(console_frame, command=self.console_output.yview,
                                     bg=self.bg_color, troughcolor=self.bg_color)
        self.console_output.config(yscrollcommand=console_scroll.set)
        
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=(0, 35))
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 3), pady=(0, 35))
        
        # Input command
        input_command = tk.Frame(console_frame, bg=self.bg_color, height=30)
        input_command.pack(side=tk.BOTTOM, fill=tk.X, padx=3, pady=(0, 3))
        input_command.pack_propagate(False)
        
        tk.Label(input_command, text="CMD▣", bg=self.bg_color, fg=self.accent_color, 
                font=("Courier", 11, "bold")).pack(side=tk.LEFT, padx=2)
        self.console_input = tk.Entry(input_command, bg=self.bg_color, fg=self.accent_color,
                                     font=("Courier", 10), insertbackground=self.accent_color, bd=1, relief=tk.SUNKEN)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        self.console_input.bind('<Return>', self.process_console_command)
        
        # Panel de botones
        button_panel = tk.Frame(left_command, bg=self.text_color, bd=3, relief=tk.RAISED, height=80)
        button_panel.pack(fill=tk.X)
        button_panel.pack_propagate(False)
        
        button_grid = tk.Frame(button_panel, bg=self.bg_color)
        button_grid.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Grid de botones 2x3
        btn_style = {"font": ("Courier", 9, "bold"), "bd": 2, "relief": tk.RAISED, "bg": self.accent_color, "fg": self.bg_color}
        
        tk.Button(button_grid, text="CLEAR", command=self.clear_console, **btn_style).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        self.scan_btn = tk.Button(button_grid, text="SCAN", command=self.system_scan, **btn_style)
        self.scan_btn.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        self.reset_btn = tk.Button(button_grid, text="RESET", command=self.emergency_reset, bg="#FF4444", **{k:v for k,v in btn_style.items() if k != 'bg'})
        self.reset_btn.grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        
        tk.Button(button_grid, text="BACK", command=self.back_to_start_screen, bg="#333333", **{k:v for k,v in btn_style.items() if k != 'bg'}).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        tk.Button(button_grid, text="EXIT", command=self.on_close, bg="#666666", **{k:v for k,v in btn_style.items() if k != 'bg'}).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        
        # Configurar grid
        for i in range(3):
            button_grid.columnconfigure(i, weight=1)
        
        # Derecha: visualizador principal (60%)
        right_display = tk.Frame(command_area, bg=self.text_color, bd=3, relief=tk.RAISED)
        right_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        display_title = tk.Label(right_display, text="▣ TACTICAL DISPLAY ▣", font=("Courier", 14, "bold"),
                                fg=self.accent_color, bg=self.bg_color)
        display_title.pack(pady=10)
        
        self.canvas = tk.Canvas(right_display, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=3, pady=(0, 3))
        
        self.setup_common_bindings()

    def setup_common_bindings(self):
        """Configura eventos comunes para todos los layouts"""
        self.canvas.bind('<Motion>', self.show_glyph_tooltip)
        self.canvas.bind('<Button-1>', self.on_glyph_click)
        
        if self.mode == "pentester":
            self.scan_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.DISABLED)
        
        self.glyph_coords = {}
        self.current_glyphs = []
        self.glyph_constellation_map = {}

    def change_layout(self, event=None):
        """Cambia el layout de la interfaz"""
        selected_layout = self.layout_var.get()
        if selected_layout != self.current_layout:
            self._save_terminal_state()
            self.current_layout = selected_layout
            self.setup_ui()
            self._restore_terminal_state()

    def get_integrity_color(self):
        """Devuelve el color apropiado según la integridad"""
        if self.system_integrity >= 80:
            return "#00FF00"
        elif self.system_integrity >= 50:
            return "#FFFF00"
        elif self.system_integrity >= 20:
            return "#FF8800"
        else:
            return "#FF0000"

    def back_to_start_screen(self):
        # Clear all widgets from the root window
        for widget in self.winfo_children():
            widget.destroy()
        self.start_screen()
        # Para reiniciar la app desde cero, podrías usar os.execl o similar si lo deseas
      
        # Para reiniciar la app desde cero, podrías usar os.execl o similar si lo deseas
        
    def write_to_console(self, text, color=None):
        """Escribe texto en la consola"""
        self.console_output.config(state=tk.NORMAL)
        if color is None:
            color = self.accent_color
        
        # Agregar timestamp
        timestamp = time.strftime("[%H:%M:%S] ")
        self.console_output.insert(tk.END, timestamp, 'timestamp')
        self.console_output.insert(tk.END, text + "\n", 'normal')
        
        # Configurar colores
        self.console_output.tag_config('timestamp', foreground=self.text_color)
        self.console_output.tag_config('normal', foreground=color)
        
        self.console_output.config(state=tk.DISABLED)
        self.console_output.see(tk.END)

    def process_console_command(self, event):
        """Procesa comandos ingresados en la consola"""
        command = self.console_input.get().strip().lower()
        self.console_input.delete(0, tk.END)
        
        if not command:
            return

        self.write_to_console(f">> {command}", self.text_color)
        self.console_history.append(command)

        # Comandos y elementos permitidos en modo pentester
        pentester_commands = [
            # MALWARE CLASSIFICATIONS
            "virus", "worm", "trojan", "ransomware", "spyware", "malware", "keylogger",
            # ATTACK SIMULATION
            "breach", "corrupt", "probe", "exploit",
            # EXPLOITATION TOOLS
            "exploit", "backdoor", "root", "admin", "botnet",
        ]
        pentester_elements = [
            "message", "network", "encrypt", "decrypt", "link", "system", "code", "data",
            "firewall", "security", "breach", "interface", "core"
        ]

        # Comandos con argumentos
        pentester_prefixes = [
            "breach ", "corrupt ", "probe ", "exploit ",
        ]

        # Procesar comandos especiales
        if command == "help":
            self.show_help()
        elif command == "man":
            self.show_manual()
        elif command == "alpha":
            self.show_synthex_alphabet()
        elif command == "enc":
            self.show_encryption_view()
        elif command == "dec":
            self.show_decryption_view()
        elif command == "clear":
            self.clear_console()
        elif command == "status":
            self.show_system_status()
        elif command == "scan":
            if self.mode == "pentester":
                self.write_to_console("[!] 'scan' command is disabled in pentester mode.", "#FF4444")
            else:
                self.system_scan()
        elif command == "reset":
            if self.mode == "pentester":
                self.write_to_console("[!] Emergency reset is blocked during pentester operations.", "#FF4444")
            else:
                self.emergency_reset()
        elif command == "test":
            if self.mode == "pentester":
                self.write_to_console("[!] 'test' is not available in pentester mode.", "#FF4444")
            else:
                self.visualize_constellations()
                self.write_to_console("Displaying all Synthex glyphs in constellations...", "#FFFF00")
        elif command.startswith("theme "):
            theme_name = command.split(" ", 1)[1]
            if theme_name in THEMES:
                self.current_theme = theme_name
                self.theme_var.set(theme_name)
                self.change_theme()
        elif command.startswith("encrypt "):
            text = command.split(" ", 1)[1]
            self.encrypt_text(text)
        elif command.startswith("decrypt "):
            synthex_text = command.split(" ", 1)[1]
            self.decrypt_text(synthex_text)
        # Reconocimiento de comandos y elementos pentester
        elif self.mode == "pentester" and (
            command in pentester_commands
            or command in pentester_elements
            or any(command.startswith(prefix) for prefix in pentester_prefixes)
        ):
            pass  # Comando reconocido, no hacer nada aún
        elif self.mode == "pentester":
            # Solo permitir ataques con el nuevo sistema: 'dp <malware>'
            if command.startswith("dp "):
                malware = command[3:].strip()
                if malware in self.MALWARE_STATS:
                    self.malware_attack(malware)
                else:
                    self.write_to_console(f"[!] '{malware}' is not a valid malware type.", "#FF4444")
            # No ejecutar ataques para otros comandos
            return
        else:
            # Procesar como encriptación normal
            self.encrypt_text(command)

    def is_attack_command(self, command):
        """Verifica si el comando es un ataque simulado"""
        attack_words = ["breach", "corrupt", "probe", "exploit", "virus", "worm", "trojan"]
        return any(word in command for word in attack_words)

    def simulate_attack(self, command):
        """Simula un ataque cibernético"""
        words = command.split()
        attack_type = None
        
        for word in words:
            if word in ["breach", "corrupt", "probe", "exploit", "virus", "worm", "trojan"]:
                attack_type = word
                break
        
        if attack_type:
            self.write_to_console(f"INITIATING {attack_type.upper()} SEQUENCE...", "#FF4400")
            
            # Simular riesgo
            risk = random.randint(1, 100)
            if risk > 70:  # 30% chance de éxito
                self.write_to_console("ATTACK SUCCESSFUL - SYSTEM COMPROMISED", "#FF0000")
                self.system_integrity = max(0, self.system_integrity - random.randint(10, 30))
                self.threat_level = min(100, self.threat_level + random.randint(20, 50))
                self.generate_trace()
            else:
                self.write_to_console("ATTACK BLOCKED - FIREWALL ACTIVE", "#00FF00")
                self.write_to_console("Generating counter-trace...", "#FFFF00")
                
            self.update_system_status()
            self.encrypt_text(command)  # También mostrar la representación Synthex

    def generate_trace(self):
        """Genera un trace hostil"""
        self.write_to_console("WARNING: HOSTILE TRACE DETECTED", "#FF0000")
        trace_commands = ["trace", "probe", "corrupt", "breach"]
        hostile_command = random.choice(trace_commands)
        self.write_to_console(f"Hostile entity executing: {hostile_command}", "#FF4400")

    def encrypt_text(self, text):
        """Encripta texto a Synthex y lo visualiza"""
        words = text.split()
        synthex_glyphs = []
        
        for word in words:
            glyph = SYNTHEX_DICTIONARY.get(word, UNKNOWN_GLYPH)
            synthex_glyphs.append(glyph)
        
        synthex_network = "—".join(synthex_glyphs)
        self.write_to_console(f"SYNTHEX: {synthex_network}", "#00FFFF")
        
        self.visualize_synthex_network(synthex_glyphs, text)

    def decrypt_text(self, synthex_text):
        """Desencripta texto Synthex"""
        glyphs = synthex_text.split("—")
        plain_words = []
        
        for glyph in glyphs:
            word = REV_SYNTHEX_DICTIONARY.get(glyph, f"[{glyph}?]")
            plain_words.append(word)
        
        plain_text = " ".join(plain_words)
        self.write_to_console(f"DECRYPTED: {plain_text}", "#00FF00")
        
        self.visualize_synthex_network(glyphs, plain_text)

    def show_help(self):
        """Muestra ayuda de comandos"""
        help_text = """
AVAILABLE COMMANDS:
  help          - Show this help
  man           - Show Synthex manual
  clear         - Clear console
  status        - Show system status
  scan          - Perform system scan
  reset         - Emergency system reset
  theme <name>  - Change theme (classic, ice, fire, matrix, neon)
  test          - Display all glyph constellations
  encrypt <text>- Encrypt text to Synthex
  decrypt <code>- Decrypt Synthex code
  alpha         - Show synthex dictionary
  enc           - Dedicated encryption system
  dec           - Dedicated decryption system
  
ATTACK SIMULATION:
  breach <target>  - Attempt system breach
  corrupt <target> - Corrupt data
  probe <target>   - Probe system
  exploit <vuln>   - Exploit vulnerability
        """
        self.write_to_console(help_text, "#FFFF00")

    def show_system_status(self):
        """Muestra estado detallado del sistema"""
        status_text = f"""
SYSTEM STATUS REPORT:
  Integrity: {self.system_integrity}%
  Threat Level: {self.threat_level}%
  Active Processes: {len(self.active_processes)}
  Console History: {len(self.console_history)} commands
  Theme: {self.current_theme}
        """
        color = "#00FF00" if self.system_integrity > 70 else "#FF4400"
        self.write_to_console(status_text, color)

    def update_system_status(self):
        """Actualiza los labels de estado y verifica el estado crítico"""
        self.integrity_label.config(text=f"Integrity: {self.system_integrity}%")
        
        if self.threat_level == 0:
            threat_text = "SECURE"
            color = "#00FF00"
        elif self.threat_level < 30:
            threat_text = "LOW"
            color = "#FFFF00"
        elif self.threat_level < 70:
            threat_text = "MEDIUM"
            color = "#FF8800"
        else:
            threat_text = "CRITICAL"
            color = "#FF0000"
        
        self.threat_label.config(text=f"Threat: {threat_text}", fg=color)
        
        # --- Lógica de Blackwall ---
        if self.system_integrity <= 0:
            self.show_blackwall()
            self.console_input.config(state=tk.DISABLED)

    def system_scan(self):
        """Simula un escaneo del sistema"""
        self.write_to_console("Initiating system scan...", "#FFFF00")
        
        def scan_process():
            scan_items = ["Memory sectors", "Network interfaces", "Security protocols", 
                         "Data integrity", "Threat signatures"]
            
            for item in scan_items:
                time.sleep(0.5)
                self.after(0, lambda i=item: self.write_to_console(f"Scanning {i}...", "#00FFFF"))
            
            threats_found = random.randint(0, 3)
            self.after(0, lambda: self.write_to_console(f"Scan complete. {threats_found} potential threats detected.", "#00FF00"))
            
            if threats_found > 0:
                self.threat_level = min(100, self.threat_level + threats_found * 10)
                self.after(0, self.update_system_status)
        
        threading.Thread(target=scan_process, daemon=True).start()

    def emergency_reset(self):
        """Reset de emergencia del sistema"""
        if messagebox.askyesno("Emergency Reset", "This will reset all system parameters. Continue?"):
            self.system_integrity = 100
            self.threat_level = 0
            self.active_processes.clear()
            self.update_system_status()
            self.write_to_console("EMERGENCY RESET COMPLETE - ALL SYSTEMS RESTORED", "#00FF00")
            self.canvas.delete("all")
            self.console_input.config(state=tk.NORMAL)
            self.visualize_synthex_network(self.current_glyphs)

    def change_theme(self, event=None):
        """Cambia el tema y reinicia la interfaz, preservando la consola y la visualización actual."""
        selected_theme = self.theme_var.get()
        if selected_theme != self.current_theme:
            # Guarda el estado completo antes de cambiar el tema
            self._save_terminal_state()
            self.current_theme = selected_theme
            self.apply_theme()

            # Destruye todos los widgets y reconstruye la interfaz principal
            for widget in self.winfo_children():
                widget.destroy()
            self.setup_ui()

            # Restaura el historial de la consola
            if hasattr(self, "_saved_console") and hasattr(self, "console_output"):
                self.console_output.config(state=tk.NORMAL)
                self.console_output.delete("1.0", tk.END)
                self.console_output.insert("1.0", self._saved_console)
                self.console_output.config(state=tk.DISABLED)
                self.console_output.see(tk.END)

            # Restaura la visualización de los glifos
            if hasattr(self, "_saved_glyphs") and self._saved_glyphs and hasattr(self, "canvas"):
                self.visualize_synthex_network(self._saved_glyphs)

            # Restaura integridad y amenaza
            if hasattr(self, "_saved_integrity"):
                self.system_integrity = self._saved_integrity
            if hasattr(self, "_saved_threat"):
                self.threat_level = self._saved_threat
            self.update_system_status()

            # --- Restaurar estados especiales de pentester ---
            if self.mode == "pentester":
                if SynthexTerminalEnhanced.pentester_integrity is not None:
                    self.system_integrity = SynthexTerminalEnhanced.pentester_integrity
                if SynthexTerminalEnhanced.pentester_stealth_level is not None:
                    self.stealth_level = SynthexTerminalEnhanced.pentester_stealth_level
                if SynthexTerminalEnhanced.pentester_stealth_status is not None and hasattr(self, "threat_label"):
                    self.threat_label.config(text=SynthexTerminalEnhanced.pentester_stealth_status)
                self.update_status_labels()

            # Restaura historial y procesos
            if hasattr(self, "_saved_history"):
                self.console_history = list(self._saved_history)
            if hasattr(self, "_saved_processes"):
                self.active_processes = list(self._saved_processes)

            # Actualiza los labels de estado si existen
            if hasattr(self, "integrity_label"):
                self.integrity_label.config(bg=self.bg_color, fg=self.accent_color)
            if hasattr(self, "threat_label"):
                self.threat_label.config(bg=self.bg_color)
            self.write_to_console(f"Theme changed to: {self.current_theme}", "#FFFF00")

    def clear_console(self):
        """Limpia la consola"""
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete(1.0, tk.END)
        self.console_output.config(state=tk.DISABLED)
        self.write_to_console("Console cleared.")
    
    def on_close(self):
        """Maneja el cierre de la ventana"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.destroy()

    def show_synthex_alphabet(self):
        """Muestra el alfabeto Synthex en una cuadrícula con una instrucción para cerrar."""
        self.current_view = "alphabet"
        # --- GUARDAR ESTADO ANTES DE CAMBIAR DE VISTA ---
        self._save_terminal_state()

        # Limpiar la vista actual del programa
        for widget in self.winfo_children():
            widget.destroy()

        # Frame contenedor para la nueva vista del alfabeto
        self.alphabet_frame = tk.Frame(self, bg=self.bg_color, padx=10, pady=10)
        self.alphabet_frame.pack(fill=tk.BOTH, expand=True)

        # Título de la vista
        tk.Label(self.alphabet_frame, text="SYNTHEX ALPHABET", font=("Courier", 24, "bold"),
                fg=self.accent_color, bg=self.bg_color).pack(pady=10)

        # Etiqueta que funciona como botón para cerrar
        close_advisor = tk.Label(self.alphabet_frame, text="< Click to close >", font=("Courier", 10),
                                bg=self.bg_color, fg=self.text_color, cursor="hand2")
        close_advisor.pack(pady=(0, 10))
        close_advisor.bind("<Button-1>", lambda e: self.return_to_terminal_restore())

        # Frame para la cuadrícula de pictogramas
        grid_container = tk.Frame(self.alphabet_frame, bg=self.bg_color)
        grid_container.pack(fill=tk.BOTH, expand=True, pady=10)

        num_columns = 8
        current_row = 0
        current_col = 0

        sorted_keys = sorted(SYNTHEX_DICTIONARY.keys())

        for word in sorted_keys:
            glyph = SYNTHEX_DICTIONARY[word]

            cell_frame = tk.Frame(grid_container, bg=self.bg_color, bd=2, relief=tk.SOLID)
            cell_frame.grid(row=current_row, column=current_col, padx=5, pady=5, sticky="nsew")

            word_label = tk.Label(cell_frame, text=word.upper(), font=("Courier", 12),
                                bg=self.bg_color, fg=self.text_color)
            word_label.pack(pady=(5, 0))

            glyph_label = tk.Label(cell_frame, text=glyph, font=("Courier", 40),
                                bg=self.bg_color, fg=self.accent_color)
            glyph_label.pack(pady=(0, 5))

            current_col += 1
            if current_col >= num_columns:
                current_col = 0
                current_row += 1

        for i in range(num_columns):
            grid_container.columnconfigure(i, weight=1)
        for i in range(current_row + 1):
            grid_container.rowconfigure(i, weight=1)

    def return_to_terminal_restore(self):
        """Destruye la vista del alfabeto y regresa a la pantalla de la terminal restaurando el estado previo."""
        if hasattr(self, 'alphabet_frame') and self.alphabet_frame:
            self.alphabet_frame.destroy()
        # Si el warning ASCII está activo, desactívalo y restaura la red
        self._ascii_warning_active = False
        self._restore_terminal_state()

    def show_encryption_view(self):
        """Muestra una interfaz de encriptación con un estilo más cyberpunk."""
        self.current_view = "encryption"
        # --- GUARDAR ESTADO ANTES DE CAMBIAR DE VISTA ---
        self._save_terminal_state()

        # Detener la animación de la terminal si está activa
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        # Limpiar la vista actual del programa
        for widget in self.winfo_children():
            widget.destroy()

        # Frame contenedor principal para la nueva vista de encriptación
        self.encryption_frame = tk.Frame(self, bg=self.bg_color, padx=20, pady=20)
        self.encryption_frame.pack(fill=tk.BOTH, expand=True)

        # Configuración de la cuadrícula
        self.encryption_frame.columnconfigure(0, weight=1)
        self.encryption_frame.columnconfigure(1, weight=1)

        # Título de la vista
        title_label = tk.Label(self.encryption_frame, text="SYNTHEX ENCRYPTION TOOL", font=("Courier", 24, "bold"),
                               fg=self.accent_color, bg=self.bg_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # Etiqueta para cerrar (advisor)
        close_advisor = tk.Label(self.encryption_frame, text="< CLICK TO CLOSE >", font=("Courier", 10, "italic"),
                                 bg=self.bg_color, fg="#5D6064", cursor="hand2")
        close_advisor.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        close_advisor.bind("<Button-1>", lambda e: self.return_to_terminal_restore())

        # Frame para la entrada
        input_frame = tk.LabelFrame(self.encryption_frame, text="MESSAGE TO ENCRYPT:", font=("Courier", 12),
                                    fg=self.text_color, bg=self.bg_color, bd=2, relief=tk.SOLID)
        input_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="nsew")
        
        self.input_text_area = tk.Text(input_frame, bg="#0E0E0E", fg="#00FF00", font=("Courier", 12),
                                     height=8, insertbackground="#00FF00", relief=tk.FLAT, bd=0)
        self.input_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para los botones
        button_frame = tk.Frame(self.encryption_frame, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))

        tk.Button(button_frame, text="ENCRYPT", command=self.encrypt_message,
                  bg=self.accent_color, fg=self.bg_color, font=("Courier", 12, "bold"),
                  activebackground=self.text_color, activeforeground=self.bg_color,
                  bd=0, relief=tk.FLAT).pack(side=tk.LEFT, padx=10, ipadx=20)
        
        tk.Button(button_frame, text="COPY", command=self.copy_encrypted,
                  bg=self.text_color, fg=self.bg_color, font=("Courier", 12, "bold"),
                  activebackground=self.accent_color, activeforeground=self.bg_color,
                  bd=0, relief=tk.FLAT).pack(side=tk.LEFT, padx=10, ipadx=20)

        # Frame para la salida
        output_frame = tk.LabelFrame(self.encryption_frame, text="ENCRYPTED GLYPHS:", font=("Courier", 12),
                                     fg=self.text_color, bg=self.bg_color, bd=2, relief=tk.SOLID)
        output_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="nsew")
        
        self.output_text_area = tk.Text(output_frame, bg="#0E0E0E", fg="#00FFFF", font=("Courier", 24),
                                      height=5, wrap="word", relief=tk.FLAT, bd=0)
        self.output_text_area.config(state=tk.DISABLED)
        self.output_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def encrypt_message(self):
        """Toma el texto de entrada y lo encripta en pictogramas Synthex, separados por un guion."""
        input_text = self.input_text_area.get("1.0", tk.END).strip().lower()
        words = input_text.split()
        encrypted_glyphs = []
        
        for word in words:
            if word in SYNTHEX_DICTIONARY:
                encrypted_glyphs.append(SYNTHEX_DICTIONARY[word])
            else:
                encrypted_glyphs.append(f"[UNK_WORD]")
        
        encrypted_text = "—".join(encrypted_glyphs)
        
        self.output_text_area.config(state=tk.NORMAL)
        self.output_text_area.delete("1.0", tk.END)
        self.output_text_area.insert("1.0", encrypted_text)
        self.output_text_area.config(state=tk.DISABLED)

    def copy_encrypted(self):
        """Copia el texto encriptado al portapapeles."""
        encrypted_text = self.output_text_area.get("1.0", tk.END).strip()
        if encrypted_text:
            self.clipboard_clear()
            self.clipboard_append(encrypted_text)
            # Si existe console_status, mostrar mensaje
            if hasattr(self, "console_status"):
                self.console_status.config(text="Encrypted message copied to clipboard.")
                self.after(2000, lambda: self.console_status.config(text=""))   

    def show_decryption_view(self):
        """Muestra una interfaz para desencriptar mensajes usando los pictogramas Synthex."""
        self.current_view = "decryption"
        # --- GUARDAR ESTADO ANTES DE CAMBIAR DE VISTA ---
        self._save_terminal_state()

        # Detener la animación de la terminal si está activa
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        
        # Limpiar la vista actual del programa
        for widget in self.winfo_children():
            widget.destroy()

        # Frame contenedor principal para la nueva vista de desencriptación
        self.decryption_frame = tk.Frame(self, bg=self.bg_color, padx=20, pady=20)
        self.decryption_frame.pack(fill=tk.BOTH, expand=True)

        # Configuración de la cuadrícula
        self.decryption_frame.columnconfigure(0, weight=1)
        self.decryption_frame.columnconfigure(1, weight=1)

        # Título de la vista
        title_label = tk.Label(self.decryption_frame, text="SYNTHEX DECRYPTION TOOL", font=("Courier", 24, "bold"),
                               fg=self.accent_color, bg=self.bg_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # Etiqueta para cerrar (advisor)
        close_advisor = tk.Label(self.decryption_frame, text="< CLICK TO CLOSE >", font=("Courier", 10, "italic"),
                                 bg=self.bg_color, fg="#5D6064", cursor="hand2")
        close_advisor.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        close_advisor.bind("<Button-1>", lambda e: self.return_to_terminal_restore())

        # Frame para la entrada
        input_frame = tk.LabelFrame(self.decryption_frame, text="GLYPHS TO DECRYPT:", font=("Courier", 12),
                                    fg=self.text_color, bg=self.bg_color, bd=2, relief=tk.SOLID)
        input_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="nsew")
        
        self.input_text_area = tk.Text(input_frame, bg="#0E0E0E", fg="#00FFFF", font=("Courier", 24),
                                     height=8, insertbackground="#00FFFF", relief=tk.FLAT, bd=0)
        self.input_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame para los botones
        button_frame = tk.Frame(self.decryption_frame, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))

        tk.Button(button_frame, text="DECRYPT", command=self.decrypt_message,
                  bg=self.accent_color, fg=self.bg_color, font=("Courier", 12, "bold"),
                  activebackground=self.text_color, activeforeground=self.bg_color,
                  bd=0, relief=tk.FLAT).pack(side=tk.LEFT, padx=10, ipadx=20)
        
        tk.Button(button_frame, text="COPY DECRYPTED", command=self.copy_decrypted,
                  bg=self.text_color, fg=self.bg_color, font=("Courier", 12, "bold"),
                  activebackground=self.accent_color, activeforeground=self.bg_color,
                  bd=0, relief=tk.FLAT).pack(side=tk.LEFT, padx=10, ipadx=20)

        # Frame para la salida
        output_frame = tk.LabelFrame(self.decryption_frame, text="DECRYPTED MESSAGE:", font=("Courier", 12),
                                     fg=self.text_color, bg=self.bg_color, bd=2, relief=tk.SOLID)
        output_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="nsew")
        
        self.output_text_area = tk.Text(output_frame, bg="#0E0E0E", fg="#00FF00", font=("Courier", 12),
                                      height=5, wrap="word", relief=tk.FLAT, bd=0)
        self.output_text_area.config(state=tk.DISABLED)
        self.output_text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)   

    def decrypt_message(self):
        """Toma los pictogramas de entrada y los desencripta a palabras Synthex."""
        input_text = self.input_text_area.get("1.0", tk.END).strip()
        glyphs = input_text.split("—")
        decrypted_words = []
        
        for glyph in glyphs:
            if glyph in REV_SYNTHEX_DICTIONARY:
                decrypted_words.append(REV_SYNTHEX_DICTIONARY[glyph])
            else:
                decrypted_words.append(f"[UNK_GLYPH]")
        
        decrypted_text = " ".join(decrypted_words)
        
        self.output_text_area.config(state=tk.NORMAL)
        self.output_text_area.delete("1.0", tk.END)
        self.output_text_area.insert("1.0", decrypted_text)
        self.output_text_area.config(state=tk.DISABLED)

    def copy_decrypted(self):
        """Copia el texto desencriptado al portapapeles."""
        decrypted_text = self.output_text_area.get("1.0", tk.END).strip()
        if decrypted_text:
            self.clipboard_clear()
            self.clipboard_append(decrypted_text)
            if hasattr(self, "console_status"):
                self.console_status.config(text="Decrypted message copied to clipboard.")
                self.after(2000, lambda: self.console_status.config(text=""))   

    # --- FUNCIONES DE RESTAURACIÓN Y GUARDADO DE ESTADO ---
    def _save_terminal_state(self):
        """Guarda el estado actual de la terminal para restaurar después de salir de vistas secundarias."""
        # Guarda el historial de la consola
        self._saved_console = self.console_output.get("1.0", tk.END) if hasattr(self, "console_output") else ""
        # Guarda los glifos visualizados
        self._saved_glyphs = list(self.current_glyphs) if hasattr(self, "current_glyphs") else []
        # Guarda la integridad y amenaza
        self._saved_integrity = self.system_integrity
        self._saved_threat = self.threat_level
        # Guarda el tema actual
        self._saved_theme = self.current_theme
        # Guarda el historial de comandos
        self._saved_history = list(self.console_history)
        # Guarda los procesos activos
        self._saved_processes = list(self.active_processes)

        # --- Guardar estados especiales de pentester ---
        if self.mode == "pentester":
            SynthexTerminalEnhanced.pentester_integrity = self.system_integrity
            SynthexTerminalEnhanced.pentester_stealth_level = self.stealth_level
            # Guardar el status de sigilo textual (label)
            if hasattr(self, "threat_label"):
                SynthexTerminalEnhanced.pentester_stealth_status = self.threat_label.cget("text")

    def _restore_terminal_state(self):
        """Restaura el estado previo de la terminal después de salir de vistas secundarias."""
        # Destruye todos los widgets y reconstruye la interfaz principal
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

        # Restaura el historial de la consola
        if hasattr(self, "_saved_console") and hasattr(self, "console_output"):
            self.console_output.config(state=tk.NORMAL)
            self.console_output.delete("1.0", tk.END)
            self.console_output.insert("1.0", self._saved_console)
            self.console_output.config(state=tk.DISABLED)
            self.console_output.see(tk.END)

        # Restaura la visualización de los glifos (y fuerza restaurar aunque el warning ASCII esté activo)
        if hasattr(self, "_saved_glyphs") and self._saved_glyphs and hasattr(self, "canvas"):
            self.visualize_synthex_network(self._saved_glyphs)

        # Restaura integridad y amenaza
        if hasattr(self, "_saved_integrity"):
            self.system_integrity = self._saved_integrity
        if hasattr(self, "_saved_threat"):
            self.threat_level = self._saved_threat
        self.update_system_status()

        # Restaura el tema
        if hasattr(self, "_saved_theme"):
            self.current_theme = self._saved_theme
            self.theme_var.set(self.current_theme)
            self.apply_theme()

        # Restaura historial y procesos
        if hasattr(self, "_saved_history"):
            self.console_history = list(self._saved_history)
        if hasattr(self, "_saved_processes"):
            self.active_processes = list(self._saved_processes)

        # Inicia animaciones si corresponde
        self.start_animations()

        # --- Restaurar estados especiales de pentester ---
        if self.mode == "pentester":
            if SynthexTerminalEnhanced.pentester_integrity is not None:
                self.system_integrity = SynthexTerminalEnhanced.pentester_integrity
            if SynthexTerminalEnhanced.pentester_stealth_level is not None:
                self.stealth_level = SynthexTerminalEnhanced.pentester_stealth_level
            if SynthexTerminalEnhanced.pentester_stealth_status is not None and hasattr(self, "threat_label"):
                self.threat_label.config(text=SynthexTerminalEnhanced.pentester_stealth_status)
            self.update_status_labels()


    def show_blackwall(self):
        """Dibuja y anima el efecto del Muro Negro."""
        # Guard: Verifica que el canvas existe y tiene tamaño válido
        if not hasattr(self, "canvas"):
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(50, self.show_blackwall)
            return

        self.canvas.delete("all")
        self.write_to_console("WARNING: BLACKWALL PROTOCOL ACTIVATED - SYSTEM INTEGRITY LOST", "#FF0000")
        self.write_to_console("ATTEMPTING TO CONTAIN HOSTILE ENTITIES...", "#FF4400")

        symbols = "0123456789ABCDEF!@#$%^&*"
        self.blackwall_items = []

        # Dibuja los símbolos y guarda sus ids y posiciones
        for _ in range(500):
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            char = random.choice(symbols)
            size = random.randint(8, 20)
            color = random.choice(["#FF0000", "#FF4400", "#FF8800"])
            item_id = self.canvas.create_text(x, y, text=char, fill=color, font=("Consolas", size), tags="blackwall")
            dx = random.choice([-2, -1, 0, 1, 2])
            dy = random.choice([-2, -1, 0, 1, 2])
            self.blackwall_items.append({"id": item_id, "dx": dx, "dy": dy, "size": size})

        # Dibuja líneas y guarda sus ids y movimientos
        for _ in range(100):
            x1, y1 = random.randint(0, canvas_width), random.randint(0, canvas_height)
            x2, y2 = random.randint(0, canvas_width), random.randint(0, canvas_height)
            item_id = self.canvas.create_line(x1, y1, x2, y2, fill="#FF4400", width=1, dash=(2, 1), tags="blackwall")
            dx = random.choice([-2, -1, 0, 1, 2])
            dy = random.choice([-2, -1, 0, 1, 2])
            self.blackwall_items.append({"id": item_id, "dx": dx, "dy": dy, "is_line": True})

        self.animate_blackwall()

    def animate_blackwall(self):
        """Anima los elementos del Blackwall moviéndolos y cambiando colores."""
        if not hasattr(self, "blackwall_items"):
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        symbols = "0123456789ABCDEF!@#$%^&*"
        colors = ["#FF0000", "#FF4400", "#FF8800"]

        for item in self.blackwall_items:
            if item.get("is_line"):
                coords = self.canvas.coords(item["id"])
                if len(coords) == 4:
                    x1, y1, x2, y2 = coords
                    # Mueve la línea
                    x1_new = (x1 + item["dx"]) % canvas_width
                    y1_new = (y1 + item["dy"]) % canvas_height
                    x2_new = (x2 + item["dx"]) % canvas_width
                    y2_new = (y2 + item["dy"]) % canvas_height
                    self.canvas.coords(item["id"], x1_new, y1_new, x2_new, y2_new)
            else:
                coords = self.canvas.coords(item["id"])
                if len(coords) == 2:
                    x, y = coords
                    x_new = (x + item["dx"]) % canvas_width
                    y_new = (y + item["dy"]) % canvas_height
                    self.canvas.coords(item["id"], x_new, y_new)
                    # Cambia el símbolo y color aleatoriamente
                    if random.random() < 0.1:
                        new_char = random.choice(symbols)
                        new_color = random.choice(colors)
                        self.canvas.itemconfig(item["id"], text=new_char, fill=new_color)

        # Repite la animación mientras la integridad sea 0
        if self.system_integrity <= 0:
            self.after(150, self.animate_blackwall)

    def visualize_synthex_network(self, glyphs, original_text=""):
        """Visualiza la red Synthex en el canvas"""
        if self.system_integrity <= 0:
            return
            
        self.canvas.delete("all")
        self.glyph_coords.clear()
        self.glyph_tooltips.clear()
        self.glyph_constellation_map.clear()
        self.current_glyphs = glyphs
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(50, lambda: self.visualize_synthex_network(glyphs, original_text))
            return

        # Si la integridad baja del 20%, la red se vuelve caótica
        is_chaotic = (UNKNOWN_GLYPH in glyphs or self.threat_level > 50 or self.system_integrity <= 20)
        
        if not glyphs:
            return


        # --- Visualización especial: malware fuera del círculo, conectados a su objetivo ---
        num_glyphs = len(glyphs)
        center_x, center_y = canvas_width / 2, canvas_height / 2
        radius = min(canvas_width, canvas_height) / 3
        malware_glyphs = [m[0] for m in SynthexTerminalEnhanced.malware_links]
        # 1. Dibuja todos los nodos normales en círculo (el círculo nunca cambia su forma ni cantidad de nodos)
        circle_indices = [i for i, glyph in enumerate(glyphs) if glyph not in malware_glyphs]
        num_circle = len(circle_indices)
        import random
        for pos, i in enumerate(circle_indices):
            glyph = glyphs[i]
            angle = pos * (2 * math.pi / num_circle) if num_circle > 0 else 0
            # Si es caótico, agrega ruido aleatorio a la posición
            if is_chaotic:
                chaos_r = radius * (0.97 + 0.08 * random.random())
                chaos_angle = angle + (random.random() - 0.5) * 0.25
                x = center_x + chaos_r * math.cos(chaos_angle)
                y = center_y + chaos_r * math.sin(chaos_angle)
            else:
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
            self.glyph_coords[i] = (x, y)
            color = self.get_glyph_color(glyph)
            self.draw_glyph_shape(glyph, x, y, 20, color)
            word = REV_SYNTHEX_DICTIONARY.get(glyph, "unknown")
            self.glyph_tooltips[i] = f"{glyph} - {word}"

        # 2. Dibuja los malware fuera del círculo y conecta a su objetivo
        for idx, (malware_glyph, target_idx, duration) in enumerate(SynthexTerminalEnhanced.malware_links):
            # Buscar el índice real del malware en glyphs
            try:
                malware_index = glyphs.index(malware_glyph)
            except ValueError:
                continue
            # Si el objetivo ya no existe, omitir
            if target_idx not in self.glyph_coords:
                continue
            # Posición del objetivo
            x0, y0 = self.glyph_coords[target_idx]
            # Ángulo desde el centro al objetivo
            angle = math.atan2(y0 - center_y, x0 - center_x)
            # Distancia malware-objetivo depende de duración: más rápido = más cerca
            min_dist = radius + 40  # mínimo fuera del círculo
            max_dist = radius + 120 # máximo lejos
            norm = max(1, min(duration, 60))
            dist = min_dist + (max_dist - min_dist) * (norm / 60)
            mx = center_x + dist * math.cos(angle)
            my = center_y + dist * math.sin(angle)
            self.glyph_coords[malware_index] = (mx, my)
            color = self.get_glyph_color(malware_glyph)
            self.draw_glyph_shape(malware_glyph, mx, my, 22, color)
            word = REV_SYNTHEX_DICTIONARY.get(malware_glyph, "unknown")
            self.glyph_tooltips[malware_index] = f"{malware_glyph} - {word} (malware)"
            # Conexión visual SOLO a su objetivo
            self.canvas.create_line(mx, my, x0, y0, fill="#FF00FF", width=2, dash=(4, 2))

        self.draw_connections(is_chaotic)
        
    def visualize_constellations(self):
        """Visualiza todos los glifos de Synthex agrupados por constelación."""
        self.canvas.delete("all")
        self.glyph_coords.clear()
        self.glyph_tooltips.clear()
        self.glyph_constellation_map.clear()

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(50, self.visualize_constellations)
            return

        constellation_names = list(GLYPH_CONSTELLATIONS.keys())
        num_constellations = len(constellation_names)
        
        center_x, center_y = canvas_width / 2, canvas_height / 2
        outer_radius = min(canvas_width, canvas_height) / 2.5
        
        # Posiciones de los centros de las constelaciones
        constellation_positions = {}
        for i, name in enumerate(constellation_names):
            angle = i * (2 * math.pi / num_constellations) + math.pi/2 # Empezar arriba
            x_pos = center_x + outer_radius * math.cos(angle)
            y_pos = center_y - outer_radius * math.sin(angle)
            constellation_positions[name] = (x_pos, y_pos)

        # Dibujar cada constelación
        for const_name, const_words in GLYPH_CONSTELLATIONS.items():
            cx, cy = constellation_positions[const_name]
            const_glyphs = [SYNTHEX_DICTIONARY.get(word, UNKNOWN_GLYPH) for word in const_words]
            num_glyphs = len(const_glyphs)
            inner_radius = 40 + num_glyphs * 2 # Radio dinámico
            
            glyph_indices = []
            
            # Dibujar glifos de la constelación
            for i, glyph in enumerate(const_glyphs):
                angle = i * (2 * math.pi / num_glyphs)
                x = cx + inner_radius * math.cos(angle)
                y = cy + inner_radius * math.sin(angle)
                
                color = self.get_glyph_color(glyph)
                tag = f"glyph_{len(self.glyph_coords)}"
                self.draw_glyph_shape(glyph, x, y, 15, color, tag)
                
                # Almacenar información del glifo
                index = len(self.glyph_coords)
                self.glyph_coords[index] = (x, y)
                self.glyph_tooltips[index] = f"{glyph} - {REV_SYNTHEX_DICTIONARY.get(glyph, 'unknown')}"
                self.glyph_constellation_map[index] = const_name
                glyph_indices.append(index)
            
            # Dibujar conexiones dentro de la constelación
            for i in range(len(glyph_indices)):
                j = (i + 1) % len(glyph_indices)
                idx1, idx2 = glyph_indices[i], glyph_indices[j]
                x1, y1 = self.glyph_coords[idx1]
                x2, y2 = self.glyph_coords[idx2]
                self.canvas.create_line(x1, y1, x2, y2, fill=self.text_color, width=1, dash=(3, 2))
                
            # Dibujar el nombre de la constelación en el centro
            self.canvas.create_text(cx, cy, text=const_name, fill=self.accent_color,
                                    font=("Courier", 10, "bold"), justify=tk.CENTER)
            
        self.current_glyphs = [glyph for words in GLYPH_CONSTELLATIONS.values() for word in words]
        self.start_animations()

    def get_glyph_color(self, glyph):
        """Determina el color del glifo basado en su tipo"""
        word = REV_SYNTHEX_DICTIONARY.get(glyph, "")
        
        if word in ATTACK_GLYPH_WORDS:
            return "#FF0000"  # Rojo para amenazas
        elif word in SECURITY_GLYPH_WORDS:
            return "#00FF00"  # Verde para seguridad
        elif word in ["ai", "sentience", "construct", "entity", "ghost", "identity", "memory"]:
            return "#00FFFF"  # Cyan para IA
        elif word in ["chaos", "anomaly"]:
            return "#9900FF"  # Purple for Critical States
        else:
            return "#FFFB00"  # Color normal

    def draw_connections(self, is_chaotic):
        """Dibuja conexiones entre glifos"""
        # Solo conectar los nodos normales (no malware) con líneas verdes
        # Los malware solo se conectan a su víctima con la línea morada en visualize_synthex_network
        if len(self.glyph_coords) < 2:
            return

        # Identificar los índices de malware para excluirlos
        malware_glyphs = [m[0] for m in SynthexTerminalEnhanced.malware_links]
        normal_indices = [i for i in self.glyph_coords.keys() if i < len(self.current_glyphs) and self.current_glyphs[i] not in malware_glyphs]

        if is_chaotic:
            num_connections = min(len(normal_indices) * 2, 20)
            for _ in range(num_connections):
                if len(normal_indices) < 2:
                    break
                i, j = random.sample(normal_indices, 2)
                x1, y1 = self.glyph_coords[i]
                x2, y2 = self.glyph_coords[j]
                self.canvas.create_line(x1, y1, x2, y2, fill="#FF4400", 
                                      width=2, dash=(3, 2), tags="connection")
        else:
            for idx in range(len(normal_indices)):
                i = normal_indices[idx]
                j = normal_indices[(idx + 1) % len(normal_indices)]
                x1, y1 = self.glyph_coords[i]
                x2, y2 = self.glyph_coords[j]
                self.canvas.create_line(x1, y1, x2, y2, fill=self.accent_color, 
                                      width=1, dash=(5, 3), tags="connection")

    def show_glyph_tooltip(self, event):
        """Muestra tooltip al pasar sobre un glifo"""
        pass

    def on_glyph_click(self, event):
        """Maneja clicks en glifos"""
        click_x, click_y = event.x, event.y
        min_distance = float('inf')
        closest_glyph_index = None
        # Buscar el glifo más cercano al click
        for index, value in self.glyph_coords.items():
            # value puede ser (x, y, word) o (x, y)
            if len(value) == 3:
                x, y, word = value
            else:
                x, y = value
                word = None
            distance = math.sqrt((click_x - x)**2 + (click_y - y)**2)
            if distance < min_distance and distance < 30: # Umbral de proximidad
                min_distance = distance
                closest_glyph_index = index
                closest_word = word
        if closest_glyph_index is not None:
            # Determinar el glifo y la palabra asociada
            glyph = self.current_glyphs[closest_glyph_index] if self.current_glyphs and closest_glyph_index < len(self.current_glyphs) else None
            # Si no se obtuvo la palabra, buscar por el glifo
            word = closest_word
            if not word and glyph:
                word = REV_SYNTHEX_DICTIONARY.get(glyph, None)
            if not word:
                self.write_to_console(f"[?] Unknown glyph: {glyph if glyph else '?'}", "#FF00FF")
                return
            # Buscar constelación a la que pertenece
            found_constellation = None
            for const_name, words in GLYPH_CONSTELLATIONS.items():
                if word in words:
                    found_constellation = const_name
                    break
            if found_constellation:
                self.write_to_console(f"[GLYPH] '{word.upper()}' ({glyph}) → {found_constellation}", "#00FFFF")
            else:
                self.write_to_console(f"[GLYPH] '{word.upper()}' ({glyph}) → (No constellation group)", "#00FFFF")
        # Si no está cerca de ningún glifo, no hacer nada
        return

    def start_animations(self):
        """Inicia las animaciones del canvas"""
        self.animate_connections()
        self.animate_data_flow_between_glyphs()

    def animate_connections(self):
        """Anima las conexiones"""
        if self.system_integrity <= 0:
            return

        connections = self.canvas.find_withtag("connection")
        for conn in connections:
            current_color = self.canvas.itemcget(conn, "fill")
            if current_color == self.accent_color:
                new_color = self.text_color
            else:
                new_color = self.accent_color
            self.canvas.itemconfig(conn, fill=new_color)
        
        self.after(500, self.animate_connections)

    def animate_data_flow_between_glyphs(self):
        """Crea y anima puntos de datos moviéndose entre glifos con lógica"""
        if self.system_integrity <= 0:
            return

        if len(self.glyph_coords) < 2 or random.random() < 0.7:
            # Controla la frecuencia de los puntos de datos para que no saturen la pantalla
            self.after(100, self.animate_data_flow_between_glyphs)
            return

        # Seleccionar un glifo de origen
        source_index = random.choice(list(self.glyph_coords.keys()))
        start_x, start_y = self.glyph_coords[source_index]
        source_word = REV_SYNTHEX_DICTIONARY.get(self.current_glyphs[source_index], "")
        
        target_index = None

        if source_word in ATTACK_GLYPH_WORDS:
            # Si el origen es un ataque, buscar un objetivo de seguridad
            security_indices = [i for i, word in enumerate(self.current_glyphs) 
                                if word in SECURITY_GLYPH_WORDS]
            if security_indices:
                target_index = random.choice(security_indices)
        
        if target_index is None:
            # Si no es un ataque o no hay objetivos de seguridad, elegir un destino aleatorio
            other_indices = [i for i in self.glyph_coords.keys() if i != source_index]
            if other_indices:
                target_index = random.choice(other_indices)

        if target_index is not None:
            end_x, end_y = self.glyph_coords[target_index]
            data_color = self.get_glyph_color(self.current_glyphs[source_index])

            point = self.canvas.create_oval(start_x-2, start_y-2, start_x+2, start_y+2,
                                            fill=data_color, outline="", tags="dataflow")
            self.animate_point_to_target(point, start_x, start_y, end_x, end_y, 0)
        
        self.after(100, self.animate_data_flow_between_glyphs)

    def animate_point_to_target(self, point, start_x, start_y, end_x, end_y, step):
        """Anima un punto de datos moviéndose de un glifo a otro"""
        if step > 40:
            self.canvas.delete(point)
            return
        
        progress = step / 40.0
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        
        coords = self.canvas.coords(point)
        if coords:
            self.canvas.coords(point, current_x-2, current_y-2, current_x+2, current_y+2)
            self.after(20, lambda: self.animate_point_to_target(point, start_x, start_y, end_x, end_y, step + 1))
    
    def show_manual(self):
        """Muestra el manual de Synthex expandido"""
        manual_window = tk.Toplevel(self)
        manual_window.title("Synthex Language Manual v2.0")
        manual_window.geometry("900x700")
        manual_window.configure(bg=self.bg_color)

        main_frame = tk.Frame(manual_window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        manual_text = tk.Text(main_frame, bg=self.bg_color, fg=self.text_color, 
                             font=("Courier", 10), padx=10, pady=10, wrap="word")
        scrollbar = tk.Scrollbar(main_frame, command=manual_text.yview)
        manual_text.config(yscrollcommand=scrollbar.set)
        
        manual_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        manual_content = """
SYNTHEX LANGUAGE MANUAL v2.0 - ENHANCED NETRUNNER EDITION
========================================================

WARNING: This terminal interfaces directly with AI constructs beyond the Blackwall.
Unauthorized access may result in ICE countermeasures or entity intrusion.

OVERVIEW:
---------
Synthex is not merely a language—it is a direct neural interface protocol used by 
rogue AIs and advanced constructs. Each glyph represents compressed conceptual data,
allowing for rapid information exchange in hostile network environments.

BASIC COMMAND STRUCTURE:
-----------------------
Commands can be executed in plain text or Synthex glyphs:
- Single words are converted to individual glyphs
- Command sequences create network visualizations
- Attack vectors trigger security protocols

CORE SYNTHEX DICTIONARY:
=======================

BASIC NETWORK OPERATIONS:
hello       ░   - Initiate handshake protocol
world       Ω   - Physical realm reference  
message     ▒   - Data packet transmission
network     ⊕   - Node connection establishment
encrypt     Ψ   - Data obfuscation protocol
decrypt     Φ   - Data revelation protocol
link        ↔   - Bidirectional connection
system      Σ   - Complete infrastructure
code        ⎚   - Executable instructions
data        ⍬   - Raw information stream

AI & CONSCIOUSNESS:
ai          ▓   - Artificial intelligence entity
sentience   ⍲   - Self-awareness indicator
construct   ⍦   - Digital consciousness copy
entity      ⍰   - Unknown intelligence presence
ghost       ⊚   - Fragmented consciousness
identity    ∞   - Core self-identification
memory      ⌂   - Data storage/recall system

SECURITY & THREATS:
firewall    ◫   - Protective barrier system
security    ⌠   - Access control protocol
breach      ⍟   - Unauthorized system entry
threat      ⍞   - Hostile presence indicator
corrupt     ⍟§  - Data integrity violation
trace       ⍒   - Tracking protocol activation
probe       ⍴   - System reconnaissance
access      ⎇   - Permission verification

SYSTEM STATES:
stable      Δ   - Secure operational state
chaos       §   - System instability
error       ⊘   - Logic fault condition
anomaly     ⌖   - Unexpected behavior pattern

ADVANCED OPERATIONS:
jack_in     ⍐   - Direct neural interface
protocol    ⍱   - Communication standard
interface   ⌤   - System interaction point
core        ◉   - Central processing unit
digital     ⎚⎚  - Virtual environment
reality     ∞∞  - Physical world contrast

EXPANDED THREAT MATRIX:
======================

MALWARE CLASSIFICATIONS:
virus       ⌼   - Self-replicating hostile code
worm        ⌿   - Network propagation entity
trojan      ⍀   - Disguised hostile program
ransomware  ⍂   - Data encryption extortion
spyware     ⍃   - Covert monitoring program
malware     ⍄   - General hostile software
keylogger   ⍁   - Input capture program

DEFENSIVE MEASURES:
honeypot    ⍅   - Deception security trap
sandbox     ⍆   - Isolated execution environment  
quarantine  ⍇   - Threat containment protocol
whitelist   ⍈   - Approved entity registry
blacklist   ⍉   - Blocked entity registry
patch       ⍌   - Security vulnerability fix
backup      ⍎   - Data preservation copy

EXPLOITATION TOOLS:
exploit     ⍊   - Vulnerability abuse vector
backdoor    ⌹   - Hidden access mechanism
root        ⌨   - Administrative access level
admin       ⌬   - System control privileges
botnet      ⌶   - Coordinated zombie network

NETWORK OPERATIONS:
mirror      ⍑   - Exact system duplication
clone       ⍒   - Entity replication process
sync        ⍓   - Data synchronization
restore     ⍏   - System recovery operation
update      ⍍   - Software modification

OPERATIONAL COMMANDS:
====================

CONSOLE COMMANDS:
help        - Display available commands
man         - Show this manual
clear       - Clear console output
status      - Show system diagnostics
scan        - Perform security scan
reset       - Emergency system restoration
theme <n>   - Change interface theme
test        - Show all glyph constellations
alpha       - Show synthex dictionary
enc         - Dedicated encryption system
dec         - Dedicated decryption system


SYNTHEX OPERATIONS:
encrypt <text>    - Convert to Synthex glyphs
decrypt <glyphs>  - Convert from Synthex glyphs

ATTACK SIMULATION:
breach <target>   - Attempt unauthorized access
corrupt <data>    - Damage system integrity  
probe <system>    - Reconnaissance operation
exploit <vuln>    - Abuse system weakness

NETWORK VISUALIZATION:
=====================

The network canvas displays glyph relationships:
- STABLE networks show ordered circular patterns
- CHAOTIC networks display random connections
- Threat level affects connection appearance
- Data flow shows as moving points
- Click glyphs for detailed information

THREAT ASSESSMENT:
=================

System Integrity: 0-100%
- 100-80%: SECURE (Green)
- 79-50%: DEGRADED (Yellow) 
- 49-20%: COMPROMISED (Orange)
- 19-0%: CRITICAL (Red)

Threat Level: 0-100%
- 0-30%: LOW (Secure operations)
- 31-69%: MEDIUM (Elevated monitoring)
- 70-100%: CRITICAL (Emergency protocols)

WARNING PROTOCOLS:
=================

- Hostile traces may be generated during attack simulations
- System integrity degrades with successful breaches
- Emergency reset restores all parameters
- Unknown glyphs indicate corrupted transmissions
- Entity intrusion possible at high threat levels

REMEMBER: The entities beyond the Blackwall do not communicate—they infiltrate.
Use Synthex protocols with extreme caution.

END TRANSMISSION
================
        """
        
        manual_text.insert(tk.END, manual_content)
        manual_text.config(state=tk.DISABLED)

        

    def draw_glyph_shape(self, glyph, x, y, size, color, tag=""):
        """Dibuja la forma correspondiente a un glifo"""
        shape_name = GLYPH_SHAPES.get(glyph, "unknown")
        
        if shape_name == "square_block": self._draw_square_block(x, y, size, color, tag)
        elif shape_name == "omega": self._draw_omega(x, y, size, color, tag)
        elif shape_name == "dotted_block": self._draw_dotted_block(x, y, size, color, tag)
        elif shape_name == "solid_block": self._draw_solid_block(x, y, size, color, tag)
        elif shape_name == "circle_plus": self._draw_circle_plus(x, y, size, color, tag)
        elif shape_name == "psi": self._draw_psi(x, y, size, color, tag)
        elif shape_name == "phi": self._draw_phi(x, y, size, color, tag)
        elif shape_name == "section": self._draw_section(x, y, size, color, tag)
        elif shape_name == "triangle": self._draw_triangle(x, y, size, color, tag)
        elif shape_name == "left_right_arrow": self._draw_left_right_arrow(x, y, size, color, tag)
        elif shape_name == "sigma": self._draw_sigma(x, y, size, color, tag)
        elif shape_name == "star": self._draw_star(x, y, size, color, tag)
        elif shape_name == "rectangle": self._draw_rectangle(x, y, size, color, tag)
        elif shape_name == "double_tilde": self._draw_double_tilde(x, y, size, color, tag)
        elif shape_name == "circle_slash": self._draw_circle_slash(x, y, size, color, tag)
        elif shape_name == "house": self._draw_house(x, y, size, color, tag)
        elif shape_name == "infinity": self._draw_infinity(x, y, size, color, tag)
        elif shape_name == "circle_dot": self._draw_circle_dot(x, y, size, color, tag)
        elif shape_name == "protocol": self._draw_protocol(x, y, size, color, tag)
        elif shape_name == "firewall": self._draw_firewall(x, y, size, color, tag)
        elif shape_name == "down_arrow": self._draw_down_arrow(x, y, size, color, tag)
        elif shape_name == "up_arrow": self._draw_up_arrow(x, y, size, color, tag)
        elif shape_name == "construct": self._draw_construct(x, y, size, color, tag)
        elif shape_name == "question_box": self._draw_question_box(x, y, size, color, tag)
        elif shape_name == "sentience": self._draw_sentience(x, y, size, color, tag)
        elif shape_name == "anomaly": self._draw_anomaly(x, y, size, color, tag)
        elif shape_name == "data_stream": self._draw_data_stream(x, y, size, color, tag)
        elif shape_name == "probe": self._draw_probe(x, y, size, color, tag)
        elif shape_name == "divert": self._draw_divert(x, y, size, color, tag)
        elif shape_name == "corrupt": self._draw_corrupt(x, y, size, color, tag)
        elif shape_name == "nullify": self._draw_nullify(x, y, size, color, tag)
        elif shape_name == "access": self._draw_access(x, y, size, color, tag)
        elif shape_name == "security": self._draw_security(x, y, size, color, tag)
        elif shape_name == "core": self._draw_core(x, y, size, color, tag)
        elif shape_name == "digital": self._draw_digital(x, y, size, color, tag)
        elif shape_name == "reality": self._draw_reality(x, y, size, color, tag)
        elif shape_name == "interface": self._draw_interface(x, y, size, color, tag)
        elif shape_name == "threat": self._draw_threat(x, y, size, color, tag)
        elif shape_name == "man": self._draw_man(x, y, size, color, tag)
        
        elif shape_name == "keyboard": self._draw_keyboard(x, y, size, color, tag)
        elif shape_name == "admin_key": self._draw_admin_key(x, y, size, color, tag)
        elif shape_name == "backdoor": self._draw_backdoor(x, y, size, color, tag)
        elif shape_name == "botnet": self._draw_botnet(x, y, size, color, tag)
        elif shape_name == "virus": self._draw_virus(x, y, size, color, tag)
        elif shape_name == "worm": self._draw_worm(x, y, size, color, tag)
        elif shape_name == "trojan": self._draw_trojan(x, y, size, color, tag)
        elif shape_name == "keylogger": self._draw_keylogger(x, y, size, color, tag)
        elif shape_name == "ransomware": self._draw_ransomware(x, y, size, color, tag)
        elif shape_name == "spyware": self._draw_spyware(x, y, size, color, tag)
        elif shape_name == "malware": self._draw_malware(x, y, size, color, tag)
        elif shape_name == "honeypot": self._draw_honeypot(x, y, size, color, tag)
        elif shape_name == "sandbox": self._draw_sandbox(x, y, size, color, tag)
        elif shape_name == "quarantine": self._draw_quarantine(x, y, size, color, tag)
        elif shape_name == "whitelist": self._draw_whitelist(x, y, size, color, tag)
        elif shape_name == "blacklist": self._draw_blacklist(x, y, size, color, tag)
        elif shape_name == "exploit": self._draw_exploit(x, y, size, color, tag)
        elif shape_name == "vulnerability": self._draw_vulnerability(x, y, size, color, tag)
        elif shape_name == "patch": self._draw_patch(x, y, size, color, tag)
        elif shape_name == "update": self._draw_update(x, y, size, color, tag)
        elif shape_name == "backup": self._draw_backup(x, y, size, color, tag)
        elif shape_name == "restore": self._draw_restore(x, y, size, color, tag)
        elif shape_name == "mirror": self._draw_mirror(x, y, size, color, tag)
        elif shape_name == "clone": self._draw_clone(x, y, size, color, tag)
        elif shape_name == "sync": self._draw_sync(x, y, size, color, tag)
        else:
            self.canvas.create_rectangle(x-size, y-size, x+size, y+size, outline=color, tags=tag)
            self.canvas.create_text(x, y, text="?", fill=color, font=("Courier", 18, "bold"), tags=tag)

    def _draw_square_block(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1, tags=tag)

    def _draw_omega(self, x, y, size, color, tag):
        points = [x - size, y + size, x - size / 2, y - size, x + size / 2, y - size, x + size, y + size]
        self.canvas.create_line(points, fill=color, width=1, tags=tag)
        self.canvas.create_arc(x - size, y - size/2, x + size, y + size/2, start=180, extent=180, outline=color, style=tk.ARC, width=1, tags=tag)

    def _draw_dotted_block(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color, tags=tag)
    
    def _draw_solid_block(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=color, outline=color, tags=tag)
    
    def _draw_circle_plus(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)

    def _draw_psi(self, x, y, size, color, tag):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)
        
    def _draw_phi(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)

    def _draw_section(self, x, y, size, color, tag):
        self.canvas.create_arc(x - size, y - size, x, y, start=90, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x, y, x + size, y + size, start=270, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_line(x, y, x, y+size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x, y, x, y-size, fill=color, width=1, tags=tag)

    def _draw_triangle(self, x, y, size, color, tag):
        self.canvas.create_polygon(x, y - size, x - size, y + size, x + size, y + size, outline=color, fill="", tags=tag)

    def _draw_left_right_arrow(self, x, y, size, color, tag):
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x - size / 2, y - size / 2, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x - size / 2, y + size / 2, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size, y, x + size / 2, y - size / 2, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size, y, x + size / 2, y + size / 2, fill=color, width=1, tags=tag)

    def _draw_sigma(self, x, y, size, color, tag):
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size, y + size, x - size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size, x, y, fill=color, width=1, tags=tag)
        self.canvas.create_line(x, y, x - size, y + size, fill=color, width=1, tags=tag)

    def _draw_star(self, x, y, size, color, tag):
        points = []
        for i in range(5):
            angle = math.pi/2 + i * (2*math.pi / 5)
            x_point = x + size * math.cos(angle)
            y_point = y - size * math.sin(angle)
            points.append((x_point, y_point))
        self.canvas.create_polygon(points, outline=color, fill="", width=1, tags=tag)

    def _draw_rectangle(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)

    def _draw_double_tilde(self, x, y, size, color, tag):
        self.canvas.create_arc(x - size, y - size, x + size, y, start=180, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x - size, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)

    def _draw_circle_slash(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1, tags=tag)

    def _draw_house(self, x, y, size, color, tag):
        self.canvas.create_polygon(x, y - size, x - size, y, x + size, y, outline=color, fill="", tags=tag)
        self.canvas.create_rectangle(x - size, y, x + size, y + size, outline=color, tags=tag)
        
    def _draw_infinity(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size/2, x, y + size/2, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x, y - size/2, x + size, y + size/2, outline=color, width=1, tags=tag)

    def _draw_circle_dot(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color, tags=tag)

    def _draw_protocol(self, x, y, size, color, tag):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1, tags=tag)

    def _draw_firewall(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x - size/2, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size, y, x + size/2, y - size, fill=color, width=1, tags=tag)

    def _draw_down_arrow(self, x, y, size, color, tag):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size / 2, y + size / 2, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size / 2, y + size / 2, x, y + size, fill=color, width=1, tags=tag)
    
    def _draw_up_arrow(self, x, y, size, color, tag):
        self.canvas.create_line(x, y + size, x, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size / 2, y - size / 2, x, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size / 2, y - size / 2, x, y - size, fill=color, width=1, tags=tag)

    def _draw_construct(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size/2, y - size, x + size/2, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)
    
    def _draw_question_box(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, tags=tag)
        self.canvas.create_arc(x - size/2, y-size, x + size/2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_line(x, y, x, y + size / 2, fill=color, width=1, tags=tag)

    def _draw_sentience(self, x, y, size, color, tag):
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size/2, y + size, x, y-size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size/2, y + size, x, y-size, fill=color, width=1, tags=tag)

    def _draw_anomaly(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size/2, y - size, x + size/2, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size/2, y - size, x - size/2, y + size, fill=color, width=1, tags=tag)

    def _draw_data_stream(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size/2, x, y + size/2, outline=color, tags=tag)
        self.canvas.create_oval(x, y - size/2, x + size, y + size/2, outline=color, tags=tag)
        self.canvas.create_line(x, y - size/2, x, y + size/2, fill=color, tags=tag)

    def _draw_probe(self, x, y, size, color, tag):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, tags=tag)
        self.canvas.create_oval(x - size, y, x, y + size, outline=color, tags=tag)
    
    def _draw_divert(self, x, y, size, color, tag):
        self.canvas.create_arc(x - size, y - size, x + size/2, y, start=180, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x - size/2, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)

    def _draw_corrupt(self, x, y, size, color, tag):
        self._draw_star(x - size/2, y, size/2, color, tag)
        self.canvas.create_arc(x + size/2, y - size/2, x + size, y + size/2, start=0, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)

    def _draw_nullify(self, x, y, size, color, tag):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
    
    def _draw_access(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1, tags=tag)

    def _draw_security(self, x, y, size, color, tag):
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1, tags=tag)

    def _draw_core(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color, tags=tag)

    def _draw_digital(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size/2, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_rectangle(x - size/2, y - size, x + size, y + size, outline=color, width=1, tags=tag)

    def _draw_reality(self, x, y, size, color, tag):
        self._draw_infinity(x - size/2, y, size, color, tag)
        self._draw_infinity(x + size/2, y, size, color, tag)

    def _draw_interface(self, x, y, size, color, tag):
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x + size, y - size, x + size, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)

    def _draw_threat(self, x, y, size, color, tag):
        self.canvas.create_polygon(x, y - size, x - size/2, y + size/2, x + size/2, y + size/2, outline=color, fill="", tags=tag)
        self.canvas.create_line(x - size/2, y+size, x + size/2, y+size, fill=color, width=1, tags=tag)
    
    def _draw_man(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x - size, y-size, x, y, start=90, extent=90, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x, y-size, x+size, y, start=0, extent=90, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x-size, y, x, y+size, start=180, extent=90, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x, y, x+size, y+size, start=270, extent=90, style=tk.ARC, outline=color, width=1, tags=tag)

    def _draw_keyboard(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size/2, x + size, y + size/2, outline=color, width=1, tags=tag)
        for i in range(-2, 3):
            for j in range(-1, 2):
                self.canvas.create_rectangle(x + i*size/3, y + j*size/4, 
                                           x + (i+0.5)*size/3, y + (j+0.5)*size/4, 
                                           outline=color, width=1, tags=tag)

    def _draw_admin_key(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size/2, y - size, x + size/2, y - size/2, outline=color, width=1, tags=tag)
        self.canvas.create_line(x, y - size/2, x, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x, y, x + size/2, y, fill=color, width=1, tags=tag)
        self.canvas.create_line(x, y + size/2, x + size/3, y + size/2, fill=color, width=1, tags=tag)

    def _draw_backdoor(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size/2, y - size, x - size/2, y + size, fill=color, width=1, tags=tag)
        self.canvas.create_oval(x - size/3, y - size/4, x - size/6, y, fill=color, outline=color, tags=tag)

    def _draw_botnet(self, x, y, size, color, tag):
        center_positions = [(x, y-size/2), (x-size/2, y+size/2), (x+size/2, y+size/2)]
        for pos in center_positions:
            self.canvas.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill=color, outline=color, tags=tag)
        for i in range(len(center_positions)):
            for j in range(i+1, len(center_positions)):
                self.canvas.create_line(center_positions[i][0], center_positions[i][1],
                                      center_positions[j][0], center_positions[j][1], fill=color, width=1, tags=tag)

    def _draw_virus(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size/2, y - size/2, x + size/2, y + size/2, outline=color, width=1, tags=tag)
        for i in range(8):
            angle = i * math.pi / 4
            x1 = x + (size/2) * math.cos(angle)
            y1 = y + (size/2) * math.sin(angle)
            x2 = x + size * math.cos(angle)
            y2 = y + size * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1, tags=tag)

    def _draw_worm(self, x, y, size, color, tag):
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            wave_x = x + (i - 5) * size / 5
            wave_y = y + size/2 * math.sin(angle * 2)
            points.extend([wave_x, wave_y])
        self.canvas.create_line(points, fill=color, width=2, smooth=True, tags=tag)

    def _draw_trojan(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_polygon(x - size/2, y, x, y - size, x + size/2, y, outline=color, fill="", tags=tag)
        self.canvas.create_oval(x - size/4, y + size/4, x + size/4, y + 3*size/4, outline=color, width=1, tags=tag)

    def _draw_keylogger(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y, x + size, y + size/2, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x - size/3, y - size, x + size/3, y - size/3, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x - size/6, y - 5*size/6, x + size/6, y - 2*size/3, fill=color, outline=color, tags=tag)

    def _draw_ransomware(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size/2, y, x + size/2, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_arc(x - size/2, y - size, x + size/2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1, tags=tag)
        self.canvas.create_text(x, y + size/2, text="$", fill=color, font=("Courier", int(size), "bold"), tags=tag)

    def _draw_spyware(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size/2, x + size, y + size/2, outline=color, width=1, tags=tag)
        self.canvas.create_oval(x - size/3, y - size/6, x + size/3, y + size/6, fill=color, outline=color, tags=tag)
        self.canvas.create_line(x, y - size/2, x, y - size, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size/4, y - 3*size/4, x + size/4, y - 3*size/4, fill=color, width=1, tags=tag)

    def _draw_malware(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y - size/2, x + size, y - size/2, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y + size/2, x + size, y + size/2, fill=color, width=1, tags=tag)
        self.canvas.create_line(x - size/2, y - size/2, x + size/2, y + size/2, fill="#FF0000", width=2, tags=tag)
        self.canvas.create_line(x - size/2, y + size/2, x + size/2, y - size/2, fill="#FF0000", width=2, tags=tag)

    def _draw_honeypot(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size/2, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_rectangle(x - size/3, y - size, x + size/3, y - size/2, outline=color, width=1, tags=tag)
        self.canvas.create_polygon(x - size/2, y, x, y - size/4, x + size/2, y, outline="#FF4400", fill="", tags=tag)

    def _draw_sandbox(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=2, tags=tag)
        self.canvas.create_rectangle(x - size/2, y - size/2, x + size/2, y + size/2, outline=color, width=1, dash=(3, 3), tags=tag)
        self.canvas.create_oval(x - size/4, y - size/4, x + size/4, y + size/4, fill=color, outline=color, tags=tag)

    def _draw_quarantine(self, x, y, size, color, tag):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=2, tags=tag)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill="#FF0000", width=3, tags=tag)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill="#FF0000", width=3, tags=tag)

    def _draw_whitelist(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        for i in range(3):
            y_pos = y - size/2 + i * size/2
            self.canvas.create_line(x - size/2, y_pos, x + size/2, y_pos, fill=color, width=1, tags=tag)
            self.canvas.create_line(x - 3*size/4, y_pos - size/8, x - size/2, y_pos, fill="#00FF00", width=2, tags=tag)
            self.canvas.create_line(x - size/2, y_pos, x - size/4, y_pos - size/4, fill="#00FF00", width=2, tags=tag)

    def _draw_blacklist(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        for i in range(3):
            y_pos = y - size/2 + i * size/2
            self.canvas.create_line(x - size/2, y_pos, x + size/2, y_pos, fill=color, width=1, tags=tag)
            self.canvas.create_line(x - 3*size/4, y_pos - size/8, x - size/4, y_pos + size/8, fill="#FF0000", width=2, tags=tag)
            self.canvas.create_line(x - 3*size/4, y_pos + size/8, x - size/4, y_pos - size/8, fill="#FF0000", width=2, tags=tag)

    def _draw_exploit(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        points = [x - size, y - size, x - size/2, y - size/2, x, y - size, 
                 x + size/2, y - size/2, x + size, y + size]
        self.canvas.create_line(points, fill="#FF4400", width=3, tags=tag)

    def _draw_vulnerability(self, x, y, size, color, tag):
        self.canvas.create_polygon(x, y - size, x - size, y, x - size/2, y + size, 
                                 x + size/2, y + size, x + size, y, outline=color, fill="", tags=tag)
        self.canvas.create_line(x - size/2, y - size/2, x + size/2, y + size/2, fill="#FF0000", width=3, tags=tag)

    def _draw_patch(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x - size, y, x + size, y, fill="#FF0000", width=2, tags=tag)
        self.canvas.create_rectangle(x - size/2, y - size/4, x + size/2, y + size/4, 
                                   fill="#00FF00", outline="#00FF00", tags=tag)

    def _draw_update(self, x, y, size, color, tag):
        self.canvas.create_arc(x - size, y - size, x + size, y + size, start=45, extent=270, 
                             style=tk.ARC, outline=color, width=2, tags=tag)
        self.canvas.create_polygon(x + size/2, y - size, x + size, y - size/2, 
                                 x + 3*size/4, y - 3*size/4, outline=color, fill=color, tags=tag)

    def _draw_backup(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x + size/2, y + size/2, outline=color, width=1, tags=tag)
        self.canvas.create_rectangle(x - size/2, y - size/2, x + size, y + size, outline=color, width=2, tags=tag)

    def _draw_restore(self, x, y, size, color, tag):
        self.canvas.create_arc(x - size, y - size, x + size, y + size, start=135, extent=270, 
                             style=tk.ARC, outline=color, width=2, tags=tag)
        self.canvas.create_polygon(x - size/2, y - size, x - size, y - size/2, 
                                 x - 3*size/4, y - 3*size/4, outline=color, fill=color, tags=tag)

    def _draw_mirror(self, x, y, size, color, tag):
        self.canvas.create_rectangle(x - size, y - size, x, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_rectangle(x, y - size, x + size, y + size, outline=color, width=1, tags=tag)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=2, tags=tag)

    def _draw_clone(self, x, y, size, color, tag):
        for i in range(3):
            offset = i * size / 4
            self.canvas.create_oval(x - size + offset, y - size + offset, 
                                  x + size/2 + offset, y + size/2 + offset, 
                                  outline=color, width=1, tags=tag)

    def _draw_sync(self, x, y, size, color, tag):
        self.canvas.create_arc(x - size, y - size/2, x, y + size/2, start=0, extent=180, 
                             style=tk.ARC, outline=color, width=2, tags=tag)
        self.canvas.create_arc(x, y - size/2, x + size, y + size/2, start=180, extent=180, 
                             style=tk.ARC, outline=color, width=2, tags=tag)
        self.canvas.create_polygon(x - size/2, y - size/2, x - 3*size/4, y - size/4, 
                                 x - 3*size/4, y - 3*size/4, outline=color, fill=color, tags=tag)
        self.canvas.create_polygon(x + size/2, y + size/2, x + 3*size/4, y + size/4, 
                                 x + 3*size/4, y + 3*size/4, outline=color, fill=color, tags=tag)


if __name__ == "__main__":
    app = SynthexTerminalEnhanced()
    app.mainloop()
