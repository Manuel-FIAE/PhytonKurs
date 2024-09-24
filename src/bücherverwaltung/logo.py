from PIL import Image, ImageTk

# Funktion zum Setzen eines Logos für ein Fenster
def set_window_logo(root, image_path):
    """
    Setzt das Icon für das Tkinter-Hauptfenster.
    
    Args:
    root: Das Tkinter-Hauptfenster.
    image_path: Der Dateipfad des Logos.
    """
    logo_image = Image.open(image_path)
    logo_photo = ImageTk.PhotoImage(logo_image)
    root.iconphoto(False, logo_photo)
