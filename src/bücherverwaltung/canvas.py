import tkinter as tk
from tkinter import ttk

def canvas(root):

    # Canvas für den Scrollbereich erstellen
    canvas = tk.Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbars erstellen (horizontal und vertikal)
    scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    scrollbar_x.pack(side="bottom", fill="x")

    # Frame in der Canvas erstellen, der gescrollt werden kann
    scrollable_frame = tk.Frame(canvas)

    # Fenster in der Canvas erstellen, in das der Frame eingefügt wird
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Scroll-Funktionalität hinzufügen
    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scrollregion)

    # Scrollbars mit der Canvas verknüpfen
    canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)