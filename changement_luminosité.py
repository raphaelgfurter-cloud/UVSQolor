def filtre_luminosite(m):
    # Ajuste la luminosité par correction gamma
    # gamma = ln(m) / ln(0.5) : formule pour transformer le paramètre d'entrée en exposant
    # np.power(img / max_value, gamma): élève chaque pixel à la puissance gamma (correction non-linéaire)
    # m est nommé en une lettre car c'est un paramètre mathématique standard pour la luminosité
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


def correction_luminosite(m):
    filtre_luminosite(m)
    
    
def ouvre_dialogue_luminosite():
    # Crée une fenêtre de dialogue Tkinter (tk.Toplevel) avec un slider (curseur)
    # tk.Toplevel(): crée une nouvelle fenêtre de dialogue indépendante
    # tk.Scale(): widget Tkinter pour slider/curseur avec valeurs numériques
    # command=correction_luminosite: lie le slider à la fonction de rappel (callback)
    # grab_set(): rend la fenêtre modale (on ne peut interagir que avec elle)
    global dialogue_effet, slider_luminosite, origine_matrice_pixel
    if matrice_pixel is None:
        messagebox.showwarning("Attention", "Veuillez d'abord charger une image")
        return
    if dialogue_effet and dialogue_effet.winfo_exists():
        dialogue_effet.lift()
        return
    origine_matrice_pixel = matrice_pixel.copy()
    dialogue_effet = tk.Toplevel(fenetre_principale)
    dialogue_effet.title("Luminosité")
    dialogue_effet.geometry("300x150")
    dialogue_effet.grab_set()
    slider_luminosite = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, 
        length=200, resolution=0.01, digits=2, command=correction_luminosite)
    slider_luminosite.set(0.50)
    slider_luminosite.pack(pady=20)
    frame_boutons = tk.Frame(dialogue_effet)
    frame_boutons.pack(side=tk.BOTTOM, pady=10)
    tk.Button(frame_boutons, text="Appliquer", command=applique_effet, bg="green", fg="white", padx=15).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_boutons, text="Annuler", command=annule_effet, bg="red", fg="white", padx=15).pack(side=tk.LEFT, padx=10)
    dialogue_effet.protocol("WM_DELETE_WINDOW", annule_effet)
    dialogue_effet.transient(fenetre_principale)