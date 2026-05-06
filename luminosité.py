import tkinter as tk
import numpy as np
from main import rafraichir, fenetre_principale, applique_effet, annule_effet, dialogue_effet, matrice_pixel, origine_matrice_pixel

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
        
def filtre_luminosite(m):
    global matrice_pixel, origine_matrice_pixel
    if matrice_pixel is None or origine_matrice_pixel is None:
        return
    try:
        m = float(m)
    except (TypeError, ValueError):
        return
    m = np.clip(m, 0.01, 0.99)
    img = origine_matrice_pixel.astype(np.float32)
    max_value = float(np.iinfo(origine_matrice_pixel.dtype).max)
    gamma = np.log(m) / np.log(0.5)
    matrice_pixel = np.clip(np.power(img / max_value, gamma) * max_value, 0, max_value).astype(origine_matrice_pixel.dtype)
    rafraichir()

def correction_gamma(m):
    filtre_luminosite(m)