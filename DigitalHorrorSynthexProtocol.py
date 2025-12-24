import tkinter as tk
from tkinter import messagebox
import random
import time
import math
import threading

# --- Configuración del juego ---

# Paleta de colores oscuros y rojos (inspirada en Blackwall)
PALETTE = {
    "bg": "#0A0000",          # Negro profundo
    "text": "#FF4136",        # Rojo sangre
    "accent": "#FF851B",      # Naranja amenazante
    "danger_text": "#FF0000", # Rojo puro para Game Over
    "healing_text": "#00FF00",# Verde brillante para curación
    "particle_red": "#B22222",# Partículas de destrucción (granate)
    "particle_green": "#32CD32"# Partículas de sanación (verde lima)
}

# Diccionario de glifos hostiles y defensivos con sus emojis
GLYPHS = {
    # 🔴 Demoniacas (dañan la cordura, dan puntos)
    "hostile": {
        "demon": "😈", "shadow": "👻", "whisper": "🗣️", "scream": "😱",
        "void": "⚫", "despair": "⚰️", "madness": "🤪", "terror": "💀",
        "nightmare": "👹", "death": "☠️", "pain": "💔", "fear": "😨",
        "soul": "💫", "flesh": "🥩", "bone": "🦴", "blood": "�",
        "skull": "💀", "ghost": "👻", "wraith": "💀", "phantom": "👻",
        "virus": "🦠", "worm": "🪱", "trojan": "🐎", "malware": "👾",
        "breach": "🔓", "corrupt": "😵‍💫", "threat": "⚠️", "anomaly": "🌀"
    },
    # 🛡️ Defensivas (restauran cordura)
    "defensive": {
        "firewall": "🛡️", "security": "🔒", "sanctuary": "🏰",
        "shield": "🛡️", "light": "💡", "hope": "✨", "healing": "❤️"
    }
}

class BlackwallGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackwall Protocol: Survival")
        # Establece un tamaño inicial, se ajustará en pantalla completa
        self.geometry("1000x800") 
        self.configure(bg=PALETTE["bg"])

        # Estado del juego
        self.is_running = False
        self.game_over = False
        self.score = 0
        self.sanity = 100 # Empieza con 100% de cordura
        self.difficulty_level = 1
        self.entity_speed = 1.0 # Velocidad base de las entidades
        self.spawn_interval = 2.0 # Intervalo inicial de aparición en segundos
        self.entities = {} # Almacena {id: {"type": "hostile", "name": "demon", "glyph": "😈", "vx": float, "vy": float}}
        self.pulsation_direction = {} # Para el efecto de pulsación de glifos

        self.setup_ui()
        self.start_menu()

    def setup_ui(self):
        """Configura la interfaz gráfica del juego."""
        # Frame principal que contendrá todo el juego
        self.main_frame = tk.Frame(self, bg=PALETTE["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas donde se dibujarán las entidades y efectos
        self.canvas = tk.Canvas(self.main_frame, bg=PALETTE["bg"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Vincula el clic izquierdo para interactuar con las entidades
        self.canvas.bind('<Button-1>', self.on_click)

        # Panel inferior para mostrar el puntaje y la cordura
        self.info_frame = tk.Frame(self.main_frame, bg=PALETTE["bg"], pady=10)
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.score_label = tk.Label(self.info_frame, text="SCORE: 0", font=("Consolas", 16, "bold"), fg=PALETTE["text"], bg=PALETTE["bg"])
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.sanity_label = tk.Label(self.info_frame, text="SANITY: 100%", font=("Consolas", 16, "bold"), fg=PALETTE["healing_text"], bg=PALETTE["bg"])
        self.sanity_label.pack(side=tk.RIGHT, padx=20)
        
        # Vinculación de teclas para reiniciar y salir
        self.bind("<Escape>", self.on_close) # Tecla ESC para salir
        self.bind("r", self.restart_game)    # Tecla R para reiniciar

    def start_menu(self):
        """Muestra la pantalla de inicio del juego."""
        # Asegura que no esté en pantalla completa para el menú inicial
        self.attributes('-fullscreen', False) 
        
        # Crea un frame para el menú y lo centra
        self.start_frame = tk.Frame(self.main_frame, bg=PALETTE["bg"])
        # Asegura que el start_frame cubra completamente el main_frame para que el clic funcione en toda la pantalla
        self.start_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1.0, relheight=1.0)

        tk.Label(self.start_frame, text="PROTOCOL BLACKWALL", font=("Consolas", 48, "bold"), fg=PALETTE["text"], bg=PALETTE["bg"]).pack(pady=20)
        tk.Label(self.start_frame, text="C L I C K   T O   S T A R T", font=("Consolas", 24), fg=PALETTE["accent"], bg=PALETTE["bg"]).pack(pady=10)
        
        # Captura el clic en cualquier parte del start_frame para iniciar el juego
        self.start_frame.bind("<Button-1>", self.start_game)
        
    def start_game(self, event=None):
        """Inicia el juego, destruyendo el menú de inicio y configurando el estado inicial."""
        if not self.is_running and not self.game_over:
            # Desvincula el clic del start_frame para evitar reinicios accidentales
            self.start_frame.unbind("<Button-1>") 
            # Destruye el frame del menú de inicio
            self.start_frame.destroy()
            
            # Activa el modo de pantalla completa para la experiencia de juego
            self.attributes('-fullscreen', True)

            # Reinicia las variables del juego
            self.is_running = True
            self.game_over = False
            self.score = 0
            self.sanity = 100
            self.difficulty_level = 1
            self.entity_speed = 1.0
            self.spawn_interval = 2.0
            self.entities.clear() # Limpia cualquier entidad residual
            self.canvas.delete("all") # Limpia el canvas
            
            # Actualiza la interfaz con los valores iniciales
            self.update_score()
            self.update_sanity()
            
            # Programa las funciones recurrentes del juego
            self.schedule_sanity_decay()
            self.schedule_entity_spawn()
            self.schedule_difficulty_increase()
            self.animate_entities()
            
            # [Audio: Iniciar música de fondo de terror digital]
            # Ejemplo: self.play_sound("background_loop.wav")

    def schedule_sanity_decay(self):
        """Programa la degradación constante de la cordura."""
        if self.is_running:
            self.sanity = max(0, self.sanity - 1) # Reduce la cordura en 1 punto
            self.update_sanity()
            if self.sanity > 0:
                # Si la cordura es mayor que 0, se programa para que se degrade de nuevo en 1 segundo
                self.after(1000, self.schedule_sanity_decay)
            else:
                # Si la cordura llega a 0, termina el juego
                self.end_game()

    def schedule_difficulty_increase(self):
        """Aumenta la dificultad del juego con el tiempo."""
        if self.is_running:
            self.difficulty_level += 1 # Incrementa el nivel de dificultad
            self.entity_speed += 0.05 # Aumenta ligeramente la velocidad de las entidades
            self.spawn_interval = max(0.3, self.spawn_interval - 0.05) # Reduce el intervalo de aparición (mínimo 0.3s)
            
            # Programa el próximo aumento de dificultad en 15 segundos
            self.after(15000, self.schedule_difficulty_increase)

    def schedule_entity_spawn(self):
        """Programa la aparición de nuevas entidades en el canvas."""
        if self.is_running:
            self.spawn_entity() # Llama a la función para crear una nueva entidad
            # Programa la próxima aparición según el intervalo actual de aparición
            self.after(int(self.spawn_interval * 1000), self.schedule_entity_spawn)

    def spawn_entity(self):
        """Crea y posiciona una nueva entidad (hostil o defensiva) en el canvas."""
        if self.is_running:
            canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
            
            # Posición aleatoria para la nueva entidad
            x = random.randint(50, canvas_width - 50)
            y = random.randint(50, canvas_height - 50)
            size = random.randint(25, 35) # Tamaño aleatorio para los glifos

            # Decide si la entidad será defensiva (30% de probabilidad) o hostil (70%)
            if random.random() > 0.7:  
                entity_type = "defensive"
                name = random.choice(list(GLYPHS["defensive"].keys()))
                glyph = GLYPHS["defensive"][name]
                color = PALETTE["healing_text"] # Glifos defensivos son verdes
                # [Audio: Sonido de aparición de entidad defensiva, ej. "beep" suave]
            else:
                entity_type = "hostile"
                name = random.choice(list(GLYPHS["hostile"].keys()))
                glyph = GLYPHS["hostile"][name]
                color = PALETTE["text"] # Glifos hostiles son rojos
                # [Audio: Sonido de aparición de entidad hostil, ej. "glitch" o "susurro"]

            # Crea el glifo como texto en el canvas
            entity_id = self.canvas.create_text(x, y, text=glyph, font=("Consolas", size, "bold"), fill=color, tags="entity")
            # Almacena los datos de la entidad, incluyendo su vector de velocidad (vx, vy)
            self.entities[entity_id] = {
                "type": entity_type, 
                "name": name, 
                "glyph": glyph, 
                "vx": random.uniform(-self.entity_speed, self.entity_speed), 
                "vy": random.uniform(-self.entity_speed, self.entity_speed)
            }
            # Inicializa la dirección de pulsación para el efecto visual
            self.pulsation_direction[entity_id] = 1 # 1 para crecer, -1 para encoger

    def animate_entities(self):
        """Mueve y anima todas las entidades en el canvas."""
        if self.is_running:
            canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()

            # Itera sobre una copia de la lista de entidades para evitar problemas si se eliminan durante el bucle
            for entity_id, entity_data in list(self.entities.items()):
                # Obtiene las coordenadas actuales de la entidad
                x, y = self.canvas.coords(entity_id)
                vx, vy = entity_data["vx"], entity_data["vy"]
                
                # Verifica los límites de la pantalla y hace rebotar a las entidades
                # Si la entidad sale de los límites horizontales, invierte su velocidad X
                if x <= 0 or x >= canvas_width:
                    vx *= -1
                # Si la entidad sale de los límites verticales, invierte su velocidad Y
                if y <= 0 or y >= canvas_height:
                    vy *= -1
                
                # Mueve la entidad en el canvas
                self.canvas.move(entity_id, vx, vy)
                # Actualiza la velocidad de la entidad en sus datos
                entity_data["vx"], entity_data["vy"] = vx, vy
                
                # Efecto de pulsación de glifos
                # Obtiene el tamaño actual de la fuente del glifo
                current_font_str = self.canvas.itemcget(entity_id, "font")
                try:
                    current_size = int(current_font_str.split()[1])
                except (IndexError, ValueError):
                    current_size = 30 # Tamaño por defecto si falla la lectura

                # Ajusta el tamaño para la pulsación
                pulsation_step = self.pulsation_direction.get(entity_id, 1) # Obtiene la dirección de pulsación
                new_size = current_size + pulsation_step
                
                # Invierte la dirección de pulsación si alcanza los límites
                if new_size >= 35 or new_size <= 25:
                    self.pulsation_direction[entity_id] *= -1
                    new_size = current_size + self.pulsation_direction[entity_id] # Aplica el cambio con la nueva dirección

                # Actualiza la fuente del glifo para el efecto de pulsación
                self.canvas.itemconfig(entity_id, font=("Consolas", new_size, "bold"))
                
                # Si una entidad hostil golpea el borde de la pantalla, la cordura se degrada
                if entity_data["type"] == "hostile":
                    # Un pequeño margen para que no sea solo en el píxel exacto
                    margin = 10 
                    if x <= margin or x >= canvas_width - margin or y <= margin or y >= canvas_height - margin:
                         self.sanity -= random.randint(1, 2) # Pequeña reducción de cordura
                         self.update_sanity()
                         # [Audio: Sonido de golpe o "corrupción" al tocar el borde]

            # Efecto de glitch de pantalla aleatorio para aumentar la tensión
            if random.random() < 0.01: # Baja probabilidad de glitch
                self.glitch_effect()

            self.after(20, self.animate_entities)

    def glitch_effect(self):
        """Crea un efecto visual de distorsión o 'glitch' en la pantalla."""
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Crea un rectángulo aleatorio con colores de la paleta de terror
        glitch_id = self.canvas.create_rectangle(
            random.randint(0, canvas_width), random.randint(0, canvas_height),
            random.randint(0, canvas_width), random.randint(0, canvas_height),
            fill=PALETTE["bg"], outline=PALETTE["danger_text"], width=random.randint(1, 5), tags="glitch"
        )
        # Asegura que las entidades (glifos) se dibujen por encima del efecto de glitch
        self.canvas.tag_raise("entity") 
        # Elimina el glitch después de un corto período de tiempo para que sea un efecto fugaz
        self.after(random.randint(50, 200), lambda: self.canvas.delete(glitch_id))
        
        # [Audio: Sonido de "glitch" o distorsión]
        # Ejemplo: self.play_sound("glitch_sound.wav")

    def on_click(self, event):
        """Maneja los clics del usuario en el canvas."""
        if self.is_running:
            # Encuentra todos los elementos que se superponen con las coordenadas del clic
            clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
            for item in clicked_items:
                # Si el elemento clicado tiene la etiqueta "entity"
                if "entity" in self.canvas.gettags(item):
                    self.handle_entity_click(item) # Procesa el clic en la entidad
                    break # Solo procesa un clic por entidad (para evitar doble interacción)

    def handle_entity_click(self, entity_id):
        """Procesa la interacción con una entidad clicada."""
        entity_data = self.entities.get(entity_id)
        if not entity_data:
            return # Si la entidad ya no existe (ej. fue eliminada por otro clic), no hacer nada

        if entity_data["type"] == "hostile":
            self.score += 10 # Gana puntos por eliminar una entidad hostil
            self.destroy_entity(entity_id, is_hostile=True) # Destruye la entidad con efecto de destrucción
            # [Audio: Sonido de éxito/destrucción, ej. "explosion" o "desintegración"]
        elif entity_data["type"] == "defensive":
            self.sanity = min(100, self.sanity + 10) # Restaura cordura al interactuar con una defensiva (máximo 100)
            self.destroy_entity(entity_id, is_hostile=False) # Destruye la entidad con efecto de sanación
            # [Audio: Sonido de curación/restauración, ej. "brillo" o "armonía"]

        self.update_score() # Actualiza la visualización del puntaje
        self.update_sanity() # Actualiza la visualización de la cordura

    def destroy_entity(self, entity_id, is_hostile):
        """Crea un efecto de partículas y elimina la entidad del canvas."""
        x, y = self.canvas.coords(entity_id) # Obtiene las coordenadas de la entidad
        
        # Determina el color de las partículas según el tipo de entidad
        if is_hostile:
            color = PALETTE["particle_red"] # Partículas rojas para hostiles
        else:
            color = PALETTE["particle_green"] # Partículas verdes para defensivas

        # Crea múltiples partículas alrededor de la posición de la entidad
        for _ in range(15): # Número de partículas
            self.create_particle(x, y, color)

        # Elimina la entidad del canvas y del diccionario de entidades
        self.canvas.delete(entity_id)
        if entity_id in self.entities:
            del self.entities[entity_id]
        if entity_id in self.pulsation_direction:
            del self.pulsation_direction[entity_id]

    def create_particle(self, x, y, color):
        """Crea y anima una pequeña partícula que se desvanece."""
        particle_id = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill=color, outline=color) # Crea un pequeño círculo
        
        # Velocidad aleatoria para la partícula
        vx = random.uniform(-3, 3)
        vy = random.uniform(-3, 3)
        
        # Función recursiva para animar la partícula
        def animate_particle(pid, count):
            if count > 0:
                self.canvas.move(pid, vx, vy) # Mueve la partícula
                # Reduce gradualmente la opacidad (simulado con color) o tamaño si fuera posible
                self.canvas.after(20, animate_particle, pid, count - 1)
            else:
                self.canvas.delete(pid) # Elimina la partícula cuando termina su animación

        animate_particle(particle_id, 30) # Anima la partícula por 30 pasos

    def update_score(self):
        """Actualiza el texto del puntaje en la interfaz."""
        self.score_label.config(text=f"SCORE: {self.score}")

    def update_sanity(self):
        """Actualiza el texto y el color de la cordura en la interfaz."""
        color = PALETTE["healing_text"] # Verde por defecto
        if self.sanity < 50:
            color = PALETTE["accent"] # Naranja si la cordura es media
        if self.sanity < 20:
            color = PALETTE["danger_text"] # Rojo si la cordura es crítica

        self.sanity_label.config(text=f"SANITY: {self.sanity}%", fg=color)

    def end_game(self):
        """Termina el juego y muestra la pantalla de Game Over."""
        self.is_running = False # Detiene el bucle principal del juego
        self.game_over = True # Marca el estado de Game Over
        self.canvas.delete("all") # Limpia todas las entidades del canvas
        self.entities.clear() # Limpia el diccionario de entidades
        self.pulsation_direction.clear() # Limpia las direcciones de pulsación
        
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Muestra el mensaje de Game Over y el puntaje final
        self.canvas.create_text(canvas_width/2, canvas_height/2 - 50, text="--- SYNC LOST ---", font=("Consolas", 40, "bold"), fill=PALETTE["danger_text"])
        self.canvas.create_text(canvas_width/2, canvas_height/2 + 20, text=f"SURVIVED: {self.score} CYCLES", font=("Consolas", 24), fill=PALETTE["text"])
        self.canvas.create_text(canvas_width/2, canvas_height/2 + 80, text="Press 'R' to REBOOT", font=("Consolas", 18), fill=PALETTE["accent"])
        
        # [Audio: Sonido de Game Over, ej. "alarma" o "estática"]

    def restart_game(self, event=None):
        """Reinicia el juego si está en estado de Game Over."""
        if self.game_over:
            self.game_over = False
            self.is_running = False
            self.canvas.delete("all") # Limpia el canvas para el nuevo juego
            self.entities.clear()
            self.pulsation_direction.clear()
            self.start_menu() # Vuelve a la pantalla de inicio

    def on_close(self, event=None):
        """Pregunta al usuario si desea salir del juego."""
        if messagebox.askyesno("Exit", "¿Estás seguro de que quieres salir?"):
            self.destroy() # Cierra la ventana del juego

# Punto de entrada principal del juego
if __name__ == "__main__":
    game = BlackwallGame()
    game.mainloop()
