import tkinter as tk
import psutil
import random
import time
import math

# --- Configuración del lenguaje Synthex ---
# El "diccionario" de Synthex mapea palabras clave a glifos abstractos.
SYNTHEX_DICTIONARY = {
    "hello": "░",
    "world": "Ω",
    "message": "▒",
    "ai": "▓",
    "network": "⊕",
    "encrypt": "Ψ",
    "decrypt": "Φ",
    "chaos": "§",
    "stable": "Δ",
    "link": "↔",
    "system": "Σ",
    "breach": "⍟",
    "code": "⎚",
    "data": "⍬",
    "error": "⊘",
    "memory": "⌂",
    "identity": "∞",
    "ghost": "⊚",
    "protocol": "⍱",
    "firewall": "◫",
    "trace": "⍒",
    "jack_in": "⍐",
    "construct": "⍦",
    "entity": "⍰",
    "sentience": "⍲",
    "anomaly": "⌖",
    "data_stream": "⍨",
    "probe": "⍴",
    "divert": "⍬⍬",
    "corrupt": "⍟§",
    "nullify": "ΨΦ",
    "access": "⎇",
    "security": "⌠",
    "core": "◉",
    "digital": "⎚⎚",
    "reality": "∞∞",
    "interface": "⌤",
    "threat": "⍞",
    "man": "⌘"
}

# Invertir el diccionario para una rápida búsqueda de desencriptación
REV_SYNTHEX_DICTIONARY = {v: k for k, v in SYNTHEX_DICTIONARY.items()}

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
TEXT_COLOR = "#00FF00"  # Verde neón para el monitor
ACCENT_COLOR = "#FF0000"  # Rojo para alertas
FONT = ("Courier", 12)
BUTTON_FONT = ("Courier", 14, "bold")

class SynthexMonitor(tk.Tk):
    """
    Clase principal de la aplicación, hereda de tkinter.Tk.
    Monitorea la actividad del sistema y la visualiza con glifos de Synthex.
    """
    def __init__(self):
        super().__init__()
        self.title("Synthex System Monitor")
        self.geometry("1000x600")
        self.configure(bg=BG_COLOR)

        # Contenedor principal
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel de visualización
        self.canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=TEXT_COLOR)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Etiqueta de estado en la parte inferior
        self.status_label = tk.Label(main_frame, text="Monitoring system activity...", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.status_label.pack(pady=5)

        self.last_net_stats = psutil.net_io_counters()
        self.glyph_stream = []
        self.max_glyphs = 50  # Máximo de glifos en pantalla

        self.animate_canvas()
        self.monitor_system()

    def monitor_system(self):
        """
        Obtiene datos del sistema y los traduce a glifos de Synthex.
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        net_stats = psutil.net_io_counters()
        net_sent = net_stats.bytes_sent - self.last_net_stats.bytes_sent
        net_recv = net_stats.bytes_recv - self.last_net_stats.bytes_recv
        self.last_net_stats = net_stats
        
        # Lógica para generar glifos basados en el estado del sistema
        new_glyphs = []
        
        # Glifos basados en el uso de CPU
        if cpu_percent > 80:
            new_glyphs.append("§")  # Caos: alto uso de CPU
            self.status_label.config(text=f"CPU overload! CPU: {cpu_percent}%", fg=ACCENT_COLOR)
        elif cpu_percent > 50:
            new_glyphs.append("▓")  # AI: Procesamiento intenso
            self.status_label.config(text=f"High CPU activity. CPU: {cpu_percent}%", fg=TEXT_COLOR)
        else:
            new_glyphs.append("Δ")  # Estable: CPU normal
            self.status_label.config(text=f"System stable. CPU: {cpu_percent}%", fg=TEXT_COLOR)

        # Glifos basados en la actividad de la red
        if net_sent > 1000000 or net_recv > 1000000: # Más de 1MB/s
            new_glyphs.append("⍟") # Breach: Gran tráfico de red
            self.status_label.config(text="Network breach detected! High data flow.", fg=ACCENT_COLOR)
        elif net_sent > 0 or net_recv > 0:
            new_glyphs.append("⍨")  # Data Stream: Tráfico normal de red
            self.status_label.config(text="Network data stream active.", fg=TEXT_COLOR)
        
        # Añade los nuevos glifos a la cola
        self.glyph_stream.extend(new_glyphs)
        
        # Mantiene la cola de glifos a un tamaño manejable
        if len(self.glyph_stream) > self.max_glyphs:
            self.glyph_stream = self.glyph_stream[-self.max_glyphs:]

        # Vuelve a llamar a esta función cada segundo
        self.after(1000, self.monitor_system)

    def animate_canvas(self):
        """
        Dibuja los glifos como un flujo de datos en el canvas.
        """
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Si el canvas aún no está renderizado, espera un momento
        if canvas_width < 10 or canvas_height < 10:
            self.after(50, self.animate_canvas)
            return

        glyph_size = 15
        spacing = 30
        x_pos = 20
        y_pos = canvas_height - 20
        
        for glyph in reversed(self.glyph_stream):
            self.draw_glyph_shape(glyph, x_pos, y_pos, glyph_size, TEXT_COLOR)
            y_pos -= spacing
            if y_pos < 20:
                y_pos = canvas_height - 20
                x_pos += spacing
                if x_pos > canvas_width - 20:
                    x_pos = 20

        # Anima los glifos con un efecto de parpadeo sutil
        for item in self.canvas.find_all():
            if random.random() > 0.9:
                self.canvas.itemconfig(item, fill=ACCENT_COLOR)
            else:
                self.canvas.itemconfig(item, fill=TEXT_COLOR)
        
        self.after(100, self.animate_canvas)

    # --- Funciones de dibujo de glifos ---
    def _draw_square_block(self, x, y, size, color):
        """Dibuja el glifo '░', un bloque cuadrado con líneas que se cruzan."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
    
    def _draw_omega(self, x, y, size, color):
        """Dibuja el glifo 'Ω', una omega elaborada."""
        points = [x - size, y + size, x - size / 2, y - size, x + size / 2, y - size, x + size, y + size]
        self.canvas.create_line(points, fill=color, width=1)
        self.canvas.create_arc(x - size, y - size / 2, x + size, y + size / 2, start=180, extent=180, outline=color, style=tk.ARC, width=1)
    
    def _draw_dotted_block(self, x, y, size, color):
        """Dibuja el glifo '▒', un bloque con un círculo central."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
    
    def _draw_solid_block(self, x, y, size, color):
        """Dibuja el glifo '▓', un bloque sólido."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=color, outline=color)
    
    def _draw_circle_plus(self, x, y, size, color):
        """Dibuja el glifo '⊕', un círculo con una cruz en el centro."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_psi(self, x, y, size, color):
        """Dibuja el glifo 'Ψ', una psi con barras horizontales."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_phi(self, x, y, size, color):
        """Dibuja el glifo 'Φ', un círculo con una línea horizontal."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_section(self, x, y, size, color):
        """Dibuja el glifo '§', un símbolo de sección doble."""
        self.canvas.create_arc(x - size, y - size, x, y, start=90, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x, y, x + size, y + size, start=270, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y, x, y + size, fill=color, width=1)
        self.canvas.create_line(x, y, x, y - size, fill=color, width=1)
    
    def _draw_triangle(self, x, y, size, color):
        """Dibuja el glifo 'Δ', un triángulo isósceles."""
        self.canvas.create_polygon(x, y - size, x - size, y + size, x + size, y + size, outline=color, fill="")
    
    def _draw_left_right_arrow(self, x, y, size, color):
        """Dibuja el glifo '↔', una flecha bidireccional."""
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y - size / 2, fill=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y + size / 2, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y - size / 2, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y + size / 2, fill=color, width=1)
    
    def _draw_sigma(self, x, y, size, color):
        """Dibuja el glifo 'Σ', una sigma elaborada."""
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1)
        self.canvas.create_line(x + size, y + size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x, y, fill=color, width=1)
        self.canvas.create_line(x, y, x - size, y + size, fill=color, width=1)
    
    def _draw_star(self, x, y, size, color):
        """Dibuja el glifo '⍟', una estrella de cinco puntas."""
        points = []
        for i in range(5):
            angle = math.pi / 2 + i * (2 * math.pi / 5)
            x_point = x + size * math.cos(angle)
            y_point = y - size * math.sin(angle)
            points.append((x_point, y_point))
        self.canvas.create_polygon(points, outline=color, fill="", width=1)
    
    def _draw_rectangle(self, x, y, size, color):
        """Dibuja el glifo '⎚', un simple rectángulo."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
    
    def _draw_double_tilde(self, x, y, size, color):
        """Dibuja el glifo '⍬', un par de arcos en forma de tilde."""
        self.canvas.create_arc(x - size, y - size, x + size, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)
    
    def _draw_circle_slash(self, x, y, size, color):
        """Dibuja el glifo '⊘', un círculo con una línea diagonal."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
    
    def _draw_house(self, x, y, size, color):
        """Dibuja el glifo '⌂', un contorno de casa con tejado."""
        self.canvas.create_polygon(x, y - size, x - size, y, x + size, y, outline=color, fill="")
        self.canvas.create_rectangle(x - size, y, x + size, y + size, outline=color)
        
    def _draw_infinity(self, x, y, size, color):
        """Dibuja el glifo '∞', un símbolo de infinito."""
        self.canvas.create_oval(x - size, y - size / 2, x, y + size / 2, outline=color, width=1)
        self.canvas.create_oval(x, y - size / 2, x + size, y + size / 2, outline=color, width=1)
    
    def _draw_circle_dot(self, x, y, size, color):
        """Dibuja el glifo '⊚', un círculo con un punto central."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
    
    def _draw_protocol(self, x, y, size, color):
        """Dibuja el glifo '⍱', un símbolo de protocolo con barras horizontales y verticales."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
    
    def _draw_firewall(self, x, y, size, color):
        """Dibuja el glifo '◫', un bloque con barreras en los lados."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y - size, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y - size, fill=color, width=1)
    
    def _draw_down_arrow(self, x, y, size, color):
        """Dibuja el glifo '⍒', una flecha hacia abajo."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y + size / 2, x, y + size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y + size / 2, x, y + size, fill=color, width=1)
    
    def _draw_up_arrow(self, x, y, size, color):
        """Dibuja el glifo '⍐', una flecha hacia arriba."""
        self.canvas.create_line(x, y + size, x, y - size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y - size / 2, x, y - size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y - size / 2, x, y - size, fill=color, width=1)
    
    def _draw_construct(self, x, y, size, color):
        """Dibuja el glifo '⍦', un símbolo de construcción."""
        self.canvas.create_oval(x - size / 2, y - size, x + size / 2, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_question_box(self, x, y, size, color):
        """Dibuja el glifo '⍰', una caja con un signo de interrogación."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color)
        self.canvas.create_arc(x - size / 2, y - size, x + size / 2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y, x, y + size / 2, fill=color, width=1)
    
    def _draw_sentience(self, x, y, size, color):
        """Dibuja el glifo '⍲', un símbolo de sentiencia en forma de pico."""
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y + size, x, y - size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y + size, x, y - size, fill=color, width=1)
    
    def _draw_anomaly(self, x, y, size, color):
        """Dibuja el glifo '⌖', un símbolo de anomalía con múltiples líneas diagonales."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y - size, x + size / 2, y + size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y - size, x - size / 2, y + size, fill=color, width=1)
    
    def _draw_data_stream(self, x, y, size, color):
        """Dibuja el glifo '⍨', un flujo de datos."""
        self.canvas.create_oval(x - size, y - size / 2, x, y + size / 2, outline=color)
        self.canvas.create_oval(x, y - size / 2, x + size, y + size / 2, outline=color)
        self.canvas.create_line(x, y - size / 2, x, y + size / 2, fill=color)
    
    def _draw_probe(self, x, y, size, color):
        """Dibuja el glifo '⍴', una sonda."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color)
        self.canvas.create_oval(x - size, y, x, y + size, outline=color)
    
    def _draw_divert(self, x, y, size, color):
        """Dibuja el glifo '⍬⍬', dos tildes dobles que simbolizan desviar."""
        self.canvas.create_arc(x - size, y - size, x + size / 2, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size / 2, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)
    
    def _draw_corrupt(self, x, y, size, color):
        """Dibuja el glifo '⍟§', una combinación de estrella y sección para representar corrupción."""
        self._draw_star(x - size / 2, y, size / 2, color)
        self.canvas.create_arc(x + size / 2, y - size / 2, x + size, y + size / 2, start=0, extent=180, style=tk.ARC, outline=color, width=1)
    
    def _draw_nullify(self, x, y, size, color):
        """Dibuja el glifo 'ΨΦ', una combinación de Psi y Phi para representar anulación."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
    
    def _draw_access(self, x, y, size, color):
        """Dibuja el glifo '⎇', un símbolo de acceso."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
    
    def _draw_security(self, x, y, size, color):
        """Dibuja el glifo '⌠', un símbolo de seguridad."""
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
    
    def _draw_core(self, x, y, size, color):
        """Dibuja el glifo '◉', un círculo central con un punto."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
    
    def _draw_digital(self, x, y, size, color):
        """Dibuja el glifo '⎚⎚', dos rectángulos que se superponen."""
        self.canvas.create_rectangle(x - size, y - size, x + size / 2, y + size, outline=color, width=1)
        self.canvas.create_rectangle(x - size / 2, y - size, x + size, y + size, outline=color, width=1)
    
    def _draw_reality(self, x, y, size, color):
        """Dibuja el glifo '∞∞', dos símbolos de infinito."""
        self._draw_infinity(x - size / 2, y, size, color)
        self._draw_infinity(x + size / 2, y, size, color)
    
    def _draw_interface(self, x, y, size, color):
        """Dibuja el glifo '⌤', un símbolo de interfaz."""
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x + size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_threat(self, x, y, size, color):
        """Dibuja el glifo '⍞', un símbolo de amenaza en forma de triángulo con una base."""
        self.canvas.create_polygon(x, y - size, x - size / 2, y + size / 2, x + size / 2, y + size / 2, outline=color, fill="")
        self.canvas.create_line(x - size / 2, y + size, x + size / 2, y + size, fill=color, width=1)
    
    def _draw_man(self, x, y, size, color):
        """Dibuja el glifo '⌘' (el símbolo de comando)."""
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
    app = SynthexMonitor()
    app.mainloop()
