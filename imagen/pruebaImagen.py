import cv2
import numpy as np
from scipy.signal import wiener
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, Frame, messagebox

# Función para cargar imagen usando un cuadro de diálogo
def cargar_imagen():
    # Abrir un cuadro de diálogo para seleccionar la imagen
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar imagen", 
                                             filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    if not ruta_imagen:
        messagebox.showinfo("Información", "No se seleccionó ninguna imagen.")
        return None
    return ruta_imagen

# Función principal para procesar la imagen
def procesar_imagen():
    ruta_imagen = cargar_imagen()
    if ruta_imagen is not None:
        # Leer la imagen seleccionada
        RGB = cv2.imread(ruta_imagen)
        if RGB is None:
            messagebox.showerror("Error", "No se pudo cargar la imagen.")
        else:
            # Convertir a escala de grises
            I = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

            # Añadir ruido gaussiano
            mean = 0
            var = 0.025
            sigma = var ** 0.5
            gauss = np.random.normal(mean, sigma, I.shape)
            J = I + gauss * 255  # Añadir el ruido a la imagen

            # Aplicar filtro Wiener para eliminar el ruido
            K = wiener(J, (5, 5))

            # Mostrar ambas imágenes completas
            mostrar_imagenes(I, J, K)

# Función para mostrar imágenes completas en una nueva ventana
def mostrar_imagenes(original, con_ruido, filtrada):
    plt.figure(figsize=(15, 10))

    plt.subplot(1, 3, 1)
    plt.imshow(original, cmap='gray')
    plt.title('Imagen Original', fontsize=14)
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(con_ruido, cmap='gray')
    plt.title('Imagen con Ruido Gaussiano', fontsize=14)
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(filtrada, cmap='gray')
    plt.title('Imagen Filtrada con Wiener', fontsize=14)
    plt.axis('off')

    # Ajustar la disposición y mostrar las imágenes
    plt.tight_layout()
    plt.show()

# Crear la ventana principal
root = Tk()
root.title("Procesador de Imágenes")
root.geometry("600x400")  # Aumentar el tamaño de la ventana
root.configure(bg="#f0f0f0")

# Crear un marco para el contenido
frame = Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(padx=40, pady=40)  # Aumentar el espacio del marco

# Título
titulo = Label(frame, text="Procesador de Imágenes", font=("Arial", 20, "bold"), bg="#ffffff")
titulo.pack(pady=20)

# Botón para cargar y procesar la imagen
btn_cargar = Button(frame, text="Cargar Imagen", command=procesar_imagen, font=("Arial", 14), bg="#4CAF50", fg="white", padx=10, pady=5)
btn_cargar.pack(pady=20)

# Mensaje de los creadores
creadores = Label(frame, text="Por Carlos Soacha, Johan Leal, Jhordy Miranda", font=("Arial", 12), bg="#ffffff")
creadores.pack(pady=20)

# Iniciar el bucle principal
root.mainloop()
