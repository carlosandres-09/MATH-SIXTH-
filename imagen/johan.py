import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
from tkinter import filedialog

# Función para mostrar la ventana de bienvenida
def show_welcome():
    window = tk.Tk()
    window.title("Bienvenido al sonido")
    window.geometry("300x150")
    label = tk.Label(window, text="Bienvenido al sonido", font=("Arial", 18))
    label.pack(pady=40)
    window.after(3000, lambda: window.destroy())  # Cerrar después de 3 segundos
    window.mainloop()

# Funciones de graficado
def plot_spectrogram(signal, fs, title):
    plt.specgram(signal, Fs=fs, NFFT=1024, noverlap=512, cmap="viridis")
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Frecuencia [Hz]')
    plt.title(f'Espectrograma - {title}')
    plt.colorbar(label='Intensidad')
    plt.show()

def plot_time_vs_frequency(signal, fs, title):
    t = np.arange(len(signal)) / fs
    plt.plot(t, signal)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title(f'Tiempo vs Frecuencia - {title}')
    plt.show()

def plot_amplitude_vs_frequency(signal, fs, title):
    N = len(signal)
    yf = np.fft.fft(signal)
    xf = np.fft.fftfreq(N, 1 / fs)[:N//2]
    plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Amplitud')
    plt.title(f'Amplitud vs Frecuencia (FFT) - {title}')
    plt.show()

# Función para procesar audio
def process_audio(file_path):
    # Leer archivo de audio
    fs, data = wavfile.read(file_path)
    
    # Reproducir el archivo de audio
    sd.play(data, fs)
    sd.wait()

    # Obtener el nombre del archivo sin la ruta completa
    output_name = file_path.split("/")[-1]

    # Graficar las señales
    plot_time_vs_frequency(data, fs, output_name)
    plot_spectrogram(data, fs, output_name)
    plot_amplitude_vs_frequency(data, fs, output_name)

# Función para seleccionar y procesar archivos de audio
def select_audio_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.wav")])
    for file_path in file_paths:
        process_audio(file_path)

# Mostrar ventana de bienvenida
show_welcome()

# Crear ventana para seleccionar archivos
root = tk.Tk()
root.title("Procesador de Audios")
root.geometry("400x200")

label = tk.Label(root, text="Selecciona los archivos de audio que deseas procesar:", font=("Arial", 12))
label.pack(pady=20)

button = tk.Button(root, text="Cargar Archivos", command=select_audio_files, font=("Arial", 14), bg="orange", fg="white")
button.pack(pady=10)

root.mainloop()
