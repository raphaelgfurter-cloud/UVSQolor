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