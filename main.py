import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL as pil
import sepia
import luminosité
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

def filtre_luminosite():
    pass

def ouvre_dialogue_luminosite():
    global dialogue_effet, slider_luminosite, origine_matrice_pixel
    if matrice_pixel is None:
        return
    if dialogue_effet is not None and dialogue_effet.winfo_exists():
        dialogue_effet.lift()
        return
    origine_matrice_pixel = matrice_pixel.copy()
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Luminosité")
    dialogue_effet.geometry("300x150")
    dialogue_effet.grab_set()

    slider_luminosite = tk.Scale(
        dialogue_effet,
        from_=0.05,
        to=0.95,
        orient=tk.HORIZONTAL,
        length=200,
        resolution=0.01,
        digits=2,
        command=correction_gamma,
    )
    slider_luminosite.set(0.50)
    slider_luminosite.pack(pady=20)

    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)

    bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=applique_effet)
    bouton_appliquer.pack(side=tk.LEFT, padx=10)
    bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
    bouton_annuler.pack(side=tk.LEFT, padx=10)

    dialogue_effet.protocol("WM_DELETE_WINDOW", annule_effet)
    dialogue_effet.transient(fenetre_principale)

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
File_Effets.add_command(label="Filtre sépia", command=filtre_sepia)
File_Effets.add_command(label="Filtre luminosité", command=filtre_luminosite)
fenetre_principale.config(menu=menubar)
fenetre_principale.mainloop()