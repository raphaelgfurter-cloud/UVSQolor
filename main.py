import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL as pil

# Définition des variables globales
matrice_pixel = None
canvas = None
image_tk = None

# Gestion de l'affichage
def rafraichir():
    """
    Convertit la matrice NumPy en image Tkinter et met à jour le canvas.
    """
    global image_tk, canvas, matrice_pixel
    if matrice_pixel is None or canvas is None:
        return

    img = Image.fromarray(matrice_pixel.astype(np.uint8))
    image_tk = ImageTk.PhotoImage(img)
    canvas.delete("all")
    canvas.config(width=img.width, height=img.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
    fenetre_principale.update_idletasks()

# Callbacks
def charger(container):
    """
    Ouvre un fichier image et initialise la matrice de pixels.
    """
    global image_tk, canvas, matrice_pixel
    nom_fichier = filedialog.askopenfilename(title="Ouvrir une image")
    if not nom_fichier:
        return

    img = pil.Image.open(nom_fichier).convert("RGB")
    matrice_pixel = np.array(img)
    image_tk = ImageTk.PhotoImage(img)

    if canvas is None:
        canvas = tk.Canvas(container, width=img.width, height=img.height)
        canvas.pack()
    else:
        canvas.delete("all")
        canvas.config(width=img.width, height=img.height)

    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
    fenetre_principale.update_idletasks()

def chargement(event=None):
    return charger(fenetre_principale)

def sepia():
    import sepia.py
    
# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("UVSQolor")

menubar = tk.Menu()
File_new = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(menu=File_new, label="Fichier")
File_new.add_command(label="Nouveau", accelerator="Ctrl+O", command=chargement)
File_new.bind_all("<Control-o>", chargement)
File_new.bind_all("<Control-O>", chargement)

File_Effets = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(menu=File_Effets, label="Effets")
File_Effets.add_command(label="Filtre sépia", command=sepia)
fenetre_principale.config(menu=menubar)
fenetre_principale.mainloop()