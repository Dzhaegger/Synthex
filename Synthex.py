import tkinter as tk
import random
import time

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
    "error": "⊘"
}

# Invertir el diccionario para una rápida búsqueda de desencriptación
REV_SYNTHEX_DICTIONARY = {v: k for k, v in SYNTHEX_DICTIONARY.items()}
UNKNOWN_GLYPH = "?"

# --- Configuración de la UI ---
BG_COLOR = "#000000"
TEXT_COLOR = "#FF0000"
ACCENT_COLOR = "#00FF00"
FONT = ("Courier", 12)

class SynthexTerminal(tk.Tk):
    """
    Clase principal de la aplicación, hereda de tkinter.Tk.
    Gestiona la interfaz de usuario y la lógica de encriptación/desencriptación.
    """
    def __init__(self):
        super().__init__()
        self.title("Synthex Netrunner Terminal")
        self.geometry("1200x800")
        self.configure(bg=BG_COLOR)

        # Contenedor principal
        main_frame = tk.Frame(self, bg=BG_COLOR, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para los controles de encriptación
        encrypt_frame = tk.LabelFrame(main_frame, text="Encrypt Message", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=10, pady=10)
        encrypt_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(encrypt_frame, text="Plain Text:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.encrypt_input = tk.Text(encrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT, insertbackground=ACCENT_COLOR)
        self.encrypt_input.pack(pady=5)
        
        encrypt_button = tk.Button(encrypt_frame, text="Encrypt", command=self.encrypt_message, bg=TEXT_COLOR, fg=BG_COLOR, font=FONT, relief=tk.RAISED, bd=3, activebackground=ACCENT_COLOR)
        encrypt_button.pack(pady=5, fill=tk.X)
        
        tk.Label(encrypt_frame, text="Synthex Network:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.synthex_output = tk.Text(encrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT)
        self.synthex_output.pack(pady=5)

        # Frame para los controles de desencriptación
        decrypt_frame = tk.LabelFrame(main_frame, text="Decrypt Synthex", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=10, pady=10)
        decrypt_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(decrypt_frame, text="Synthex Network:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.decrypt_input = tk.Text(decrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT, insertbackground=ACCENT_COLOR)
        self.decrypt_input.pack(pady=5)
        
        decrypt_button = tk.Button(decrypt_frame, text="Decrypt", command=self.decrypt_message, bg=TEXT_COLOR, fg=BG_COLOR, font=FONT, relief=tk.RAISED, bd=3, activebackground=ACCENT_COLOR)
        decrypt_button.pack(pady=5, fill=tk.X)
        
        tk.Label(decrypt_frame, text="Plain Text:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT).pack(anchor=tk.W)
        self.plain_output = tk.Text(decrypt_frame, height=5, width=40, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT)
        self.plain_output.pack(pady=5)

        # Panel de visualización de la red (simulación de Netrunner)
        self.canvas = tk.Canvas(main_frame, bg=BG_COLOR, highlightthickness=1, highlightbackground=TEXT_COLOR)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Almacena las coordenadas de los glifos para dibujar las conexiones
        self.glyph_coords = {}
        
        # Iniciar la animación
        self.animate_canvas()
    
    def encrypt_message(self):
        """
        Toma el texto plano, lo convierte a la representación de Synthex
        y lo muestra en el campo de salida y en el canvas.
        """
        plain_text = self.encrypt_input.get("1.0", tk.END).strip().lower()
        if not plain_text:
            return

        words = plain_text.split()
        synthex_glyphs = []
        for word in words:
            # Encuentra el glifo correspondiente o usa un glifo desconocido
            synthex_glyphs.append(SYNTHEX_DICTIONARY.get(word, UNKNOWN_GLYPH))

        # La red se representa como una secuencia de glifos unidos por un "enlace"
        synthex_network = f"{'—'.join(synthex_glyphs)}"
        
        self.synthex_output.delete("1.0", tk.END)
        self.synthex_output.insert(tk.END, synthex_network)
        
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
            # Encuentra la palabra correspondiente o usa un marcador de posición
            plain_words.append(REV_SYNTHEX_DICTIONARY.get(glyph, f"[{glyph} UNKNOWN]"))

        plain_text = " ".join(plain_words)
        
        self.plain_output.delete("1.0", tk.END)
        self.plain_output.insert(tk.END, plain_text)

        self.visualize_synthex_network(glyphs)
        
    def visualize_synthex_network(self, glyphs):
        """
        Dibuja los glifos en el canvas, conectados aleatoriamente
        para simular una red no lineal.
        """
        self.canvas.delete("all")
        self.glyph_coords.clear()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Evitar errores si el canvas no se ha renderizado aún
        if canvas_width == 1 or canvas_height == 1:
            self.after(50, self.visualize_synthex_network, glyphs)
            return

        # Dibujar glifos
        for i, glyph in enumerate(glyphs):
            x = random.randint(50, canvas_width - 50)
            y = random.randint(50, canvas_height - 50)
            self.glyph_coords[i] = (x, y)
            
            # Crear un efecto de "halo" alrededor del glifo
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, outline=TEXT_COLOR, width=1, tags=f"glyph_{i}")
            
            # Dibujar el glifo en el centro
            self.canvas.create_text(x, y, text=glyph, fill=ACCENT_COLOR, font=("Courier", 18, "bold"), tags=f"glyph_{i}")

        # Dibujar las conexiones entre glifos
        if len(glyphs) > 1:
            for i in range(len(glyphs) - 1):
                start_x, start_y = self.glyph_coords[i]
                end_x, end_y = self.glyph_coords[i + 1]
                
                # Crear una conexión con un efecto de parpadeo
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=TEXT_COLOR, width=1, dash=(5, 3), tags=f"link_{i}")
                
    def animate_canvas(self):
        """
        Crea un efecto de animación de parpadeo en las líneas del canvas.
        """
        for item in self.canvas.find_all():
            tags = self.canvas.itemcget(item, "tags")
            if "link" in tags:
                # Alternar el estado de la línea
                current_fill = self.canvas.itemcget(item, "fill")
                new_fill = TEXT_COLOR if current_fill == ACCENT_COLOR else ACCENT_COLOR
                self.canvas.itemconfig(item, fill=new_fill)
                
        # Repetir la animación cada 200 milisegundos
        self.after(200, self.animate_canvas)

if __name__ == "__main__":
    app = SynthexTerminal()
    app.mainloop()
