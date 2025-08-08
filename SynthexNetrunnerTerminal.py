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
    "fire": {"bg": "#3D0000", "text": "#FF4136", "accent": "#FF851B"},
    "matrix": {"bg": "#000000", "text": "#00FF41", "accent": "#00FFFF"},
    "neon": {"bg": "#191970", "text": "#F0F8FF", "accent": "#FF69B4"}
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
    def __init__(self):
        super().__init__()
        self.after_id = None  # <--- Añade esta línea
        self.title("Synthex Netrunner Terminal v2.0 - Enhanced")
        self.geometry("1600x900")
        #self.iconbitmap("synthex.ico")
    
        # Estado del sistema
        self.current_theme = "ice"
        self.system_integrity = 100
        self.threat_level = 0
        self.active_processes = []
        self.console_history = []
        self.data_flow_points = []
        self.glyph_tooltips = {}

        # Track current view for reliable restoration
        self.current_view = "start"  # Possible values: start, terminal, alphabet, encryption, decryption

        self.apply_theme()
        # --- CAMBIO AQUI: Ahora la app empieza con la pantalla de inicio ---
        self.start_screen()
        # --- FIN DEL CAMBIO ---

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
        tk.Label(self.start_frame, text="Accessing core infrastructure requires authorization...", font=("Courier", 16), fg=self.text_color, bg=self.bg_color).pack(pady=40)

        # Botones
        tk.Button(self.start_frame, text="JACK IN (Iniciar Terminal)", font=("Courier", 14, "bold"), 
                  bg=self.accent_color, fg=self.bg_color, command=self.start_terminal,
                  activebackground=self.text_color, activeforeground=self.bg_color,
                  bd=3, relief=tk.RAISED).pack(pady=10, ipadx=20, ipady=10)
        
        tk.Button(self.start_frame, text="MANUAL (Ver Guía)", font=("Courier", 14), 
                  bg=self.text_color, fg=self.bg_color, command=self.show_manual,
                  activebackground=self.accent_color, activeforeground=self.bg_color,
                  bd=3, relief=tk.RAISED).pack(pady=10, ipadx=20, ipady=10)
    
    def start_terminal(self):
        """Destruye la pantalla de inicio y crea la terminal"""
        self.current_view = "terminal"
        self.start_frame.destroy()
        self.setup_ui()
        self.start_animations()
        self.write_to_console("=== SYNTHEX TERMINAL v2.0 INITIALIZED ===")
        self.write_to_console("Type 'help' for available commands")
        self.write_to_console("Type 'man' for Synthex language manual")
        self.write_to_console("Type 'test' to visualize glyph constellations")
    # --- FIN DE LAS NUEVAS FUNCIONES ---

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self, bg=self.bg_color, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel superior - Status y controles
        top_frame = tk.Frame(main_frame, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # Status del sistema
        status_frame = tk.LabelFrame(top_frame, text="System Status", bg=self.bg_color, 
                                   fg=self.text_color, font=("Courier", 10))
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.integrity_label = tk.Label(status_frame, text="Integrity: 100%", 
                                      bg=self.bg_color, fg=self.accent_color, font=("Courier", 9))
        self.integrity_label.pack(side=tk.LEFT, padx=5)

        self.threat_label = tk.Label(status_frame, text="Threat: SECURE", 
                                   bg=self.bg_color, fg=self.accent_color, font=("Courier", 9))
        self.threat_label.pack(side=tk.LEFT, padx=5)

        # Controles de tema
        theme_frame = tk.LabelFrame(top_frame, text="Theme", bg=self.bg_color, 
                                  fg=self.text_color, font=("Courier", 10))
        theme_frame.pack(side=tk.RIGHT)

        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                 values=list(THEMES.keys()), state="readonly", width=10)
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)

        # Frame del medio - Console y visualización
        middle_frame = tk.Frame(main_frame, bg=self.bg_color)
        middle_frame.pack(fill=tk.BOTH, expand=True)

        # Console integrada (izquierda)
        console_frame = tk.LabelFrame(middle_frame, text="Synthex Console", 
                                    bg=self.bg_color, fg=self.text_color, 
                                    font=("Courier", 12), padx=10, pady=10)
        console_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Área de output de la consola
        self.console_output = tk.Text(console_frame, height=25, bg=self.bg_color, 
                                    fg=self.accent_color, font=("Courier", 10),
                                    state=tk.DISABLED, wrap=tk.WORD)
        console_scrollbar = tk.Scrollbar(console_frame, command=self.console_output.yview)
        self.console_output.config(yscrollcommand=console_scrollbar.set)
        
        self.console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame de input
        input_frame = tk.Frame(console_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(input_frame, text=">>", bg=self.bg_color, fg=self.text_color, 
                font=("Courier", 12, "bold")).pack(side=tk.LEFT)

        self.console_input = tk.Entry(input_frame, bg=self.bg_color, fg=self.accent_color,
                                    font=("Courier", 12), insertbackground=self.accent_color)
        self.console_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.console_input.bind('<Return>', self.process_console_command)

            # Canvas de visualización (derecha)
        viz_frame = tk.LabelFrame(middle_frame, text="Network Visualization", 
                                bg=self.bg_color, fg=self.text_color, font=("Courier", 12))
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        # Ajusta el ancho aquí
        self.canvas = tk.Canvas(viz_frame, bg=self.bg_color, highlightthickness=1, 
                               highlightbackground=self.text_color, width=900)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        # Bind para tooltips
        self.canvas.bind('<Motion>', self.show_glyph_tooltip)
        self.canvas.bind('<Button-1>', self.on_glyph_click)

        # Panel inferior - Controles adicionales
        bottom_frame = tk.Frame(main_frame, bg=self.bg_color)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))

        # Botones de acción
        tk.Button(bottom_frame, text="Clear Console", command=self.clear_console,
                 bg=self.text_color, fg=self.bg_color, font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="System Scan", command=self.system_scan,
                 bg=self.accent_color, fg=self.bg_color, font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="Emergency Reset", command=self.emergency_reset,
                 bg="#FF4444", fg=self.bg_color, font=("Courier", 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="Exit", command=self.on_close,
                 bg="#555555", fg=self.bg_color, font=("Courier", 10)).pack(side=tk.RIGHT, padx=5)

        # Almacenamiento para glifos y animaciones
        self.glyph_coords = {}
        self.current_glyphs = []
        # --- NUEVO: diccionario para guardar a qué constelación pertenece cada glifo ---
        self.glyph_constellation_map = {}
        
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

        # Procesar comandos especiales
        if command == "help":
            self.show_help()
        elif command == "man":
            self.show_manual()
        # --- AÑADE ESTA LÍNEA ---
        elif command == "alpha":
            self.show_synthex_alphabet()
        # --- FIN DEL CÓDIGO A AÑADIR ---
        elif command == "enc":
            self.show_encryption_view()
        elif command == "dec":
            self.show_decryption_view()
        elif command == "clear":
            self.clear_console()
        elif command == "status":
            self.show_system_status()
        elif command == "scan":
            self.system_scan()
        elif command == "reset":
            self.emergency_reset()
        elif command == "test":
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
        elif self.is_attack_command(command):
            self.simulate_attack(command)
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
            self.current_theme = selected_theme
            self.apply_theme()
            # Guarda el historial de la consola y los glifos actuales
            saved_console = self.console_output.get("1.0", tk.END) if hasattr(self, "console_output") else ""
            saved_glyphs = list(self.current_glyphs) if hasattr(self, "current_glyphs") else []
            saved_view = self.current_view

            # Destruye todos los widgets y reconstruye la interfaz principal
            for widget in self.winfo_children():
                widget.destroy()
            self.setup_ui()

            # Restaura el historial de la consola
            if saved_console and hasattr(self, "console_output"):
                self.console_output.config(state=tk.NORMAL)
                self.console_output.delete("1.0", tk.END)
                self.console_output.insert("1.0", saved_console)
                self.console_output.config(state=tk.DISABLED)
                self.console_output.see(tk.END)

            # Restaura la visualización de los glifos
            if saved_glyphs and hasattr(self, "canvas"):
                self.visualize_synthex_network(saved_glyphs)

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
        close_advisor.bind("<Button-1>", lambda e: self.return_to_start_screen())

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

    def return_to_start_screen(self):
        """Destruye la vista del alfabeto y regresa a la pantalla de la terminal."""
        # Destruye el frame del alfabeto si existe
        if hasattr(self, 'alphabet_frame') and self.alphabet_frame:
            self.alphabet_frame.destroy()
        
        # Llama a la función que crea la pantalla de la terminal
        self.start_terminal()     

    def show_encryption_view(self):
        """Muestra una interfaz de encriptación con un estilo más cyberpunk."""
        self.current_view = "encryption"
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
        close_advisor.bind("<Button-1>", lambda e: self.return_to_terminal())

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
        # --- CAMBIO IMPORTANTE AQUÍ: Se asegura que el texto esté en minúsculas ---
        input_text = self.input_text_area.get("1.0", tk.END).strip().lower()
        words = input_text.split()
        encrypted_glyphs = []
        
        for word in words:
            # Si la palabra existe en el diccionario, usa el pictograma
            if word in SYNTHEX_DICTIONARY:
                encrypted_glyphs.append(SYNTHEX_DICTIONARY[word])
            # Si no existe, usa un marcador de palabra desconocida
            else:
                encrypted_glyphs.append(f"[UNK_WORD]")
        
        # --- CAMBIO IMPORTANTE AQUÍ: Unir los pictogramas con un guion ---
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
            self.console_status.config(text="Encrypted message copied to clipboard.")
            self.after(2000, lambda: self.console_status.config(text=""))   

    def return_to_terminal(self):
        """Destruye la vista de encriptación y regresa a la pantalla de la terminal."""
        if hasattr(self, 'encryption_frame') and self.encryption_frame:
            self.encryption_frame.destroy()
        
        # Llama a la función start_terminal para reconstruir la vista y reiniciar la animación
        self.start_terminal()      

    def show_decryption_view(self):
        """Muestra una interfaz para desencriptar mensajes usando los pictogramas Synthex."""
        self.current_view = "decryption"
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
        close_advisor.bind("<Button-1>", lambda e: self.return_to_terminal())

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

    def return_to_terminal(self):
        """Destruye la vista de desencriptación o encriptación y regresa a la pantalla de la terminal."""
        if hasattr(self, 'decryption_frame') and self.decryption_frame:
            self.decryption_frame.destroy()
        elif hasattr(self, 'encryption_frame') and self.encryption_frame:
            self.encryption_frame.destroy()
        
        self.start_terminal()     

    def decrypt_message(self):
        """Toma los pictogramas de entrada y los desencripta a palabras Synthex."""
        input_text = self.input_text_area.get("1.0", tk.END).strip()
        # Se asume que los pictogramas están separados por guiones
        glyphs = input_text.split("—")
        decrypted_words = []
        
        for glyph in glyphs:
            # Si el pictograma existe en el diccionario inverso, usa la palabra
            if glyph in REV_SYNTHEX_DICTIONARY:
                decrypted_words.append(REV_SYNTHEX_DICTIONARY[glyph])
            # Si no existe, usa un marcador de pictograma desconocido
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
            self.console_status.config(text="Decrypted message copied to clipboard.")
            self.after(2000, lambda: self.console_status.config(text=""))   


    def show_blackwall(self):
        """Dibuja el efecto del Muro Negro."""
        self.canvas.delete("all")
        self.write_to_console("WARNING: BLACKWALL PROTOCOL ACTIVATED - SYSTEM INTEGRITY LOST", "#FF0000")
        self.write_to_console("ATTEMPTING TO CONTAIN HOSTILE ENTITIES...", "#FF4400")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        symbols = "0123456789ABCDEF!@#$%^&*"
        
        for _ in range(500):
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            char = random.choice(symbols)
            size = random.randint(8, 20)
            
            color = random.choice(["#FF0000", "#FF4400", "#FF8800"])
            self.canvas.create_text(x + random.randint(-3, 3), y + random.randint(-3, 3),
                                    text=char, fill=color, font=("Consolas", size), tags="blackwall")

        for _ in range(100):
            x1, y1 = random.randint(0, canvas_width), random.randint(0, canvas_height)
            x2, y2 = random.randint(0, canvas_width), random.randint(0, canvas_height)
            self.canvas.create_line(x1, y1, x2, y2, fill="#FF4400", width=1, dash=(2, 1), tags="blackwall")

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

        is_chaotic = UNKNOWN_GLYPH in glyphs or self.threat_level > 50
        
        if not glyphs:
            return

        if is_chaotic:
            for i, glyph in enumerate(glyphs):
                x = random.randint(50, canvas_width - 50)
                y = random.randint(50, canvas_height - 50)
                self.glyph_coords[i] = (x, y)
                
                color = self.get_glyph_color(glyph)
                self.draw_glyph_shape(glyph, x, y, 20, color)
                
                word = REV_SYNTHEX_DICTIONARY.get(glyph, "unknown")
                self.glyph_tooltips[i] = f"{glyph} - {word}"
        else:
            num_glyphs = len(glyphs)
            center_x, center_y = canvas_width / 2, canvas_height / 2
            radius = min(canvas_width, canvas_height) / 3
            
            for i, glyph in enumerate(glyphs):
                angle = i * (2 * math.pi / num_glyphs)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                self.glyph_coords[i] = (x, y)
                
                color = self.get_glyph_color(glyph)
                self.draw_glyph_shape(glyph, x, y, 20, color)
                
                word = REV_SYNTHEX_DICTIONARY.get(glyph, "unknown")
                self.glyph_tooltips[i] = f"{glyph} - {word}"

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
        if len(self.glyph_coords) < 2:
            return
        
        if is_chaotic:
            num_connections = min(len(self.glyph_coords) * 2, 20)
            for _ in range(num_connections):
                i, j = random.sample(list(self.glyph_coords.keys()), 2)
                x1, y1 = self.glyph_coords[i]
                x2, y2 = self.glyph_coords[j]
                
                self.canvas.create_line(x1, y1, x2, y2, fill="#FF4400", 
                                      width=2, dash=(3, 2), tags="connection")
        else:
            indices = list(self.glyph_coords.keys())
            for i in range(len(indices)):
                j = (i + 1) % len(indices)
                x1, y1 = self.glyph_coords[indices[i]]
                x2, y2 = self.glyph_coords[indices[j]]
                
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
        
        # Iterar a través de los glifos dibujados
        for index, (x, y) in self.glyph_coords.items():
            distance = math.sqrt((click_x - x)**2 + (click_y - y)**2)
            if distance < min_distance and distance < 20: # Radio de clic
                min_distance = distance
                closest_glyph_index = index
        
        if closest_glyph_index is not None:
            # Obtener el tooltip del glifo
            tooltip_text = self.glyph_tooltips.get(closest_glyph_index, "Unknown glyph")
            # Obtener el nombre de la constelación si existe
            constellation_name = self.glyph_constellation_map.get(closest_glyph_index, "No Constellation")
            
            self.write_to_console(f"Glyph selected: {tooltip_text} (Constellation: {constellation_name})", "#FFFF00")

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