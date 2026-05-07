import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import PIL as pil
import sepia


# Définition des variables globales
matrice_pixel = None
origine_matrice_pixel = None
canvas = None
image_tk = None
dialogue_effet = None
slider_luminosite = None

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
# application et annulation d'effet
def applique_effet():
    global dialogue_effet, origine_matrice_pixel
    origine_matrice_pixel = None
    if dialogue_effet is not None and dialogue_effet.winfo_exists():
        dialogue_effet.destroy()
        dialogue_effet = None

def annule_effet():
    global matrice_pixel, dialogue_effet, origine_matrice_pixel
    if origine_matrice_pixel is not None:
        matrice_pixel = origine_matrice_pixel
        rafraichir()
    origine_matrice_pixel = None
    if dialogue_effet is not None and dialogue_effet.winfo_exists():
        dialogue_effet.destroy()
        dialogue_effet = None
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

def filtre_sepia():
    sepia.filtre_sépia(matrice_pixel, rafraichir)

def filtre_luminosite_b():
    from changement_luminosité import ouvre_dialogue_luminosite
    ouvre_dialogue_luminosite()

def filtre_contraste():
    pass

def filtre_flou():
    pass

def filtre_nettete():
    pass

# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("UVSQolor - Éditeur d'Images")
fenetre_principale.geometry("700x500")
fenetre_principale.resizable(True, True)

# Création du menu principal
menubar = tk.Menu()

# Menu Fichier
File_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(menu=File_menu, label="Fichier")
File_menu.add_command(label="Ouvrir Image", accelerator="Ctrl+O", command=chargement)
File_menu.add_separator()
File_menu.add_command(label="Quitter", accelerator="Ctrl+Q", command=fenetre_principale.quit)
fenetre_principale.bind_all("<Control-o>", chargement)
fenetre_principale.bind_all("<Control-q>", lambda e: fenetre_principale.quit())

# Menu Effets
File_Effets = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(menu=File_Effets, label="Effets")
File_Effets.add_command(label="Sépia", command=filtre_sepia)
File_Effets.add_command(label="Luminosité", command=filtre_luminosite_b)
File_Effets.add_command(label="Contraste", command=filtre_contraste)
File_Effets.add_command(label="Flou", command=filtre_flou)
File_Effets.add_command(label="Netteté", command=filtre_nettete)

# Menu Aide
File_Aide = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(menu=File_Aide, label="Aide")
File_Aide.add_command(
    label="À propos",
    command=lambda: messagebox.showinfo(
        "À propos",
        "UVSQolor v1.0\n\nÉditeur d'images simple avec filtres\n\n"
        "Filtres implémentés:\n"
        "• Luminosité (Correction Gamma)\n"
        "• Contraste (Gamma pivotée)\n"
        "• Flou (Convolution)\n"
        "• Netteté (Unsharp Masking)"
    )
)

fenetre_principale.config(menu=menubar)
fenetre_principale.mainloop()