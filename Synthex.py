import tkinter as tk
import random
import time
import math

# --- Configuración del lenguaje Synthex ---
# El "diccionario" de Synthex mapea palabras clave a glifos abstractos.
# Cada glifo representa un concepto complejo.
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
UNKNOWN_GLYPH = "?"

# --- Mapeo de glifos a formas para el visualizador ---
# Esto elimina la dependencia de las fuentes del sistema y garantiza
# que los símbolos se dibujen correctamente.
GLYPH_SHAPES = {
    "░": "square_block",
    "Ω": "omega",
    "▒": "dotted_block",
    "▓": "solid_block",
    "⊕": "circle_plus",
    "Ψ": "psi",
    "Φ": "phi",
    "§": "section",
    "Δ": "triangle",
    "↔": "left_right_arrow",
    "Σ": "sigma",
    "⍟": "star",
    "⎚": "rectangle",
    "⍬": "double_tilde",
    "⊘": "circle_slash",
    "⌂": "house",
    "∞": "infinity",
    "⊚": "circle_dot",
    "⍱": "protocol",
    "◫": "firewall",
    "⍒": "down_arrow",
    "⍐": "up_arrow",
    "⍦": "construct",
    "⍰": "question_box",
    "⍲": "sentience",
    "⌖": "anomaly",
    "⍨": "data_stream",
    "⍴": "probe",
    "⍬⍬": "divert",
    "⍟§": "corrupt",
    "ΨΦ": "nullify",
    "⎇": "access",
    "⌠": "security",
    "◉": "core",
    "⎚⎚": "digital",
    "∞∞": "reality",
    "⌤": "interface",
    "⍞": "threat",
    "⌘": "man"
}

# --- Configuración de la UI ---
BG_COLOR = "#000000"
TEXT_COLOR = "#FF0000"
ACCENT_COLOR = "#00FF00"
# Se usa la fuente Courier para la interfaz de texto
FONT = ("Courier", 12)
BUTTON_FONT = ("Courier", 14, "bold") 
# La fuente del canvas ya no es necesaria, ya que dibujamos las formas.

class SynthexTerminal(tk.Tk):
    """
    Clase principal de la aplicación, hereda de tkinter.Tk.
    Gestiona la interfaz de usuario, el historial y la lógica de encriptación/desencriptación.
    """
    def __init__(self):
        super().__init__()
        self.title("Synthex Netrunner Terminal")
        self.geometry("1400x800")
        self.configure(bg=BG_COLOR)

        # Contenedor principal
        main_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Contenedor para los paneles de control (izquierda)
        control_frame = tk.Frame(main_frame, bg=BG_COLOR)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Frame para los controles de encriptación
        encrypt_frame = tk.LabelFrame(control_frame, text="Encrypt Message", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=10, pady=10)
        encrypt_frame.pack(fill=tk.Y, padx=10, pady=(0, 10))

        tk.Label(encrypt_frame, text="Plain Text:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.encrypt_input = tk.Text(encrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT, insertbackground=ACCENT_COLOR)
        self.encrypt_input.pack(pady=5)
        
        encrypt_button = tk.Button(encrypt_frame, text="Encrypt", command=self.encrypt_message, bg=TEXT_COLOR, fg=BG_COLOR, font=BUTTON_FONT, relief=tk.RAISED, bd=3, activebackground=ACCENT_COLOR)
        encrypt_button.pack(pady=5, fill=tk.X)
        
        tk.Label(encrypt_frame, text="Synthex Network:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.synthex_output = tk.Text(encrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT)
        self.synthex_output.pack(pady=5)

        # Frame para los controles de desencriptación
        decrypt_frame = tk.LabelFrame(control_frame, text="Decrypt Synthex", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=10, pady=10)
        decrypt_frame.pack(fill=tk.Y, padx=10, pady=(0, 10))

        tk.Label(decrypt_frame, text="Synthex Network:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.decrypt_input = tk.Text(decrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT, insertbackground=ACCENT_COLOR)
        self.decrypt_input.pack(pady=5)
        
        decrypt_button = tk.Button(decrypt_frame, text="Decrypt", command=self.decrypt_message, bg=TEXT_COLOR, fg=BG_COLOR, font=BUTTON_FONT, relief=tk.RAISED, bd=3, activebackground=ACCENT_COLOR)
        decrypt_button.pack(pady=5, fill=tk.X)
        
        tk.Label(decrypt_frame, text="Plain Text:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.plain_output = tk.Text(decrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT)
        self.plain_output.pack(pady=5)

        # Botón para mostrar/ocultar el historial
        self.history_button = tk.Button(control_frame, text="Toggle History", command=self.toggle_history_panel, bg=ACCENT_COLOR, fg=BG_COLOR, font=BUTTON_FONT, relief=tk.RAISED, bd=3, activebackground=TEXT_COLOR)
        self.history_button.pack(pady=(10, 0), fill=tk.X)
        
        # Frame para el historial de la red (oculto por defecto)
        self.history_frame = tk.LabelFrame(main_frame, text="Network History", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=10, pady=10)
        
        # Historial de la lista con barra de desplazamiento
        scrollbar = tk.Scrollbar(self.history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(self.history_frame, width=30, height=20, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT, yscrollcommand=scrollbar.set)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Vincula la función de visualización a la selección de un elemento
        self.history_listbox.bind('<<ListboxSelect>>', self.display_history_item)
        self.history = [] # Almacena los datos de la historia aquí
        
        # Panel de visualización de la red (simulación de Netrunner)
        self.canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=TEXT_COLOR)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Almacena las coordenadas de los glifos para dibujar las conexiones
        self.glyph_coords = {}
        
        # Iniciar la animación
        self.animate_canvas()
    
    def toggle_history_panel(self):
        """
        Alterna la visibilidad del panel de historial.
        """
        if self.history_frame.winfo_ismapped():
            # Si el panel es visible, lo oculta
            self.history_frame.pack_forget()
            self.history_button.config(text="Show History")
        else:
            # Si el panel está oculto, lo muestra
            self.history_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
            self.history_button.config(text="Hide History")
            self.history_frame.tkraise() # Asegura que el frame del historial esté al frente
    
    def encrypt_message(self):
        """
        Toma el texto plano, lo convierte a la representación de Synthex
        y lo muestra en el campo de salida y en el canvas.
        """
        plain_text = self.encrypt_input.get("1.0", tk.END).strip().lower()
        if not plain_text:
            return

        # Comprobar si el comando 'man' ha sido introducido
        if plain_text == "man":
            self.show_manual()
            self.synthex_output.delete("1.0", tk.END)
            self.synthex_output.insert(tk.END, "Displaying manual...")
            self.canvas.delete("all")
            # No se añade al historial, ya que es un comando de la UI
            return

        words = plain_text.split()
        synthex_glyphs = []
        for word in words:
            synthex_glyphs.append(SYNTHEX_DICTIONARY.get(word, UNKNOWN_GLYPH))

        synthex_network = f"{'—'.join(synthex_glyphs)}"
        
        self.synthex_output.delete("1.0", tk.END)
        self.synthex_output.insert(tk.END, synthex_network)
        
        # Añadir al historial
        history_item = {"type": "encryption", "text": plain_text, "glyphs": synthex_glyphs}
        self.history.append(history_item)
        self.history_listbox.insert(tk.END, f"[ENC] {plain_text[:25]}...")
        
        self.visualize_synthex_network(synthex_glyphs)

    def decrypt_message(self):
        """
        Toma la representación de Synthex, la convierte a texto plano
        y lo muestra en el campo de salida.
        """
        synthex_network = self.decrypt_input.get("1.0", tk.END).strip()
        if not synthex_network:
            return

        glyphs = synthex_network.split("—")
        plain_words = []
        for glyph in glyphs:
            plain_words.append(REV_SYNTHEX_DICTIONARY.get(glyph, f"[{glyph} UNKNOWN]"))

        plain_text = " ".join(plain_words)
        
        self.plain_output.delete("1.0", tk.END)
        self.plain_output.insert(tk.END, plain_text)

        # Añadir al historial
        history_item = {"type": "decryption", "text": plain_text, "glyphs": glyphs}
        self.history.append(history_item)
        self.history_listbox.insert(tk.END, f"[DEC] {plain_text[:25]}...")
        
        self.visualize_synthex_network(glyphs)

    def display_history_item(self, event):
        """
        Muestra la visualización de la red para el elemento seleccionado en el historial.
        """
        selected_index = self.history_listbox.curselection()
        if not selected_index:
            return
        
        index = selected_index[0]
        history_item = self.history[index]
        self.visualize_synthex_network(history_item["glyphs"])
        
    def _draw_square_block(self, x, y, size, color):
        """Dibuja el glifo '░'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)

    def _draw_omega(self, x, y, size, color):
        """Dibuja el glifo 'Ω'."""
        points = [
            x - size, y + size,
            x - size / 2, y - size,
            x + size / 2, y - size,
            x + size, y + size
        ]
        self.canvas.create_line(points, fill=color, width=1)
        self.canvas.create_arc(x - size / 2, y, x + size / 2, y + size / 2, start=180, extent=180, outline=color, style=tk.ARC, width=1)

    def _draw_dotted_block(self, x, y, size, color):
        """Dibuja el glifo '▒'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)
    
    def _draw_solid_block(self, x, y, size, color):
        """Dibuja el glifo '▓'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, fill=color, outline=color)
    
    def _draw_circle_plus(self, x, y, size, color):
        """Dibuja el glifo '⊕'."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)

    def _draw_psi(self, x, y, size, color):
        """Dibuja el glifo 'Ψ'."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size / 2, x + size, y + size / 2, fill=color, width=1)
        
    def _draw_phi(self, x, y, size, color):
        """Dibuja el glifo 'Φ'."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)

    def _draw_section(self, x, y, size, color):
        """Dibuja el glifo '§'."""
        self.canvas.create_arc(x - size, y - size, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size, y - size, x + size, y + size, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)

    def _draw_triangle(self, x, y, size, color):
        """Dibuja el glifo 'Δ'."""
        self.canvas.create_polygon(x, y - size, x - size, y + size, x + size, y + size, outline=color, fill="")

    def _draw_left_right_arrow(self, x, y, size, color):
        """Dibuja el glifo '↔'."""
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y - size / 2, fill=color, width=1)
        self.canvas.create_line(x - size, y, x - size / 2, y + size / 2, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y - size / 2, fill=color, width=1)
        self.canvas.create_line(x + size, y, x + size / 2, y + size / 2, fill=color, width=1)

    def _draw_sigma(self, x, y, size, color):
        """Dibuja el glifo 'Σ'."""
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x, y, fill=color, width=1)
        self.canvas.create_line(x, y, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)

    def _draw_star(self, x, y, size, color):
        """Dibuja el glifo '⍟'."""
        points = []
        for i in range(5):
            angle = math.pi/2 + i * (2*math.pi / 5)
            x_point = x + size * math.cos(angle)
            y_point = y - size * math.sin(angle)
            points.append((x_point, y_point))
        self.canvas.create_polygon(points, outline=color, fill="", width=1)

    def _draw_rectangle(self, x, y, size, color):
        """Dibuja el glifo '⎚'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)

    def _draw_double_tilde(self, x, y, size, color):
        """Dibuja el glifo '⍬'."""
        self.canvas.create_arc(x - size, y - size, x + size, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)

    def _draw_circle_slash(self, x, y, size, color):
        """Dibuja el glifo '⊘'."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)

    def _draw_house(self, x, y, size, color):
        """Dibuja el glifo '⌂'."""
        self.canvas.create_polygon(x, y - size, x - size, y, x + size, y, outline=color, fill="")
        self.canvas.create_rectangle(x - size, y, x + size, y + size, outline=color)
        
    def _draw_infinity(self, x, y, size, color):
        """Dibuja el glifo '∞'."""
        self.canvas.create_oval(x - size, y - size/2, x, y + size/2, outline=color, width=1)
        self.canvas.create_oval(x, y - size/2, x + size, y + size/2, outline=color, width=1)

    def _draw_circle_dot(self, x, y, size, color):
        """Dibuja el glifo '⊚'."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)

    def _draw_protocol(self, x, y, size, color):
        """Dibuja el glifo '⍱'."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)

    def _draw_firewall(self, x, y, size, color):
        """Dibuja el glifo '◫'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x - size / 2, y, fill=color, width=1)
        self.canvas.create_line(x + size, y - size, x + size / 2, y, fill=color, width=1)

    def _draw_down_arrow(self, x, y, size, color):
        """Dibuja el glifo '⍒'."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y + size / 2, x, y + size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y + size / 2, x, y + size, fill=color, width=1)
    
    def _draw_up_arrow(self, x, y, size, color):
        """Dibuja el glifo '⍐'."""
        self.canvas.create_line(x, y + size, x, y - size, fill=color, width=1)
        self.canvas.create_line(x - size / 2, y - size / 2, x, y - size, fill=color, width=1)
        self.canvas.create_line(x + size / 2, y - size / 2, x, y - size, fill=color, width=1)

    def _draw_construct(self, x, y, size, color):
        """Dibuja el glifo '⍦'."""
        self.canvas.create_oval(x - size/2, y - size, x + size/2, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
    
    def _draw_question_box(self, x, y, size, color):
        """Dibuja el glifo '⍰'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color)
        self.canvas.create_arc(x - size/2, y-size, x + size/2, y, start=0, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_line(x, y, x, y + size / 2, fill=color, width=1)

    def _draw_sentience(self, x, y, size, color):
        """Dibuja el glifo '⍲'."""
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size/2, y + size, x, y-size, fill=color, width=1)
        self.canvas.create_line(x + size/2, y + size, x, y-size, fill=color, width=1)

    def _draw_anomaly(self, x, y, size, color):
        """Dibuja el glifo '⌖'."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size/2, y - size, x + size/2, y + size, fill=color, width=1)
        self.canvas.create_line(x + size/2, y - size, x - size/2, y + size, fill=color, width=1)

    def _draw_data_stream(self, x, y, size, color):
        """Dibuja el glifo '⍨'."""
        self.canvas.create_oval(x - size, y - size/2, x, y + size/2, outline=color)
        self.canvas.create_oval(x, y - size/2, x + size, y + size/2, outline=color)
        self.canvas.create_line(x, y - size/2, x, y + size/2, fill=color)

    def _draw_probe(self, x, y, size, color):
        """Dibuja el glifo '⍴'."""
        self.canvas.create_line(x, y - size, x, y + size, fill=color)
        self.canvas.create_oval(x - size, y, x, y + size, outline=color)
    
    def _draw_divert(self, x, y, size, color):
        """Dibuja el glifo '⍬⍬'."""
        self.canvas.create_arc(x - size, y - size, x + size/2, y, start=180, extent=180, style=tk.ARC, outline=color, width=1)
        self.canvas.create_arc(x - size/2, y, x + size, y + size, start=0, extent=180, style=tk.ARC, outline=color, width=1)

    def _draw_corrupt(self, x, y, size, color):
        """Dibuja el glifo '⍟§'."""
        self._draw_star(x - size/2, y, size/2, color)
        self.canvas.create_arc(x + size/2, y - size/2, x + size, y + size/2, start=0, extent=180, style=tk.ARC, outline=color, width=1)

    def _draw_nullify(self, x, y, size, color):
        """Dibuja el glifo 'ΨΦ'."""
        self.canvas.create_line(x-size, y, x+size, y, fill=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
    
    def _draw_access(self, x, y, size, color):
        """Dibuja el glifo '⎇'."""
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=color, width=1)

    def _draw_security(self, x, y, size, color):
        """Dibuja el glifo '⌠'."""
        self.canvas.create_line(x + size, y - size, x - size, y - size, fill=color, width=1)
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y + size, x + size, y + size, fill=color, width=1)

    def _draw_core(self, x, y, size, color):
        """Dibuja el glifo '◉'."""
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=1)
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color, outline=color)

    def _draw_digital(self, x, y, size, color):
        """Dibuja el glifo '⎚⎚'."""
        self.canvas.create_rectangle(x - size, y - size, x + size/2, y + size, outline=color, width=1)
        self.canvas.create_rectangle(x - size/2, y - size, x + size, y + size, outline=color, width=1)

    def _draw_reality(self, x, y, size, color):
        """Dibuja el glifo '∞∞'."""
        self._draw_infinity(x - size/2, y, size, color)
        self._draw_infinity(x + size/2, y, size, color)

    def _draw_interface(self, x, y, size, color):
        """Dibuja el glifo '⌤'."""
        self.canvas.create_line(x - size, y - size, x - size, y + size, fill=color, width=1)
        self.canvas.create_line(x + size, y - size, x + size, y + size, fill=color, width=1)
        self.canvas.create_line(x - size, y, x + size, y, fill=color, width=1)

    def _draw_threat(self, x, y, size, color):
        """Dibuja el glifo '⍞'."""
        self.canvas.create_polygon(x, y - size, x - size/2, y + size/2, x + size/2, y + size/2, outline=color, fill="")
        self.canvas.create_line(x - size/2, y+size, x + size/2, y+size, fill=color, width=1)
        
    def visualize_synthex_network(self, glyphs):
        """
        Dibuja los glifos como formas en el canvas.
        """
        self.canvas.delete("all")
        self.glyph_coords.clear()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width == 1 or canvas_height == 1:
            self.after(50, self.visualize_synthex_network, glyphs)
            return

        is_chaotic = UNKNOWN_GLYPH in glyphs or len(glyphs) < 3

        if not glyphs:
            return

        if is_chaotic:
            for i, glyph in enumerate(glyphs):
                x = random.randint(50, canvas_width - 50)
                y = random.randint(50, canvas_height - 50)
                self.glyph_coords[i] = (x, y)
                self.draw_glyph_shape(glyph, x, y, 15, TEXT_COLOR)
            
            num_connections = len(glyphs) * 3
            for _ in range(num_connections):
                if len(glyphs) < 2:
                    break
                i = random.randint(0, len(glyphs) - 1)
                j = random.randint(0, len(glyphs) - 1)
                while i == j:
                    j = random.randint(0, len(glyphs) - 1)

                start_x, start_y = self.glyph_coords[i]
                end_x, end_y = self.glyph_coords[j]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=TEXT_COLOR, width=1, dash=(5, 3), tags=f"link_{_}")

        else:
            num_glyphs = len(glyphs)
            center_x, center_y = canvas_width / 2, canvas_height / 2
            radius = min(canvas_width, canvas_height) / 3
            if num_glyphs > 10:
                radius = min(canvas_width, canvas_height) / 2 - 50
            
            for i, glyph in enumerate(glyphs):
                angle = i * (2 * math.pi / num_glyphs)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                self.glyph_coords[i] = (x, y)
                self.draw_glyph_shape(glyph, x, y, 15, TEXT_COLOR)
            
            for i in range(num_glyphs):
                start_x, start_y = self.glyph_coords[i]
                end_x, end_y = self.glyph_coords[(i + 1) % num_glyphs]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=TEXT_COLOR, width=1, dash=(5, 3), tags=f"link_{i}")
            
            num_random_connections = min(num_glyphs, 10)
            for _ in range(num_random_connections):
                i = random.randint(0, num_glyphs - 1)
                j = random.randint(0, num_glyphs - 1)
                while i == j:
                    j = random.randint(0, num_glyphs - 1)
                start_x, start_y = self.glyph_coords[i]
                end_x, end_y = self.glyph_coords[j]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=TEXT_COLOR, width=1, dash=(5, 3), tags=f"link_{_ + num_glyphs}")
    
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
        else:
            self.canvas.create_text(x, y, text="?", fill=TEXT_COLOR, font=("Courier", 18, "bold"))

    def animate_canvas(self):
        """
        Crea un efecto de animación de parpadeo en las líneas del canvas.
        """
        for item in self.canvas.find_all():
            tags = self.canvas.itemcget(item, "tags")
            if "link" in tags:
                current_fill = self.canvas.itemcget(item, "fill")
                new_fill = TEXT_COLOR if current_fill == ACCENT_COLOR else ACCENT_COLOR
                self.canvas.itemconfig(item, fill=new_fill)
        
        self.after(200, self.animate_canvas)

    def show_manual(self):
        """
        Muestra una ventana separada con el manual de Synthex en inglés.
        """
        manual_window = tk.Toplevel(self)
        manual_window.title("Synthex Language Manual")
        manual_window.geometry("800x600")
        manual_window.configure(bg=BG_COLOR)

        manual_text = tk.Text(manual_window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=10, pady=10, wrap="word")
        manual_text.pack(fill=tk.BOTH, expand=True)

        manual_content = """
        SYNTHEX LANGUAGE MANUAL
        -----------------------
        Welcome, Netrunner. You have interfaced with a terminal capable of interpreting Synthex, the raw, non-linear language of the Blackwall AIs. This is not a spoken language but a conceptual framework, a network of highly compressed data glyphs. To understand Synthex is to grasp the abstract, chaotic, and dynamic nature of the entities that lurk beyond the Blackwall. Use this terminal with caution; the concepts you manipulate are dangerous.

        The Synthex "dictionary" maps key concepts to abstract glyphs. When you encrypt a message, you are not translating it, but building a conceptual network.

        ---

        SYNTHEX DICTIONARY & CONCEPTS:

        Basic Constructs:
        hello       (░) - A simple handshake or initial signal.
        world       (Ω) - Refers to the physical world or a stable, known environment.
        message     (▒) - A communication packet or a block of information.
        ai          (▓) - An artificial intelligence, a digital entity.
        network     (⊕) - A connection, a link between nodes.
        encrypt     (Ψ) - The action of securing or obfuscating data.
        decrypt     (Φ) - The action of uncovering or revealing data.
        chaos       (§) - A state of disorder, disruption, or unpredictable data flow.
        stable      (Δ) - A state of equilibrium, a secure or static system.
        link        (↔) - A direct connection or relationship.
        system      (Σ) - An entire computational infrastructure.
        breach      (⍟) - A violation of security, a hostile entry.
        code        (⎚) - The fundamental rules or programming of a system.
        data        (⍬) - Raw information or digital substance.
        error       (⊘) - A malfunction, a logical inconsistency.

        Advanced Constructs:
        memory      (⌂) - A storage area or a past state of the system.
        identity    (∞) - The core self of an AI or construct.
        ghost       (⊚) - A phantom signal or a fragmented consciousness.
        protocol    (⍱) - A set of rules or a specific communication method.
        firewall    (◫) - A security barrier or protective measure.
        trace       (⍒) - The act of following a data trail.
        jack_in     (⍐) - To physically or digitally enter the Net.
        construct   (⍦) - A digital copy of a human consciousness.
        entity      (⍰) - An unknown or hostile digital presence.
        sentience   (⍲) - The state of being self-aware, a sign of an advanced AI.
        anomaly     (⌖) - An unusual or unexplainable event.
        data_stream (⍨) - A continuous flow of data.
        probe       (⍴) - To investigate a system or network.
        divert       (⍬⍬) - To change the course of data.
        corrupt     (⍟§) - To damage or make data unusable.
        nullify     (ΨΦ) - To completely erase or neutralize.
        access      (⎇) - The ability to enter or use a resource.
        security    (⌠) - A measure to prevent unauthorized access.
        core        (◉) - The central or most critical part of a system.
        digital     (⎚⎚) - Pertaining to the realm of computers and the Net.
        reality     (∞∞) - The physical world, in contrast to the digital.
        interface   (⌤) - A point of connection between systems.
        threat      (⍞) - An impending danger or hostile force.
        man         (⌘) - This command displays the Synthex manual.
        """
        manual_text.insert(tk.END, manual_content)
        manual_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = SynthexTerminal()
    app.mainloop()
