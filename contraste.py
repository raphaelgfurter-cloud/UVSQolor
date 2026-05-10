def filtre_contraste(c, p=0.5):
    # Ajuste le contraste avec correction gamma pivotée
    # c: paramètre de contraste (-1 à 1), nommé court car c'est l'exposant mathématique
    # p: point pivot (pivot point), les pixels à ce niveau de gris restent inchangés
    # np.where(): applique deux formules différentes selon que les pixels sont sombres ou clairs
    global matrice_pixel, origine_matrice_pixel
    if matrice_pixel is None or origine_matrice_pixel is None:
        return
    try:
        c = float(c)
        p = float(p)
    except (TypeError, ValueError):
        return
    p = np.clip(p, 0.001, 0.999)
    gamma = 2.0 ** c
    img = origine_matrice_pixel.astype(np.float32)
    max_value = float(np.iinfo(origine_matrice_pixel.dtype).max)
    img_norm = img / max_value
    result = np.where(
        img_norm <= p,
        p * np.power(img_norm / p, gamma),
        1 - (1 - p) * np.power((1 - img_norm) / (1 - p), gamma)
    )
    matrice_pixel = np.clip(result * max_value, 0, max_value).astype(origine_matrice_pixel.dtype)
    rafraichir()


def correction_contraste(c):
    p = slider_pivot.get() if slider_pivot else 0.5
    filtre_contraste(c, p)


def correction_pivot(p):
    c = slider_contraste.get() if slider_contraste else 0.0
    filtre_contraste(c, p)
    
def ouvre_dialogue_contraste():
    global dialogue_effet, slider_contraste, slider_pivot, origine_matrice_pixel
    if matrice_pixel is None:
        messagebox.showwarning("Attention", "Veuillez d'abord charger une image")
        return
    if dialogue_effet and dialogue_effet.winfo_exists():
        dialogue_effet.lift()
        return
    origine_matrice_pixel = matrice_pixel.copy()
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Contraste")
    dialogue_effet.geometry("350x220")
    dialogue_effet.grab_set()
    tk.Label(dialogue_effet, text="Contraste:", font=("Arial", 10, "bold")).pack(pady=5)
    slider_contraste = tk.Scale(dialogue_effet, from_=-1.0, to=1.0, orient=tk.HORIZONTAL, 
        length=300, resolution=0.01, digits=2, command=correction_contraste)
    slider_contraste.set(0.0)
    slider_contraste.pack(pady=10)
    tk.Label(dialogue_effet, text="Pivot:", font=("Arial", 10, "bold")).pack(pady=5)
    slider_pivot = tk.Scale(dialogue_effet, from_=0.1, to=0.9, orient=tk.HORIZONTAL, 
        length=300, resolution=0.01, digits=2, command=correction_pivot)
    slider_pivot.set(0.5)
    slider_pivot.pack(pady=10)
    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)
    tk.Button(frame_boutons, text="Appliquer", command=applique_effet, bg="green", fg="white", padx=15).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_boutons, text="Annuler", command=annule_effet, bg="red", fg="white", padx=15).pack(side=tk.LEFT, padx=10)
    dialogue_effet.protocol("WM_DELETE_WINDOW", annule_effet)
    dialogue_effet.transient(fenetre_principale)