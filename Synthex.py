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

# --- Configuración de la UI ---
BG_COLOR = "#000000"
TEXT_COLOR = "#FF0000"
ACCENT_COLOR = "#00FF00"
# Se usa la fuente Courier para la interfaz y Arial Unicode MS para el visualizador
# ya que es más compatible con los glifos de Synthex en el canvas.
FONT = ("Courier", 12)
BUTTON_FONT = ("Courier", 14, "bold") 
CANVAS_FONT = ("Arial Unicode MS", 18, "bold") # Fuente para el visualizador

class SynthexTerminal(tk.Tk):
    """
    Clase principal de la aplicación, hereda de tkinter.Tk.
    Gestiona la interfaz de usuario, el historial y la lógica de encriptación/desencriptación.
    """
    def __init__(self):
        super().__init__()
        self.title("Synthex Netrunner Terminal")
        self.geometry("1400x800")  # Aumentar el tamaño para acomodar el historial
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
        
    def visualize_synthex_network(self, glyphs):
        """
        Dibuja los glifos en el canvas. La distribución de los glifos
        depende de si se encuentran caracteres inválidos.
        """
        self.canvas.delete("all")
        self.glyph_coords.clear()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Evitar errores si el canvas no se ha renderizado aún
        if canvas_width == 1 or canvas_height == 1:
            self.after(50, self.visualize_synthex_network, glyphs)
            return

        # Comprobar si hay glifos desconocidos (caracteres inválidos)
        is_chaotic = UNKNOWN_GLYPH in glyphs

        if not glyphs:
            return

        # Si el número de glifos es menor a 3, se usa un layout aleatorio para evitar errores de polígono.
        if len(glyphs) < 3 or is_chaotic:
            # Layout caótico o para mensajes cortos
            for i, glyph in enumerate(glyphs):
                x = random.randint(50, canvas_width - 50)
                y = random.randint(50, canvas_height - 50)
                self.glyph_coords[i] = (x, y)
                self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, outline=TEXT_COLOR, width=1, tags=f"glyph_{i}")
                # Usamos una fuente compatible con Unicode para el canvas
                self.canvas.create_text(x, y, text=glyph, fill=ACCENT_COLOR, font=CANVAS_FONT, tags=f"glyph_{i}")
            
            # Conexiones caóticas
            num_connections = len(glyphs) * 3  # Más conexiones para un efecto más caótico
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
            # Layout estructurado: Organizar glifos en una forma poligonal
            num_glyphs = len(glyphs)
            center_x, center_y = canvas_width / 2, canvas_height / 2
            # El radio del polígono se ajusta al número de glifos para evitar que se salgan de la pantalla
            radius = min(canvas_width, canvas_height) / 3
            if num_glyphs > 10:
                radius = min(canvas_width, canvas_height) / 2 - 50
            
            for i, glyph in enumerate(glyphs):
                # Calcular la posición en la circunferencia de un polígono
                angle = i * (2 * math.pi / num_glyphs)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                self.glyph_coords[i] = (x, y)
                self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, outline=TEXT_COLOR, width=1, tags=f"glyph_{i}")
                # Usamos una fuente compatible con Unicode para el canvas
                self.canvas.create_text(x, y, text=glyph, fill=ACCENT_COLOR, font=CANVAS_FONT, tags=f"glyph_{i}")
            
            # Conexiones estructuradas (formando el polígono)
            for i in range(num_glyphs):
                start_x, start_y = self.glyph_coords[i]
                end_x, end_y = self.glyph_coords[(i + 1) % num_glyphs]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=TEXT_COLOR, width=1, dash=(5, 3), tags=f"link_{i}")
            
            # Agregar algunas conexiones aleatorias para simular el tráfico de red
            num_random_connections = min(num_glyphs, 10)
            for _ in range(num_random_connections):
                i = random.randint(0, num_glyphs - 1)
                j = random.randint(0, num_glyphs - 1)
                while i == j:
                    j = random.randint(0, num_glyphs - 1)
                start_x, start_y = self.glyph_coords[i]
                end_x, end_y = self.glyph_coords[j]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill=TEXT_COLOR, width=1, dash=(5, 3), tags=f"link_{_ + num_glyphs}")

                
    def animate_canvas(self):
        """
        Crea un efecto de animación de parpadeo en las líneas del canvas.
        Los glifos ya no parpadean, solo las conexiones.
        """
        # Alternar el color de las líneas
        for item in self.canvas.find_all():
            tags = self.canvas.itemcget(item, "tags")
            if "link" in tags:
                current_fill = self.canvas.itemcget(item, "fill")
                new_fill = TEXT_COLOR if current_fill == ACCENT_COLOR else ACCENT_COLOR
                self.canvas.itemconfig(item, fill=new_fill)
        
        # Repetir la animación cada 200 milisegundos
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
        manual_text.config(state=tk.DISABLED) # Evita que el usuario edite el manual.

if __name__ == "__main__":
    app = SynthexTerminal()
    app.mainloop()
    # --- Clase SynthexTerminal ---
