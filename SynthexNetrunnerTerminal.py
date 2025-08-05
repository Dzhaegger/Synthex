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

# Configuración de temas
THEMES = {
    "classic": {"bg": "#000000", "text": "#FF0000", "accent": "#00FF00"},
    "ice": {"bg": "#001122", "text": "#00CCFF", "accent": "#FFFFFF"},
    "fire": {"bg": "#110000", "text": "#FF4400", "accent": "#FFAA00"},
    "matrix": {"bg": "#000000", "text": "#00FF00", "accent": "#FFFFFF"},
    "neon": {"bg": "#0A0A0A", "text": "#FF00FF", "accent": "#00FFFF"}
}

class SynthexTerminalEnhanced(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Synthex Netrunner Terminal v2.0 - Enhanced")
        self.geometry("1600x900")
        
        # Estado del sistema
        self.current_theme = "classic"
        self.system_integrity = 100
        self.threat_level = 0
        self.active_processes = []
        self.console_history = []
        self.data_flow_points = []
        self.glyph_tooltips = {}
        
        self.apply_theme()
        self.setup_ui()
        self.start_animations()

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.bg_color = theme["bg"]
        self.text_color = theme["text"]
        self.accent_color = theme["accent"]
        self.configure(bg=self.bg_color)

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
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(viz_frame, bg=self.bg_color, highlightthickness=1, 
                               highlightbackground=self.text_color)
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

        # Almacenamiento para glifos y animaciones
        self.glyph_coords = {}
        self.current_glyphs = []
        
        # Inicializar console
        self.write_to_console("=== SYNTHEX TERMINAL v2.0 INITIALIZED ===")
        self.write_to_console("Type 'help' for available commands")
        self.write_to_console("Type 'man' for Synthex language manual")

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
        elif command == "clear":
            self.clear_console()
        elif command == "status":
            self.show_system_status()
        elif command == "scan":
            self.system_scan()
        elif command == "reset":
            self.emergency_reset()
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
                self.system_integrity -= random.randint(10, 30)
                self.threat_level += random.randint(20, 50)
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
  encrypt <text>- Encrypt text to Synthex
  decrypt <code>- Decrypt Synthex code
  
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
        """Actualiza los labels de estado"""
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

    def system_scan(self):
        """Simula un escaneo del sistema"""
        self.write_to_console("Initiating system scan...", "#FFFF00")
        
        # Simular proceso de escaneo
        def scan_process():
            scan_items = ["Memory sectors", "Network interfaces", "Security protocols", 
                         "Data integrity", "Threat signatures"]
            
            for item in scan_items:
                time.sleep(0.5)
                self.after(0, lambda i=item: self.write_to_console(f"Scanning {i}...", "#00FFFF"))
            
            # Resultados aleatorios
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

    def change_theme(self, event=None):
        """Cambia el tema de la aplicación"""
        self.current_theme = self.theme_var.get()
        self.apply_theme()
        
        # Actualizar todos los widgets con los nuevos colores
        self.setup_ui()
        self.write_to_console(f"Theme changed to: {self.current_theme}", "#FFFF00")

    def clear_console(self):
        """Limpia la consola"""
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete(1.0, tk.END)
        self.console_output.config(state=tk.DISABLED)
        self.write_to_console("Console cleared.")

    def visualize_synthex_network(self, glyphs, original_text=""):
        """Visualiza la red Synthex en el canvas"""
        self.canvas.delete("all")
        self.glyph_coords.clear()
        self.glyph_tooltips.clear()
        self.current_glyphs = glyphs
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(50, lambda: self.visualize_synthex_network(glyphs, original_text))
            return

        # Determinar si es caótico
        is_chaotic = UNKNOWN_GLYPH in glyphs or self.threat_level > 50
        
        if not glyphs:
            return

        # Posicionar glifos
        if is_chaotic:
            # Distribución caótica
            for i, glyph in enumerate(glyphs):
                x = random.randint(50, canvas_width - 50)
                y = random.randint(50, canvas_height - 50)
                self.glyph_coords[i] = (x, y)
                
                color = self.get_glyph_color(glyph)
                self.draw_glyph_shape(glyph, x, y, 20, color)
                
                # Agregar tooltip info
                word = REV_SYNTHEX_DICTIONARY.get(glyph, "unknown")
                self.glyph_tooltips[i] = f"{glyph} - {word}"
        else:
            # Distribución ordenada en círculo
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
                
                # Agregar tooltip info
                word = REV_SYNTHEX_DICTIONARY.get(glyph, "unknown")
                self.glyph_tooltips[i] = f"{glyph} - {word}"

        # Dibujar conexiones
        self.draw_connections(is_chaotic)

    def get_glyph_color(self, glyph):
        """Determina el color del glifo basado en su tipo"""
        word = REV_SYNTHEX_DICTIONARY.get(glyph, "")
        
        # Colores según tipo de glifo
        if word in ["breach", "corrupt", "virus", "worm", "trojan", "threat", "error"]:
            return "#FF0000"  # Rojo para amenazas
        elif word in ["firewall", "security", "stable", "access", "backup"]:
            return "#00FF00"  # Verde para seguridad
        elif word in ["ai", "sentience", "construct", "entity"]:
            return "#00FFFF"  # Cyan para IA
        else:
            return self.text_color  # Color normal

    def draw_connections(self, is_chaotic):
        """Dibuja conexiones entre glifos"""
        if len(self.glyph_coords) < 2:
            return
        
        if is_chaotic:
            # Conexiones caóticas
            num_connections = min(len(self.glyph_coords) * 2, 20)
            for _ in range(num_connections):
                i, j = random.sample(list(self.glyph_coords.keys()), 2)
                x1, y1 = self.glyph_coords[i]
                x2, y2 = self.glyph_coords[j]
                
                self.canvas.create_line(x1, y1, x2, y2, fill="#FF4400", 
                                      width=2, dash=(3, 2), tags="connection")
        else:
            # Conexiones ordenadas
            indices = list(self.glyph_coords.keys())
            for i in range(len(indices)):
                j = (i + 1) % len(indices)
                x1, y1 = self.glyph_coords[indices[i]]
                x2, y2 = self.glyph_coords[indices[j]]
                
                self.canvas.create_line(x1, y1, x2, y2, fill=self.accent_color, 
                                      width=1, dash=(5, 3), tags="connection")

    def show_glyph_tooltip(self, event):
        """Muestra tooltip al pasar sobre un glifo"""
        # Esta funcionalidad se puede expandir para mostrar información detallada
        pass

    def on_glyph_click(self, event):
        """Maneja clicks en glifos"""
        # Encontrar el glifo más cercano al click
        click_x, click_y = event.x, event.y
        min_distance = float('inf')
        closest_glyph = None
        
        for i, (x, y) in self.glyph_coords.items():
            distance = math.sqrt((click_x - x)**2 + (click_y - y)**2)
            if distance < min_distance and distance < 30:  # Radio de 30 píxeles
                min_distance = distance
                closest_glyph = i
        
        if closest_glyph is not None:
            tooltip_text = self.glyph_tooltips.get(closest_glyph, "Unknown glyph")
            self.write_to_console(f"Glyph selected: {tooltip_text}", "#FFFF00")

    def start_animations(self):
        """Inicia las animaciones del canvas"""
        self.animate_connections()
        self.animate_data_flow()

    def animate_connections(self):
        """Anima las conexiones"""
        connections = self.canvas.find_withtag("connection")
        for conn in connections:
            current_color = self.canvas.itemcget(conn, "fill")
            if current_color == self.accent_color:
                new_color = self.text_color
            else:
                new_color = self.accent_color
            self.canvas.itemconfig(conn, fill=new_color)
        
        self.after(500, self.animate_connections)

    def animate_data_flow(self):
        """Anima flujo de datos"""
        # Crear puntos de datos que se mueven por las conexiones
        if len(self.glyph_coords) >= 2 and random.random() < 0.3:
            # Seleccionar dos glifos aleatorios
            indices = list(self.glyph_coords.keys())
            start_idx, end_idx = random.sample(indices, 2)
            start_x, start_y = self.glyph_coords[start_idx]
            end_x, end_y = self.glyph_coords[end_idx]
            
            # Crear punto de datos
            point = self.canvas.create_oval(start_x-2, start_y-2, start_x+2, start_y+2,
                                          fill="#FFFFFF", outline="", tags="dataflow")
            
            # Animar movimiento
            self.animate_point_to_target(point, start_x, start_y, end_x, end_y, 0)
        
        self.after(1000, self.animate_data_flow)

    def animate_point_to_target(self, point, start_x, start_y, end_x, end_y, step):
        """Anima un punto de datos moviéndose de un glifo a otro"""
        if step > 20:  # 20 pasos para completar la animación
            self.canvas.delete(point)
            return
        
        # Calcular posición interpolada
        progress = step / 20.0
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        
        # Mover el punto
        coords = self.canvas.coords(point)
        if coords:  # Verificar que el punto aún existe
            self.canvas.coords(point, current_x-2, current_y-2, current_x+2, current_y+2)
            self.after(50, lambda: self.animate_point_to_target(point, start_x, start_y, end_x, end_y, step + 1))

    def show_manual(self):
        """Muestra el manual de Synthex expandido"""
        manual_window = tk.Toplevel(self)
        manual_window.title("Synthex Language Manual v2.0")
        manual_window.geometry("900x700")
        manual_window.configure(bg=self.bg_color)

        # Frame con scrollbar
        main_frame = tk.Frame(manual_window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Text widget con scrollbar
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

    # Métodos de dibujo de glifos (mantener todos los originales y agregar nuevos)
    def draw_glyph_shape(self, glyph, x, y, size, color):
        """Dibuja la forma correspondiente a un glifo"""
        shape_name = GLYPH_SHAPES.get(glyph, "unknown")
        
        # Glifos básicos (mantener todos los métodos originales)
        if shape_name == "square_block": self._draw_square_block(x, y, size, color)
        elif shape_name == "omega": self._draw_omega(x, y, size, color)
        elif shape_name == "dotted_block": self._draw_dotted_block(x, y, size, color)
        elif shape_name == "solid_block": self._draw_solid_block(x, y, size, color)
        elif shape_name == "circle_plus": self._draw_circle_plus(x, y, size, color)
        elif shape_name == "psi": self._draw_psi(x, y, size, color)
        elif shape_name == "phi": self._draw_phi(x, y, size, color)
        elif shape_name == "section": self._draw_section(x, y, size, color)
        elif shape_name == "triangle": self._draw_triangle(x, y, size, color)
        elif shape_name == "left_right_arrow": self._draw_left_right_arrow(x, y, size, color)
        elif shape_name == "sigma": self._draw_sigma(x, y, size, color)
        elif shape_name == "star": self._draw_star(x, y, size, color)
        elif shape_name == "rectangle": self._draw_rectangle(x, y, size, color)
        elif shape_name == "double_tilde": self._draw_double_tilde(x, y, size, color)
        elif shape_name == "circle_slash": self._draw_circle_slash(x, y, size, color)
        elif shape_name == "house": self._draw_house(x, y, size, color)
        elif shape_name == "infinity": self._draw_infinity(x, y, size, color)
        elif shape_name == "circle_dot": self._draw_circle_dot(x, y, size, color)
        elif shape_name == "protocol": self._draw_protocol(x, y, size, color)
        elif shape_name == "firewall": self._draw_firewall(x, y, size, color)
        elif shape_name == "down_arrow": self._draw_down_arrow(x, y, size, color)
        elif shape_name == "up_arrow": self._draw_up_arrow(x, y, size, color)
        elif shape_name == "construct": self._draw_construct(x, y, size, color)
        elif shape_name == "question_box": self._draw_question_box(x, y, size, color)
        elif shape_name == "sentience": self._draw_sentience(x, y, size, color)
        elif shape_name == "anomaly": self._draw_anomaly(x, y, size, color)
        elif shape_name == "data_stream": self._draw_data_stream(x, y, size, color)
        elif shape_name == "probe": self._draw_probe(x, y, size, color)
        elif shape_name == "divert": self._draw_divert(x, y, size, color)
        elif shape_name == "corrupt": self._draw_corrupt(x, y, size, color)
        elif shape_name == "nullify": self._draw_nullify(x, y, size, color)
        elif shape_name == "access": self._draw_access(x, y, size, color)
        elif shape_name == "security": self._draw_security(x, y, size, color)
        elif shape_name == "core": self._draw_core(x, y, size, color)
        elif shape_name == "digital": self._draw_digital(x, y, size, color)
        elif shape_name == "reality": self._draw_reality(x, y, size, color)
        elif shape_name == "interface": self._draw_interface(x, y, size, color)
        elif shape_name == "threat": self._draw_threat(x, y, size, color)
        elif shape_name == "man": self._draw_man(x, y, size, color)
        
        # Nuevos glifos
        elif shape_name == "keyboard": self._draw_keyboard(x, y, size, color)
        elif shape_name == "admin_key": self._draw_admin_key(x, y, size, color)
        elif shape_name == "backdoor": self._draw_backdoor(x, y, size, color)
        elif shape_name == "botnet": self._draw_botnet(x, y, size, color)
        elif shape_name == "virus": self._draw_virus(x, y, size, color)
        elif shape_name == "worm": self._draw_worm(x, y, size, color)
        elif shape_name == "trojan": self._draw_trojan(x, y, size, color)
        elif shape_name == "keylogger": self._draw_keylogger(x, y, size, color)
        elif shape_name == "ransomware": self._draw_ransomware(x, y, size, color)
        elif shape_name == "spyware": self._draw_spyware(x, y, size, color)
        elif shape_name == "malware": self._draw_malware(x, y, size, color)
        elif shape_name == "honeypot": self._draw_honeypot(x, y, size, color)
        elif shape_name == "sandbox": self._draw_sandbox(x, y, size, color)
        elif shape_name == "quarantine": self._draw_quarantine(x, y, size, color)
        elif shape_name == "whitelist": self._draw_whitelist(x, y, size, color)
        elif shape_name == "blacklist": self._draw_blacklist(x, y, size, color)
        elif shape_name == "exploit": self._draw_exploit(x, y, size, color)
        elif shape_name == "vulnerability": self._draw_vulnerability(x, y, size, color)
        elif shape_name == "patch": self._draw_patch(x, y, size, color)
        elif shape_name == "update": self._draw_update(x, y, size, color)
        elif shape_name == "backup": self._draw_backup(x, y, size, color)
        elif shape_name == "restore": self._draw_restore(x, y, size, color)
        elif shape_name == "mirror": self._draw_mirror(x, y, size, color)
        elif shape_name == "clone": self._draw_clone(x, y, size, color)
        elif shape_name == "sync": self._draw_sync(x, y, size, color)
        else:
            # Glifo desconocido
            self.canvas.create_rectangle(x-size, y-size, x+size, y+size, outline=color)
            self.canvas.create_text(x, y, text="?", fill=color, font=("Courier", 18, "bold"))

    # Métodos de dibujo originales (mantener todos)
    def _draw_square_block(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)

    def _draw_omega(self, x, y, size, color):
        points = [x - size, y + size, x - size / 2, y - size, x + size / 2, y - size, x + size, y + size]
        self.canvas.create_line(points, fill=color, width=1)
        self.canvas.create_arc(x - size, y - size/2, x + size, y + size/2, start=180, extent=180, outline=color, style=tk.ARC, width=1)

    def _draw_dotted_block(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
    
    def _draw_solid_block(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=color, outline=color)
    
    def _draw_circle_plus(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)

    def _draw_psi(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        
    def _draw_phi(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)

    def _draw_section(self, x, y, size, color):
        self.canvas.create_arc(x - size, y - size, x, y, start=90, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x, y, x + size, y + size, start=270, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y, x, y+size, fill=color, width=1)
        self.canvas.create_line(x, y, x, y-size, fill=color, width=1)

    def _draw_triangle(self, x, y, size, color):
        self.canvas.create_polygon(x, y - size, x - size, y + size, x + size, y + size, outline=color, fill="")

    def _draw_left_right_arrow(self, x, y, size, color):
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y - size / 2, fill=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y + size / 2, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y - size / 2, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y + size / 2, fill=color, width=1)

    def _draw_sigma(self, x, y, size, color):
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1)
        self.canvas.create_line(x + size, y + size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x, y, fill=color, width=1)
        self.canvas.create_line(x, y, x - size, y + size, fill=color, width=1)

    def _draw_star(self, x, y, size, color):
        points = []
        for i in range(5):
            angle = math.pi/2 + i * (2*math.pi / 5)
            x_point = x + size * math.cos(angle)
            y_point = y - size * math.sin(angle)
            points.append((x_point, y_point))
        self.canvas.create_polygon(points, outline=color, fill="", width=1)

    def _draw_rectangle(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)

    def _draw_double_tilde(self, x, y, size, color):
        self.canvas.create_arc(x - size, y - size, x + size, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)

    def _draw_circle_slash(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)

    def _draw_house(self, x, y, size, color):
        self.canvas.create_polygon(x, y - size, x - size, y, x + size, y, outline=color, fill="")
        self.canvas.create_rectangle(x - size, y, x + size, y + size, outline=color)
        
    def _draw_infinity(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size/2, x, y + size/2, outline=color, width=1)
        self.canvas.create_oval(x, y - size/2, x + size, y + size/2, outline=color, width=1)

    def _draw_circle_dot(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)

    def _draw_protocol(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)

    def _draw_firewall(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x - size/2, y - size, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size/2, y - size, fill=color, width=1)

    def _draw_down_arrow(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y + size / 2, x, y + size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y + size / 2, x, y + size, fill=color, width=1)
    
    def _draw_up_arrow(self, x, y, size, color):
        self.canvas.create_line(x, y + size, x, y - size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y - size / 2, x, y - size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y - size / 2, x, y - size, fill=color, width=1)

    def _draw_construct(self, x, y, size, color):
        self.canvas.create_oval(x - size/2, y - size, x + size/2, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_question_box(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color)
        self.canvas.create_arc(x - size/2, y-size, x + size/2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y, x, y + size / 2, fill=color, width=1)

    def _draw_sentience(self, x, y, size, color):
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size/2, y + size, x, y-size, fill=color, width=1)
        self.canvas.create_line(x + size/2, y + size, x, y-size, fill=color, width=1)

    def _draw_anomaly(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size/2, y - size, x + size/2, y + size, fill=color, width=1)
        self.canvas.create_line(x + size/2, y - size, x - size/2, y + size, fill=color, width=1)

    def _draw_data_stream(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size/2, x, y + size/2, outline=color)
        self.canvas.create_oval(x, y - size/2, x + size, y + size/2, outline=color)
        self.canvas.create_line(x, y - size/2, x, y + size/2, fill=color)

    def _draw_probe(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color)
        self.canvas.create_oval(x - size, y, x, y + size, outline=color)
    
    def _draw_divert(self, x, y, size, color):
        self.canvas.create_arc(x - size, y - size, x + size/2, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size/2, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)

    def _draw_corrupt(self, x, y, size, color):
        self._draw_star(x - size/2, y, size/2, color)
        self.canvas.create_arc(x + size/2, y - size/2, x + size, y + size/2, start=0, extent=180, style=tk.ARC, outline=color, width=1)

    def _draw_nullify(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
    
    def _draw_access(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)

    def _draw_security(self, x, y, size, color):
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)

    def _draw_core(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)

    def _draw_digital(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size/2, y + size, outline=color, width=1)
        self.canvas.create_rectangle(x - size/2, y - size, x + size, y + size, outline=color, width=1)

    def _draw_reality(self, x, y, size, color):
        self._draw_infinity(x - size/2, y, size, color)
        self._draw_infinity(x + size/2, y, size, color)

    def _draw_interface(self, x, y, size, color):
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x + size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)

    def _draw_threat(self, x, y, size, color):
        self.canvas.create_polygon(x, y - size, x - size/2, y + size/2, x + size/2, y + size/2, outline=color, fill="")
        self.canvas.create_line(x - size/2, y+size, x + size/2, y+size, fill=color, width=1)
    
    def _draw_man(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_arc(x - size, y-size, x, y, start=90, extent=90, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x, y-size, x+size, y, start=0, extent=90, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x-size, y, x, y+size, start=180, extent=90, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x, y, x+size, y+size, start=270, extent=90, style=tk.ARC, outline=color, width=1)

    # Nuevos métodos de dibujo para glifos expandidos
    def _draw_keyboard(self, x, y, size, color):
        """Dibuja el glifo '⌨' (root/keyboard)"""
        self.canvas.create_rectangle(x - size, y - size/2, x + size, y + size/2, outline=color, width=1)
        # Teclas pequeñas
        for i in range(-2, 3):
            for j in range(-1, 2):
                self.canvas.create_rectangle(x + i*size/3, y + j*size/4, 
                                           x + (i+0.5)*size/3, y + (j+0.5)*size/4, 
                                           outline=color, width=1)

    def _draw_admin_key(self, x, y, size, color):
        """Dibuja el glifo '⌬' (admin)"""
        # Forma de llave
        self.canvas.create_oval(x - size/2, y - size, x + size/2, y - size/2, outline=color, width=1)
        self.canvas.create_line(x, y - size/2, x, y + size, fill=color, width=1)
        self.canvas.create_line(x, y, x + size/2, y, fill=color, width=1)
        self.canvas.create_line(x, y + size/2, x + size/3, y + size/2, fill=color, width=1)

    def _draw_backdoor(self, x, y, size, color):
        """Dibuja el glifo '⌹' (backdoor)"""
        # Puerta con abertura oculta
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size/2, y - size, x - size/2, y + size, fill=color, width=1)
        self.canvas.create_oval(x - size/3, y - size/4, x - size/6, y, fill=color, outline=color)

    def _draw_botnet(self, x, y, size, color):
        """Dibuja el glifo '⌶' (botnet)"""
        # Red de nodos conectados
        center_positions = [(x, y-size/2), (x-size/2, y+size/2), (x+size/2, y+size/2)]
        for pos in center_positions:
            self.canvas.create_oval(pos[0]-3, pos[1]-3, pos[0]+3, pos[1]+3, fill=color, outline=color)
        # Conexiones
        for i in range(len(center_positions)):
            for j in range(i+1, len(center_positions)):
                self.canvas.create_line(center_positions[i][0], center_positions[i][1],
                                      center_positions[j][0], center_positions[j][1], fill=color, width=1)

    def _draw_virus(self, x, y, size, color):
        """Dibuja el glifo '⌼' (virus)"""
        # Forma viral con espinas
        self.canvas.create_oval(x - size/2, y - size/2, x + size/2, y + size/2, outline=color, width=1)
        for i in range(8):
            angle = i * math.pi / 4
            x1 = x + (size/2) * math.cos(angle)
            y1 = y + (size/2) * math.sin(angle)
            x2 = x + size * math.cos(angle)
            y2 = y + size * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    def _draw_worm(self, x, y, size, color):
        """Dibuja el glifo '⌿' (worm)"""
        # Forma serpenteante
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            wave_x = x + (i - 5) * size / 5
            wave_y = y + size/2 * math.sin(angle * 2)
            points.extend([wave_x, wave_y])
        self.canvas.create_line(points, fill=color, width=2, smooth=True)

    def _draw_trojan(self, x, y, size, color):
        """Dibuja el glifo '⍀' (trojan)"""
        # Caballo de Troya estilizado
        self.canvas.create_rectangle(x - size, y, x + size, y + size, outline=color, width=1)
        self.canvas.create_polygon(x - size/2, y, x, y - size, x + size/2, y, outline=color, fill="")
        self.canvas.create_oval(x - size/4, y + size/4, x + size/4, y + 3*size/4, outline=color, width=1)

    def _draw_keylogger(self, x, y, size, color):
        """Dibuja el glifo '⍁' (keylogger)"""
        # Teclado con ojo
        self.canvas.create_rectangle(x - size, y, x + size, y + size/2, outline=color, width=1)
        self.canvas.create_oval(x - size/3, y - size, x + size/3, y - size/3, outline=color, width=1)
        self.canvas.create_oval(x - size/6, y - 5*size/6, x + size/6, y - 2*size/3, fill=color, outline=color)

    def _draw_ransomware(self, x, y, size, color):
        """Dibuja el glifo '⍂' (ransomware)"""
        # Candado con signo de dinero
        self.canvas.create_rectangle(x - size/2, y, x + size/2, y + size, outline=color, width=1)
        self.canvas.create_arc(x - size/2, y - size, x + size/2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_text(x, y + size/2, text="$", fill=color, font=("Courier", int(size), "bold"))

    def _draw_spyware(self, x, y, size, color):
        """Dibuja el glifo '⍃' (spyware)"""
        # Ojo con antena
        self.canvas.create_oval(x - size, y - size/2, x + size, y + size/2, outline=color, width=1)
        self.canvas.create_oval(x - size/3, y - size/6, x + size/3, y + size/6, fill=color, outline=color)
        self.canvas.create_line(x, y - size/2, x, y - size, fill=color, width=1)
        self.canvas.create_line(x - size/4, y - 3*size/4, x + size/4, y - 3*size/4, fill=color, width=1)

    def _draw_malware(self, x, y, size, color):
        """Dibuja el glifo '⍄' (malware)"""
        # Código malicioso estilizado
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size/2, x + size, y - size/2, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x - size, y + size/2, x + size, y + size/2, fill=color, width=1)
        # X sobre el código
        self.canvas.create_line(x - size/2, y - size/2, x + size/2, y + size/2, fill="#FF0000", width=2)
        self.canvas.create_line(x - size/2, y + size/2, x + size/2, y - size/2, fill="#FF0000", width=2)

    def _draw_honeypot(self, x, y, size, color):
        """Dibuja el glifo '⍅' (honeypot)"""
        # Tarro de miel con trampa
        self.canvas.create_oval(x - size, y - size/2, x + size, y + size, outline=color, width=1)
        self.canvas.create_rectangle(x - size/3, y - size, x + size/3, y - size/2, outline=color, width=1)
        self.canvas.create_polygon(x - size/2, y, x, y - size/4, x + size/2, y, outline="#FF4400", fill="")

    def _draw_sandbox(self, x, y, size, color):
        """Dibuja el glifo '⍆' (sandbox)"""
        # Caja de arena con límites
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=2)
        self.canvas.create_rectangle(x - size/2, y - size/2, x + size/2, y + size/2, outline=color, width=1, dash=(3, 3))
        self.canvas.create_oval(x - size/4, y - size/4, x + size/4, y + size/4, fill=color, outline=color)

    def _draw_quarantine(self, x, y, size, color):
        """Dibuja el glifo '⍇' (quarantine)"""
        # Símbolo de cuarentena
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=2)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill="#FF0000", width=3)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill="#FF0000", width=3)

    def _draw_whitelist(self, x, y, size, color):
        """Dibuja el glifo '⍈' (whitelist)"""
        # Lista con checkmarks
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        for i in range(3):
            y_pos = y - size/2 + i * size/2
            self.canvas.create_line(x - size/2, y_pos, x + size/2, y_pos, fill=color, width=1)
            self.canvas.create_line(x - 3*size/4, y_pos - size/8, x - size/2, y_pos, fill="#00FF00", width=2)
            self.canvas.create_line(x - size/2, y_pos, x - size/4, y_pos - size/4, fill="#00FF00", width=2)

    def _draw_blacklist(self, x, y, size, color):
        """Dibuja el glifo '⍉' (blacklist)"""
        # Lista con X marks
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        for i in range(3):
            y_pos = y - size/2 + i * size/2
            self.canvas.create_line(x - size/2, y_pos, x + size/2, y_pos, fill=color, width=1)
            # X mark
            self.canvas.create_line(x - 3*size/4, y_pos - size/8, x - size/4, y_pos + size/8, fill="#FF0000", width=2)
            self.canvas.create_line(x - 3*size/4, y_pos + size/8, x - size/4, y_pos - size/8, fill="#FF0000", width=2)

    def _draw_exploit(self, x, y, size, color):
        """Dibuja el glifo '⍊' (exploit)"""
        # Grieta o brecha
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        # Línea de grieta zigzag
        points = [x - size, y - size, x - size/2, y - size/2, x, y - size, 
                 x + size/2, y - size/2, x + size, y + size]
        self.canvas.create_line(points, fill="#FF4400", width=3)

    def _draw_vulnerability(self, x, y, size, color):
        """Dibuja el glifo '⍋' (vulnerability)"""
        # Escudo roto
        self.canvas.create_polygon(x, y - size, x - size, y, x - size/2, y + size, 
                                 x + size/2, y + size, x + size, y, outline=color, fill="")
        self.canvas.create_line(x - size/2, y - size/2, x + size/2, y + size/2, fill="#FF0000", width=3)

    def _draw_patch(self, x, y, size, color):
        """Dibuja el glifo '⍌' (patch)"""
        # Parche sobre grieta
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        # Grieta
        self.canvas.create_line(x - size, y, x + size, y, fill="#FF0000", width=2)
        # Parche
        self.canvas.create_rectangle(x - size/2, y - size/4, x + size/2, y + size/4, 
                                   fill="#00FF00", outline="#00FF00")

    def _draw_update(self, x, y, size, color):
        """Dibuja el glifo '⍍' (update)"""
        # Flecha circular (actualización)
        self.canvas.create_arc(x - size, y - size, x + size, y + size, start=45, extent=270, 
                             style=tk.ARC, outline=color, width=2)
        # Punta de flecha
        self.canvas.create_polygon(x + size/2, y - size, x + size, y - size/2, 
                                 x + 3*size/4, y - 3*size/4, outline=color, fill=color)

    def _draw_backup(self, x, y, size, color):
        """Dibuja el glifo '⍎' (backup)"""
        # Dos rectángulos superpuestos
        self.canvas.create_rectangle(x - size, y - size, x + size/2, y + size/2, outline=color, width=1)
        self.canvas.create_rectangle(x - size/2, y - size/2, x + size, y + size, outline=color, width=2)

    def _draw_restore(self, x, y, size, color):
        """Dibuja el glifo '⍏' (restore)"""
        # Flecha curvada hacia atrás
        self.canvas.create_arc(x - size, y - size, x + size, y + size, start=135, extent=270, 
                             style=tk.ARC, outline=color, width=2)
        # Punta de flecha
        self.canvas.create_polygon(x - size/2, y - size, x - size, y - size/2, 
                                 x - 3*size/4, y - 3*size/4, outline=color, fill=color)

    def _draw_mirror(self, x, y, size, color):
        """Dibuja el glifo '⍑' (mirror)"""
        # Dos formas idénticas reflejadas
        self.canvas.create_rectangle(x - size, y - size, x, y + size, outline=color, width=1)
        self.canvas.create_rectangle(x, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=2)

    def _draw_clone(self, x, y, size, color):
        """Dibuja el glifo '⍒' (clone)"""
        # Múltiples copias superpuestas
        for i in range(3):
            offset = i * size / 4
            self.canvas.create_oval(x - size + offset, y - size + offset, 
                                  x + size/2 + offset, y + size/2 + offset, 
                                  outline=color, width=1)

    def _draw_sync(self, x, y, size, color):
        """Dibuja el glifo '⍓' (sync)"""
        # Dos flechas circulares
        self.canvas.create_arc(x - size, y - size/2, x, y + size/2, start=0, extent=180, 
                             style=tk.ARC, outline=color, width=2)
        self.canvas.create_arc(x, y - size/2, x + size, y + size/2, start=180, extent=180, 
                             style=tk.ARC, outline=color, width=2)
        # Puntas de flecha
        self.canvas.create_polygon(x - size/2, y - size/2, x - 3*size/4, y - size/4, 
                                 x - 3*size/4, y - 3*size/4, outline=color, fill=color)
        self.canvas.create_polygon(x + size/2, y + size/2, x + 3*size/4, y + size/4, 
                                 x + 3*size/4, y + 3*size/4, outline=color, fill=color)


if __name__ == "__main__":
    app = SynthexTerminalEnhanced()
    app.mainloop()
