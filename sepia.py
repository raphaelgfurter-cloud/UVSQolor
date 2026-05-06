import numpy as np

def filtre_sépia(matrice_pixel, rafraichir_func, event=None):
    if matrice_pixel is None:
        return

# valeur prise de https://fredbl.gitlab.io/algebre-lineaire-et-imagerie-numerique/couleurs.html#conversion-en-sepia

    img = matrice_pixel.astype(np.float32)
    transform = np.array([[0.393, 0.769, 0.189],
                          [0.349, 0.686, 0.168],
                          [0.272, 0.534, 0.131]], dtype=np.float32)

    sepia_img = img.dot(transform.T)
    matrice_pixel[:] = np.clip(sepia_img, 0, 255).astype(np.uint8)
    rafraichir_func()
