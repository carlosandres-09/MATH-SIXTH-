import numpy as np 
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.signal import butter, filtfilt
import sounddevice as sd
from scipy.fft import fft, ifft, fftfreq
from tkinter import Tk, Button, messagebox, Label
from tkinter.filedialog import askopenfilename

# Definir el filtro pasa-bajos
def filtro_pasa_bajos(corte, fs, orden=5):
    nyq = 0.5 * fs
    corte_normal = corte / nyq
    b, a = butter(orden, corte_normal, btype='low', analog=False)
    return b, a

# Función para procesar el audio
def procesar_audio(archivo):
    # Cargar el audio
    señal, fs = librosa.load(archivo, sr=None)

    # Reproducir el sonido original
    print("Reproduciendo el sonido original...")
    sd.play(señal, samplerate=fs)
    sd.wait()  # Espera hasta que termine la reproducción

    # Realizar la Transformada Rápida de Fourier (FFT)
    Y = fft(señal)
    frecuencias = fftfreq(len(Y), 1 / fs)

    # Identificar la frecuencia fundamental (pico máximo en el espectro de frecuencias)
    magnitud = np.abs(Y)
    frecuencia_fundamental = frecuencias[np.argmax(magnitud)]
    print(f"Frecuencia fundamental detectada: {frecuencia_fundamental:.2f} Hz")

    # Crear un filtro que conserve las frecuencias cercanas a la fundamental
    espectro_filtrado = np.zeros_like(Y)
    ancho_frecuencia = 1000  # Aumentar el rango de frecuencias a conservar
    for i in range(len(frecuencias)):
        if abs(frecuencias[i] - frecuencia_fundamental) < ancho_frecuencia:
            espectro_filtrado[i] = Y[i]

    # Reconstruir el sonido a partir del espectro filtrado utilizando la IFFT
    señal_reconstruida = ifft(espectro_filtrado).real

    # Crear el tono puro (solo la frecuencia fundamental)
    duracion = len(señal) / fs  # Duración en segundos
    t = np.linspace(0, duracion, len(señal), endpoint=False)  # Tiempo para la duración del audio
    tono_puro = np.sin(2 * np.pi * frecuencia_fundamental * t)

    # Reproducir el tono puro
    print("Reproduciendo el tono puro...")
    sd.play(tono_puro, samplerate=fs)
    sd.wait()  # Espera hasta que termine la reproducción

    # Reproducir el sonido reconstruido (resultado de la IFFT)
    print("Reproduciendo el sonido reconstruido (resultado de la IFFT)...")
    sd.play(señal_reconstruida, samplerate=fs)
    sd.wait()  # Espera hasta que termine la reproducción

    # Calcular el espectro normal
    espectro_normal = np.fft.fft(señal)
    frecuencias = np.fft.fftfreq(len(señal), 1/fs)

    # Aplicar el filtro pasa-bajos
    corte = 300  # Frecuencia de corte (Hz), ajustado para guitarra
    orden = 4  # Orden del filtro
    b, a = filtro_pasa_bajos(corte, fs, orden)
    señal_filtrada = filtfilt(b, a, señal)

    # Aumentar el volumen de la señal filtrada
    señal_filtrada = np.clip(señal_filtrada, -1.0, 1.0)  # Asegurar que no supere [-1, 1]

    # Calcular el espectro filtrado
    espectro_filtrado = np.fft.fft(señal_filtrada)

    # Crear una figura para los gráficos de amplitud
    plt.figure(figsize=(16, 12))

    # Gráfico de la señal original y la señal filtrada
    plt.subplot(4, 2, 1)
    plt.plot(señal, color='green', label='Señal Original')
    plt.plot(señal_filtrada, color='orange', label='Señal Filtrada', linestyle='--')
    plt.title(f'Señal Original y Filtrada: {archivo}')
    plt.xlabel('Muestra')
    plt.ylabel('Amplitud')
    plt.legend()

    # Gráfico de la señal original y la señal reconstruida
    plt.subplot(4, 2, 4)
    plt.plot(señal, color='green', label='Señal Original')
    plt.plot(señal_reconstruida, color='blue', label='Señal Reconstruida', linestyle='--')
    plt.title('Señal Original vs Señal Reconstruida')
    plt.xlabel('Muestra')
    plt.ylabel('Amplitud')
    plt.legend()

    # Gráfico de la señal reconstruida y la señal filtrada
    plt.subplot(4, 2, 5)
    plt.plot(señal_reconstruida, color='blue', label='Señal Original')
    plt.plot(señal_filtrada, color='orange', label='Señal Reconstruida', linestyle='--')
    plt.title('Señal Original vs Señal Reconstruida')
    plt.xlabel('Muestra')
    plt.ylabel('Amplitud')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Crear una figura para los gráficos de los espectros
    plt.figure(figsize=(16, 12))

    # Gráfico del espectro normal
    plt.subplot(4, 2, 1)
    plt.plot(frecuencias[:len(frecuencias)//2], np.abs(espectro_normal)[:len(espectro_normal)//2], color='green')
    plt.title('Espectro Normal')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')

    # Gráfico del espectro filtrado
    plt.subplot(4, 2, 4)
    plt.plot(frecuencias[:len(frecuencias)//2], np.abs(espectro_filtrado)[:len(espectro_filtrado)//2], color='orange')
    plt.title('Espectro Filtrado')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')

    # Espectro de la señal reconstruida
    espectro_reconstruido = np.fft.fft(señal_reconstruida)
    plt.subplot(4, 2, 5)
    plt.plot(frecuencias[:len(frecuencias)//2], np.abs(espectro_reconstruido)[:len(espectro_reconstruido)//2], color='blue')
    plt.title('Espectro de la Señal Reconstruida')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')

    plt.tight_layout()
    plt.show()

    # Crear una figura para los espectrogramas
    plt.figure(figsize=(16, 12))

    # Espectrograma de la señal original
    plt.subplot(4, 2, 1)
    D_original = librosa.amplitude_to_db(np.abs(librosa.stft(señal)), ref=np.max)
    librosa.display.specshow(D_original, sr=fs, x_axis='time', y_axis='log', cmap='plasma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma Señal Original')

    # Espectrograma de la señal filtrada
    plt.subplot(4, 2, 4)
    D_filtrada = librosa.amplitude_to_db(np.abs(librosa.stft(señal_filtrada)), ref=np.max)
    librosa.display.specshow(D_filtrada, sr=fs, x_axis='time', y_axis='log', cmap='plasma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma Señal Filtrada')

    # Espectrograma de la señal reconstruida
    plt.subplot(4, 2, 5)
    D_reconstruida = librosa.amplitude_to_db(np.abs(librosa.stft(señal_reconstruida)), ref=np.max)
    librosa.display.specshow(D_reconstruida, sr=fs, x_axis='time', y_axis='log', cmap='plasma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma de la Señal Reconstruida')

    plt.tight_layout()
    plt.show()

# Función para abrir un nuevo archivo de audio
def abrir_archivo_audio():
    archivo = askopenfilename(title="Selecciona un archivo de audio", filetypes=[("Archivos de Audio", "*.wav;*.mp3;*.ogg;*.flac")])
    if archivo:
        procesar_audio(archivo)
    else:
        messagebox.showinfo("Información", "No se seleccionó ningún archivo.")

# Función para cerrar la aplicación
def cerrar_aplicacion():
    root.quit()

# Crear una ventana de Tkinter
root = Tk()
root.title("Procesador de Audio")

# Etiqueta con los nombres de los creadores
Label(root, text="Creado por Carlos Soacha, Johan Leal, Jhordy Miranda", font=("Arial", 12)).pack(pady=10)

# Botón para seleccionar un archivo de audio
boton_seleccionar_audio = Button(root, text="Seleccionar Archivo de Audio", command=abrir_archivo_audio, font=("Arial", 14), bg="orange")
boton_seleccionar_audio.pack(pady=20)

# Botón para cerrar la aplicación
boton_salir = Button(root, text="Salir", command=cerrar_aplicacion, font=("Arial", 12), fg="white", bg="red")
boton_salir.pack(pady=10)

# Iniciar el bucle principal de la ventana
root.mainloop()
        