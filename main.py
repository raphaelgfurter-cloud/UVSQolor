import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import PIL as pil
import truc_complet_au_cas_ou as tcc
from truc_complet_au_cas_ou import (
    filtre_sepia, filtre_luminosite, filtre_contraste, 
    filtre_flou, filtre_flou_gaussien, filtre_nettete, filtre_fusion,
    ouvre_dialogue_luminosite, ouvre_dialogue_contraste, 
    ouvre_dialogue_flou, ouvre_dialogue_flou_gaussien,
    ouvre_dialogue_fusion, ouvre_dialogue_nettete
)

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
    if tcc.matrice_pixel is None or tcc.canvas is None:
        return

    img = Image.fromarray(tcc.matrice_pixel.astype(np.uint8))
    tcc.image_tk = ImageTk.PhotoImage(img)
    tcc.canvas.delete("all")
    tcc.canvas.config(width=img.width, height=img.height)
    tcc.canvas.create_image(0, 0, anchor=tk.NW, image=tcc.image_tk)
    fenetre_principale.update_idletasks()
# application et annulation d'effet
def applique_effet():
    tcc.origine_matrice_pixel = None
    if tcc.dialogue_effet is not None and tcc.dialogue_effet.winfo_exists():
        tcc.dialogue_effet.destroy()
        tcc.dialogue_effet = None

def annule_effet():
    if tcc.origine_matrice_pixel is not None:
        tcc.matrice_pixel = tcc.origine_matrice_pixel.copy()
        rafraichir()
    tcc.origine_matrice_pixel = None
    if tcc.dialogue_effet is not None and tcc.dialogue_effet.winfo_exists():
        tcc.dialogue_effet.destroy()
        tcc.dialogue_effet = None
# Callbacks
def charger(container):
    """
    Ouvre un fichier image et initialise la matrice de pixels.
    """
    nom_fichier = filedialog.askopenfilename(
        title="Ouvrir une image",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp"), ("Tous les fichiers", "*.*")]
    )
    if not nom_fichier:
        return
    try:
        img = Image.open(nom_fichier).convert("RGB")
        tcc.matrice_pixel = np.array(img)
        tcc.image_tk = ImageTk.PhotoImage(img)
        if tcc.canvas is None:
            tcc.canvas = tk.Canvas(container, width=img.width, height=img.height, bg="gray")
            tcc.canvas.pack()
        else:
            tcc.canvas.delete("all")
            tcc.canvas.config(width=img.width, height=img.height)
        tcc.canvas.create_image(0, 0, anchor=tk.NW, image=tcc.image_tk)
        fenetre_principale.update_idletasks()
        messagebox.showinfo("Succès", "Image chargée avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")

def chargement(event=None):
    return charger(fenetre_principale)

def filtre_sepia_callback():
    filtre_sepia()

def filtre_luminosite_callback():
    ouvre_dialogue_luminosite()

def filtre_contraste_callback():
    ouvre_dialogue_contraste()

def filtre_flou_callback():
    ouvre_dialogue_flou()

def filtre_nettete_callback():
    ouvre_dialogue_nettete()

def filtre_flou_gaussien_callback():
    ouvre_dialogue_flou_gaussien()

def filtre_fusion_callback():
    ouvre_dialogue_fusion()

# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("UVSQolor - Éditeur d'Images")
fenetre_principale.geometry("700x500")
fenetre_principale.resizable(True, True)

# Initialiser les variables globales du module tcc pour qu'elles pointent vers main
tcc.fenetre_principale = fenetre_principale
tcc.rafraichir = rafraichir
tcc.applique_effet = applique_effet
tcc.annule_effet = annule_effet

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
File_Effets.add_command(label="Sépia", command=filtre_sepia_callback)
File_Effets.add_command(label="Luminosité", command=filtre_luminosite_callback)
File_Effets.add_command(label="Contraste", command=filtre_contraste_callback)
File_Effets.add_command(label="Flou", command=filtre_flou_callback)
File_Effets.add_command(label="Flou Gaussien", command=filtre_flou_gaussien_callback)
File_Effets.add_command(label="Netteté", command=filtre_nettete_callback)
File_Effets.add_command(label="Fusion", command=filtre_fusion_callback)

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