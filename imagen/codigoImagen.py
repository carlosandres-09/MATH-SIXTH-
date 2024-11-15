import cv2
import numpy as np
from scipy.signal import wiener
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Button, Frame, messagebox, Canvas
import random

# Función para cargar imagen usando un cuadro de diálogo
def cargar_imagen():
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
        RGB = cv2.imread(ruta_imagen)
        if RGB is None:
            messagebox.showerror("Error", "No se pudo cargar la imagen. Por favor, verifica el archivo.")
            return
        else:
            # Convertir imagen a escala de grises
            I = cv2.cvtColor(RGB, cv2.COLOR_BGR2GRAY)

            # Añadir ruido gaussiano
            mean = 0
            var = 0.025
            sigma = var ** 0.5
            gauss = np.random.normal(mean, sigma, I.shape)
            J = I + gauss * 255

            # Aplicar filtro Wiener
            K = wiener(J, (5, 5))

            # Mostrar imágenes
            mostrar_imagenes(RGB, I, J, K)

# Función para mostrar imágenes en una nueva ventana de forma organizada
def mostrar_imagenes(original_color, original_gris, con_ruido, filtrada):
    # Crear una nueva figura
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.subplots_adjust(hspace=0.4, wspace=0.3)  # Ajustar el espacio entre imágenes

    # Imagen Original
    axes[0, 0].imshow(cv2.cvtColor(original_color, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('IMAGEN ORIGINAL (COLOR)', fontsize=12, fontweight='bold')
    axes[0, 0].axis('off')

    # Imagen en Escala de Grises
    axes[0, 1].imshow(original_gris, cmap='gray')
    axes[0, 1].set_title('IMAGEN EN ESCALA DE GRIS', fontsize=12, fontweight='bold')
    axes[0, 1].axis('off')

    # Imagen con Ruido Gaussiano
    axes[1, 0].imshow(con_ruido, cmap='gray')
    axes[1, 0].set_title('IMAGEN CON RUIDO GAUSSIANO', fontsize=12, fontweight='bold')
    axes[1, 0].axis('off')

    # Imagen Filtrada con Wiener
    axes[1, 1].imshow(filtrada, cmap='gray')
    axes[1, 1].set_title('IMAGEN FILTRADA CON WIENER', fontsize=12, fontweight='bold')
    axes[1, 1].axis('off')

    # Mostrar la figura
    plt.show()

# Crear la ventana principal
root = Tk()
root.title("Procesador de Imágenes - Matemáticas Divertidas")
root.geometry("800x600")  
root.minsize(400, 300)  # Tamaño mínimo de la ventana
root.configure(bg="#e6f7ff")  # Fondo azul pastel claro

# Crear un marco para el contenido
frame = Frame(root, bg="#e6f7ff", padx=20, pady=20, bd=5, relief="raised")
frame.pack(padx=20, pady=20, fill='both', expand=True)

# Título
titulo = Label(frame, text="🔬 PROCESADOR DE IMÁGENES 🔬", font=("Arial", 24, "bold"), bg="#e6f7ff", fg="#4CAF50")
titulo.pack(pady=10)

# Botón para cargar y procesar la imagen
btn_cargar = Button(frame, text="📸 CARGAR IMAGEN 📸", command=procesar_imagen, font=("Arial", 14), bg="#ff9800", fg="white", padx=10, pady=5, borderwidth=2)
btn_cargar.pack(pady=10)

# Mensaje de los creadores
creadores = Label(frame, text="CREADO POR CARLOS SOACHA, JOHAN LEAL, JHORDY MIRANDA 📐", font=("Arial", 12, "italic"), bg="#e6f7ff", fg="#4CAF50")
creadores.pack(pady=10)

# Canvas para el fondo matemático
canvas = Canvas(root, width=800, height=200, bg="#e6f7ff", highlightthickness=0)
canvas.pack(side="bottom", fill="x")

# Generar un patrón matemático
def dibujar_patron():
    for _ in range(50):  # Cambiar el número de patrones
        x1 = random.randint(0, 800)
        y1 = random.randint(0, 200)
        x2 = x1 + random.randint(20, 100)
        y2 = y1 + random.randint(20, 100)
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=2)

dibujar_patron()

# Iniciar el bucle principal
root.mainloop()
