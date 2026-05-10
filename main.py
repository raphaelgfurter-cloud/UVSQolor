import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import PIL as pil
import fonctions_complete as fc

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
    if fc.matrice_pixel is None or fc.canvas is None:
        return

    img = Image.fromarray(fc.matrice_pixel.astype(np.uint8))
    fc.image_tk = ImageTk.PhotoImage(img)
    fc.canvas.delete("all")
    fc.canvas.config(width=img.width, height=img.height)
    fc.canvas.create_image(0, 0, anchor=tk.NW, image=fc.image_tk)
    fenetre_principale.update_idletasks()
# application et annulation d'effet
def applique_effet():
    fc.origine_matrice_pixel = None
    if fc.dialogue_effet is not None and fc.dialogue_effet.winfo_exists():
        fc.dialogue_effet.destroy()
        fc.dialogue_effet = None

def annule_effet():
    if fc.origine_matrice_pixel is not None:
        fc.matrice_pixel = fc.origine_matrice_pixel.copy()
        rafraichir()
    fc.origine_matrice_pixel = None
    if fc.dialogue_effet is not None and fc.dialogue_effet.winfo_exists():
        fc.dialogue_effet.destroy()
        fc.dialogue_effet = None
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
        fc.matrice_pixel = np.array(img)
        fc.image_tk = ImageTk.PhotoImage(img)
        if fc.canvas is None:
            fc.canvas = tk.Canvas(container, width=img.width, height=img.height, bg="gray")
            fc.canvas.pack()
        else:
            fc.canvas.delete("all")
            fc.canvas.config(width=img.width, height=img.height)
        fc.canvas.create_image(0, 0, anchor=tk.NW, image=fc.image_tk)
        fenetre_principale.update_idletasks()
        messagebox.showinfo("Succès", "Image chargée avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")

def chargement(event=None):
    return charger(fenetre_principale)

def filtre_sepia_callback():
    fc.filtre_sepia()

def filtre_luminosite_callback():
    fc.ouvre_dialogue_luminosite()

def filtre_contraste_callback():
    fc.ouvre_dialogue_contraste()

def filtre_flou_callback():
    fc.ouvre_dialogue_flou()

def filtre_nettete_callback():
    fc.ouvre_dialogue_nettete()

def filtre_flou_gaussien_callback():
    fc.ouvre_dialogue_flou_gaussien()

def filtre_fusion_callback():
    fc.ouvre_dialogue_fusion()

# Création de la fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("UVSQolor - Éditeur d'Images")
fenetre_principale.geometry("700x500")
fenetre_principale.resizable(True, True)

# Initialiser les variables globales du module fc pour qu'elles pointent vers main
fc.fenetre_principale = fenetre_principale
fc.rafraichir = rafraichir
fc.applique_effet = applique_effet
fc.annule_effet = annule_effet

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
        "• Filtre Sépia (effet vieux)"
        "• Luminosité (Correction Gamma)\n"
        "• Contraste (Gamma pivotée)\n"
        "• Flou (Convolution)\n"
        "• Flou Gaussien (écart type)"
        "• Netteté (Unsharp Masking)"
        "• Fusion d'image (avec opacité à 0.5)"
    )
)

fenetre_principale.config(menu=menubar)
fenetre_principale.mainloop()