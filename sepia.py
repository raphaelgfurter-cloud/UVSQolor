import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL as pil


matrice_pixel = None
canvas = None
image_tk = None

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


def filtre_sépia(event=None):
    global matrice_pixel
    if matrice_pixel is None:
        return

# valeur prise de https://fredbl.gitlab.io/algebre-lineaire-et-imagerie-numerique/couleurs.html#conversion-en-sepia

    img = matrice_pixel.astype(np.float32)
    transform = np.array([[0.393, 0.769, 0.189],
                          [0.349, 0.686, 0.168],
                          [0.272, 0.534, 0.131]], dtype=np.float32)

    sepia = img.dot(transform.T)
    matrice_pixel = np.clip(sepia, 0, 255).astype(np.uint8)
    rafraichir()
