import tkinter as tk
from PIL import Image, ImageTk
import itertools

class TamagotchiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Tamagotchi")
        
        # Canvas erstellen
        self.canvas = tk.Canvas(root, width=200, height=200, bg='white')
        self.canvas.pack()

        # Sprites laden (verschiedene Zustände)
        self.frames = {
            'idle': [ImageTk.PhotoImage(Image.open(f"frame_{i}.png").resize((100, 100))) for i in range(1, 3)],
            'happy': [ImageTk.PhotoImage(Image.open(f"happy_{i}.png").resize((100, 100))) for i in range(1, 3)],
            'eating': [ImageTk.PhotoImage(Image.open(f"eat_{i}.png").resize((100, 100))) for i in range(1, 3)],
            'sleeping': [ImageTk.PhotoImage(Image.open(f"sleep_{i}.png").resize((100, 100))) for i in range(1, 3)],
        }

        # Anfangszustand festlegen
        self.current_animation = 'idle'
        self.current_frame = itertools.cycle(self.frames[self.current_animation])
        self.sprite_id = self.canvas.create_image(100, 100, image=next(self.current_frame))

        # Animation starten
        self.animate()

        # Buttons hinzufügen
        self.feed_button = tk.Button(root, text="Füttern", command=self.feed)
        self.feed_button.pack(side="left")

        self.play_button = tk.Button(root, text="Spielen", command=self.play)
        self.play_button.pack(side="left")

        self.sleep_button = tk.Button(root, text="Schlafen", command=self.sleep)
        self.sleep_button.pack(side="left")

    def animate(self):
        try:
            # Nächstes Frame der aktuellen Animation anzeigen
            self.canvas.itemconfig(self.sprite_id, image=next(self.current_frame))
        except StopIteration:
            # Zurück zum Anfang der Animation
            self.current_frame = itertools.cycle(self.frames[self.current_animation])

        # Animation alle 500ms aktualisieren
        self.root.after(500, self.animate)

    def feed(self):
        self.set_animation('eating')

    def play(self):
        self.set_animation('happy')

    def sleep(self):
        self.set_animation('sleeping')

    def set_animation(self, animation):
        self.current_animation = animation
        self.current_frame = itertools.cycle(self.frames[self.current_animation])

# Hauptfenster erstellen
root = tk.Tk()
game = TamagotchiGame(root)
root.mainloop()
