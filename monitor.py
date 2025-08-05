import tkinter as tk
import psutil
import random
import math
from datetime import datetime

# --- Configuración del lenguaje Synthex ---
# El "diccionario" de Synthex mapea palabras clave a glifos abstractos.
SYNTHEX_DICTIONARY = {
    "hello": "░", "world": "Ω", "message": "▒", "ai": "▓", "network": "⊕",
    "encrypt": "Ψ", "decrypt": "Φ", "chaos": "§", "stable": "Δ", "link": "↔",
    "system": "Σ", "breach": "⍟", "code": "⎚", "data": "⍬", "error": "⊘",
    "memory": "⌂", "identity": "∞", "ghost": "⊚", "protocol": "⍱", "firewall": "◫",
    "trace": "⍒", "jack_in": "⍐", "construct": "⍦", "entity": "⍰", "sentience": "⍲",
    "anomaly": "⌖", "data_stream": "⍨", "probe": "⍴", "divert": "⍬⍬", "corrupt": "⍟§",
    "nullify": "ΨΦ", "access": "⎇", "security": "⌠", "core": "◉", "digital": "⎚⎚",
    "reality": "∞∞", "interface": "⌤", "threat": "⍞", "man": "⌘"
}

# Mapeo de glifos a formas para el visualizador
GLYPH_SHAPES = {
    "░": "square_block", "Ω": "omega", "▒": "dotted_block", "▓": "solid_block",
    "⊕": "circle_plus", "Ψ": "psi", "Φ": "phi", "§": "section",
    "Δ": "triangle", "↔": "left_right_arrow", "Σ": "sigma", "⍟": "star",
    "⎚": "rectangle", "⍬": "double_tilde", "⊘": "circle_slash", "⌂": "house",
    "∞": "infinity", "⊚": "circle_dot", "⍱": "protocol", "◫": "firewall",
    "⍒": "down_arrow", "⍐": "up_arrow", "⍦": "construct", "⍰": "question_box",
    "⍲": "sentience", "⌖": "anomaly", "⍨": "data_stream", "⍴": "probe",
    "⍬⍬": "divert", "⍟§": "corrupt", "ΨΦ": "nullify", "⎇": "access",
    "⌠": "security", "◉": "core", "⎚⎚": "digital", "∞∞": "reality",
    "⌤": "interface", "⍞": "threat", "⌘": "man"
}

# --- Configuración de la UI ---
BG_COLOR = "#000000"
TEXT_COLOR = "#00FF00"
ACCENT_COLOR = "#FF0000"
FONT = ("Courier", 12)
TITLE_FONT = ("Courier", 18, "bold")
MONITOR_FONT = ("Courier", 10)
BUTTON_FONT = ("Courier", 12, "bold")
BUTTON_STYLE = {
    "background": BG_COLOR,
    "foreground": TEXT_COLOR,
    "activebackground": TEXT_COLOR,
    "activeforeground": BG_COLOR,
    "font": BUTTON_FONT,
    "borderwidth": 2,
    "relief": "groove",
    "highlightbackground": TEXT_COLOR,
    "highlightcolor": TEXT_COLOR
}

class SynthexTerminal(tk.Tk):
    """
    Clase principal de la aplicación, unifica el visualizador Synthex
    con un panel de monitoreo de sistema en una sola interfaz.
    """
    def __init__(self):
        super().__init__()
        self.title("Synthex Terminal: Monitor de Sistema")
        self.geometry("1000x800")
        self.configure(bg=BG_COLOR)

        self.last_net_stats = psutil.net_io_counters()
        self.glyph_stream = []
        self.max_glyphs = 100
        self.breach_active = False

        # Panel principal con dos secciones (visualizador y monitor)
        self.main_panel = tk.Frame(self, bg=BG_COLOR)
        self.main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame del visualizador de glifos
        self.visualizer_frame = tk.Frame(self.main_panel, bg=BG_COLOR, relief="groove", borderwidth=2)
        self.visualizer_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.canvas = tk.Canvas(self.visualizer_frame, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame del monitor de datos
        self.monitor_frame = tk.Frame(self.main_panel, bg=BG_COLOR, relief="groove", borderwidth=2)
        self.monitor_frame.pack(fill=tk.X, pady=(10, 0))
        self.monitor_title = tk.Label(self.monitor_frame, text="< ANÁLISIS DE DATOS DEL SISTEMA >", bg=BG_COLOR, fg=TEXT_COLOR, font=TITLE_FONT)
        self.monitor_title.pack(pady=5)
        self.data_monitor = tk.Text(self.monitor_frame, bg=BG_COLOR, fg=TEXT_COLOR, font=MONITOR_FONT, height=10, state="disabled", insertbackground=TEXT_COLOR, borderwidth=0)
        self.data_monitor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botón de acción en la parte inferior
        self.breach_button = tk.Button(self, text="[ PROTOCOLO DE INTRUSIÓN ]", command=self.trigger_breach, **BUTTON_STYLE)
        self.breach_button.pack(pady=10)

        self.animate_canvas()
        self.update_system_data()

    def update_system_data(self):
        """
        Obtiene datos del sistema y actualiza el visualizador de glifos y el panel de datos.
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        net_stats = psutil.net_io_counters()
        net_sent = net_stats.bytes_sent - self.last_net_stats.bytes_sent
        net_recv = net_stats.bytes_recv - self.last_net_stats.bytes_recv
        self.last_net_stats = net_stats
        
        mem_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        # --- Generación de Glifos ---
        new_glyphs = []
        if self.breach_active:
            new_glyphs.extend(random.choices(["⍟", "§", "⊘", "⍞"], k=3))
        elif cpu_percent > 70:
            new_glyphs.append("§")  # Caos: alto uso de CPU
        elif cpu_percent > 40:
            new_glyphs.append("▓")  # AI: Procesamiento intenso
        else:
            new_glyphs.append("Δ")  # Estable: CPU normal

        if net_sent > 500000 or net_recv > 500000:
            new_glyphs.append("⍟")
        elif net_sent > 0 or net_recv > 0:
            new_glyphs.append("⍨")

        self.glyph_stream.extend(new_glyphs)
        if len(self.glyph_stream) > self.max_glyphs:
            self.glyph_stream = self.glyph_stream[-self.max_glyphs:]

        # --- Actualización del panel de texto ---
        status_text = f"  [ESTADO]        : {'▓' if self.breach_active else 'Δ'} CORE OPERATIVO\n"
        status_text += f"  [PROCESADOR]    : {cpu_percent}% DE CAPACIDAD\n"
        status_text += f"  [MEMORIA RAM]   : {mem_info.percent}% ({mem_info.used / (1024**3):.2f}/{mem_info.total / (1024**3):.2f} GB)\n"
        status_text += f"  [ALMACENAMIENTO]: {disk_info.percent}% ({disk_info.used / (1024**3):.2f}/{disk_info.total / (1024**3):.2f} GB)\n"
        status_text += f"  [TRÁFICO RED]   : ↓ {net_recv / 1024:.2f} KB/s  ↑ {net_sent / 1024:.2f} KB/s\n"
        
        if self.breach_active:
            status_text += "\n< !!! ADVERTENCIA DE BRECHA DE SEGURIDAD DETECTADA !!! >"
        
        self.data_monitor.config(state="normal")
        self.data_monitor.delete("1.0", tk.END)
        self.data_monitor.insert(tk.END, status_text)
        self.data_monitor.config(state="disabled")

        self.after(1000, self.update_system_data)

    def trigger_breach(self):
        """Simula una brecha de seguridad con un cambio en el monitor."""
        if not self.breach_active:
            self.breach_active = True
            self.breach_button.config(state="disabled", text="[ INTRUSIÓN EN PROGRESO... ]", foreground=ACCENT_COLOR)
            self.after(10000, self.end_breach)
    
    def end_breach(self):
        """Finaliza la simulación de brecha de seguridad."""
        self.breach_active = False
        self.breach_button.config(state="normal", text="[ PROTOCOLO DE INTRUSIÓN ]", foreground=TEXT_COLOR)

    def animate_canvas(self):
        """
        Dibuja los glifos como un flujo de datos en el canvas.
        """
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10 or canvas_height < 10:
            self.after(50, self.animate_canvas)
            return

        glyph_size = 15
        spacing = 30
        x_pos = 20
        y_pos = canvas_height - 20
        
        for glyph in reversed(self.glyph_stream):
            color = ACCENT_COLOR if self.breach_active else TEXT_COLOR
            self.draw_glyph_shape(glyph, x_pos, y_pos, glyph_size, color)
            y_pos -= spacing
            if y_pos < 20:
                y_pos = canvas_height - 20
                x_pos += spacing
                if x_pos > canvas_width - 20:
                    x_pos = 20

        # Efecto de parpadeo sutil
        for item in self.canvas.find_all():
            if random.random() > 0.9:
                self.canvas.itemconfig(item, fill=ACCENT_COLOR if self.breach_active else TEXT_COLOR)
            else:
                self.canvas.itemconfig(item, fill=TEXT_COLOR)
        
        self.after(100, self.animate_canvas)

    # --- Funciones de dibujo de glifos ---
    def _draw_square_block(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
    
    def _draw_omega(self, x, y, size, color):
        points = [x - size, y + size, x - size / 2, y - size, x + size / 2, y - size, x + size, y + size]
        self.canvas.create_line(points, fill=color, width=1)
        self.canvas.create_arc(x - size, y - size / 2, x + size, y + size / 2, start=180, extent=180, outline=color, style=tk.ARC, width=1)
    
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
        self.canvas.create_line(x, y, x, y + size, fill=color, width=1)
        self.canvas.create_line(x, y, x, y - size, fill=color, width=1)
    
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
            angle = math.pi / 2 + i * (2 * math.pi / 5)
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
        self.canvas.create_oval(x - size, y - size / 2, x, y + size / 2, outline=color, width=1)
        self.canvas.create_oval(x, y - size / 2, x + size, y + size / 2, outline=color, width=1)
    
    def _draw_circle_dot(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
    
    def _draw_protocol(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
    
    def _draw_firewall(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y - size, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y - size, fill=color, width=1)
    
    def _draw_down_arrow(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y + size / 2, x, y + size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y + size / 2, x, y + size, fill=color, width=1)
    
    def _draw_up_arrow(self, x, y, size, color):
        self.canvas.create_line(x, y + size, x, y - size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y - size / 2, x, y - size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y - size / 2, x, y - size, fill=color, width=1)
    
    def _draw_construct(self, x, y, size, color):
        self.canvas.create_oval(x - size / 2, y - size, x + size / 2, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_question_box(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color)
        self.canvas.create_arc(x - size / 2, y - size, x + size / 2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y, x, y + size / 2, fill=color, width=1)
    
    def _draw_sentience(self, x, y, size, color):
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y + size, x, y - size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y + size, x, y - size, fill=color, width=1)
    
    def _draw_anomaly(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y - size, x + size / 2, y + size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y - size, x - size / 2, y + size, fill=color, width=1)
    
    def _draw_data_stream(self, x, y, size, color):
        self.canvas.create_oval(x - size, y - size / 2, x, y + size / 2, outline=color)
        self.canvas.create_oval(x, y - size / 2, x + size, y + size / 2, outline=color)
        self.canvas.create_line(x, y - size / 2, x, y + size / 2, fill=color)
    
    def _draw_probe(self, x, y, size, color):
        self.canvas.create_line(x, y - size, x, y + size, fill=color)
        self.canvas.create_oval(x - size, y, x, y + size, outline=color)
    
    def _draw_divert(self, x, y, size, color):
        self.canvas.create_arc(x - size, y - size, x + size / 2, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size / 2, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)
    
    def _draw_corrupt(self, x, y, size, color):
        self._draw_star(x - size / 2, y, size / 2, color)
        self.canvas.create_arc(x + size / 2, y - size / 2, x + size, y + size / 2, start=0, extent=180, style=tk.ARC, outline=color, width=1)
    
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
        self.canvas.create_rectangle(x - size, y - size, x + size / 2, y + size, outline=color, width=1)
        self.canvas.create_rectangle(x - size / 2, y - size, x + size, y + size, outline=color, width=1)
    
    def _draw_reality(self, x, y, size, color):
        self._draw_infinity(x - size / 2, y, size, color)
        self._draw_infinity(x + size / 2, y, size, color)
    
    def _draw_interface(self, x, y, size, color):
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x + size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_threat(self, x, y, size, color):
        self.canvas.create_polygon(x, y - size, x - size / 2, y + size / 2, x + size / 2, y + size / 2, outline=color, fill="")
        self.canvas.create_line(x - size / 2, y + size, x + size / 2, y + size, fill=color, width=1)
    
    def _draw_man(self, x, y, size, color):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_arc(x - size, y - size, x, y, start=90, extent=90, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x, y - size, x + size, y, start=0, extent=90, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size, y, x, y + size, start=180, extent=90, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x, y, x + size, y + size, start=270, extent=90, style=tk.ARC, outline=color, width=1)

    def draw_glyph_shape(self, glyph, x, y, size, color):
        """Llama a la función de dibujo correspondiente para un glifo."""
        shape_name = GLYPH_SHAPES.get(glyph, "unknown")
        
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
        else:
            self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color)
            self.canvas.create_text(x, y, text="?", fill=color, font=("Courier", 18, "bold"))

if __name__ == "__main__":
    app = SynthexTerminal()
    app.mainloop()
