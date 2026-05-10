def filtre_nettete(intensite=1.0, rayon_flou=1):
    # Augmente la netteté par technique d'unsharp masking (masquage flou)
    # intensite: nommé pour le facteur d'amplification des détails
    # rayon_flou: rayon du flou utilisé pour extraire les détails (details = image - image_floue)
    # details = img - img_floue: filtre passe-haut (haute fréquence)
    # img + intensite * details: amplification des contours pour plus de netteté
    global matrice_pixel, origine_matrice_pixel
    if matrice_pixel is None or origine_matrice_pixel is None:
        return
    try:
        intensite = float(intensite)
        rayon_flou = int(rayon_flou)
    except (TypeError, ValueError):
        return
    rayon_flou = max(1, rayon_flou)
    intensite = np.clip(intensite, 0, 3.0)
    taille = 2 * rayon_flou + 1
    kernel = np.ones((taille, taille)) / (taille * taille)
    img = origine_matrice_pixel.astype(np.float32)
    img_floue = img.copy()
    for i in range(3):
        img_floue[:, :, i] = convolve2d(img[:, :, i], kernel, mode='same', boundary='symm')
    details = img - img_floue
    result = img + intensite * details
    matrice_pixel = np.clip(result, 0, 255).astype(np.uint8)
    rafraichir()


def correction_nettete(intensite):
    rayon = slider_rayon_nettete.get() if slider_rayon_nettete else 1
    filtre_nettete(intensite, rayon)


def correction_rayon_nettete(rayon):
    intensite = slider_intensite_nettete.get() if slider_intensite_nettete else 1.0
    filtre_nettete(intensite, rayon)
def ouvre_dialogue_nettete():
    global dialogue_effet, slider_intensite_nettete, slider_rayon_nettete, origine_matrice_pixel
    if matrice_pixel is None:
        messagebox.showwarning("Attention", "Veuillez d'abord charger une image")
        return
    if dialogue_effet and dialogue_effet.winfo_exists():
        dialogue_effet.lift()
        return
    origine_matrice_pixel = matrice_pixel.copy()
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Netteté")
    dialogue_effet.geometry("350x220")
    dialogue_effet.grab_set()
    tk.Label(dialogue_effet, text="Intensité:", font=("Arial", 10, "bold")).pack(pady=5)
    slider_intensite_nettete = tk.Scale(dialogue_effet, from_=0.0, to=3.0, orient=tk.HORIZONTAL, 
        length=300, resolution=0.1, digits=1, command=correction_nettete)
    slider_intensite_nettete.set(1.0)
    slider_intensite_nettete.pack(pady=10)
    tk.Label(dialogue_effet, text="Rayon de flou:", font=("Arial", 10, "bold")).pack(pady=5)
    slider_rayon_nettete = tk.Scale(dialogue_effet, from_=1, to=5, orient=tk.HORIZONTAL, 
        length=300, command=correction_rayon_nettete)
    slider_rayon_nettete.set(1)
    slider_rayon_nettete.pack(pady=10)
    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)
    tk.Button(frame_boutons, text="Appliquer", command=applique_effet, bg="green", fg="white", padx=15).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_boutons, text="Annuler", command=annule_effet, bg="red", fg="white", padx=15).pack(side=tk.LEFT, padx=10)
    dialogue_effet.protocol("WM_DELETE_WINDOW", annule_effet)
    dialogue_effet.transient(fenetre_principale)