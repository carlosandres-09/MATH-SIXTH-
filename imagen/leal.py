import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.signal import butter, filtfilt, spectrogram
import sounddevice as sd
import soundfile as sf
from scipy.fft import fft, fftfreq
import os
import tkinter as tk
from tkinter import Button, Label, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Parámetros generales
fs = 44100
duracion_segundos = 2
ultimo_tono = None

# --- Función para crear un filtro pasa-bajos ---
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs  # Frecuencia de Nyquist
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# --- Función para cargar y procesar múltiples audios ---
def cargar_y_procesar_varios():
    global ultimo_tono

    # Diálogo para seleccionar varios archivos
    files = filedialog.askopenfilenames(title="Selecciona archivos de audio", 
                                        filetypes=[("Archivos de Audio", ".wav;.mp3;.ogg;.flac")])
    if not files:
        messagebox.showinfo("Información", "No se seleccionó ningún archivo.")
        return

    for file in files:
        signal, fs = librosa.load(file, sr=None)
        
        # Reproducir el sonido original
        sd.play(signal, samplerate=fs)
        sd.wait()
        
        # Calcular la frecuencia fundamental
        Y = fft(signal)
        freqs = fftfreq(len(Y), 1 / fs)
        magnitude = np.abs(Y)
        fundamental_frequency = freqs[np.argmax(magnitude)]
        
        # Filtrar frecuencias alrededor de la frecuencia fundamental
        filtered_spectrum = np.zeros_like(Y)
        frequency_bandwidth = 100
        for i in range(len(freqs)):
            if abs(freqs[i] - fundamental_frequency) < frequency_bandwidth:
                filtered_spectrum[i] = Y[i]

        # Reconstrucción de la señal filtrada
        reconstructed_signal = np.fft.ifft(filtered_spectrum).real

        # Generar un tono puro basado en la frecuencia fundamental
        t = np.linspace(0, duracion_segundos, int(fs * duracion_segundos), endpoint=False)
        tone_pure = np.sin(2 * np.pi * fundamental_frequency * t)
        ultimo_tono = tone_pure  # Guardar el tono para reproducir al cierre

        # Reproducir el tono puro
        sd.play(tone_pure, samplerate=fs)
        sd.wait()

        # Aplicar filtro pasa-bajos a la señal original
        cutoff = 3000
        b, a = butter_lowpass(cutoff, fs, order=4)
        filtered_signal = filtfilt(b, a, signal)
        filtered_signal = np.clip(filtered_signal, -1.0, 1.0)

        # Graficar los resultados
        fig, axs = plt.subplots(3, 1, figsize=(10, 8))
        
        # Gráfico 1: Tiempo vs Amplitud
        axs[0].plot(signal[:1000], color='blue', label='Señal Original')
        axs[0].plot(filtered_signal[:1000], color='orange', linestyle='--', label='Señal Filtrada')
        axs[0].set_title("Tiempo vs Amplitud")
        axs[0].legend()

        # Gráfico 2: Espectrograma de la señal original
        f, t, Sxx = spectrogram(signal, fs)
        axs[1].pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        axs[1].set_title("Espectrograma de Señal Original")
        axs[1].set_ylabel("Frecuencia [Hz]")

        # Gráfico 3: Espectrograma de la señal filtrada
        f, t, Sxx = spectrogram(filtered_signal, fs)
        axs[2].pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        axs[2].set_title("Espectrograma de Señal Filtrada")
        axs[2].set_xlabel("Tiempo [s]")
        axs[2].set_ylabel("Frecuencia [Hz]")

        plt.tight_layout()
        show_plot(fig)

        # Guardar la señal filtrada
        output_file = os.path.join(os.path.dirname(file), f"filtered_{os.path.basename(file)}")
        sf.write(output_file, filtered_signal, fs)
        messagebox.showinfo("Archivo Guardado", f"Audio filtrado guardado en: {output_file}")

# --- Función para mostrar gráficos en la interfaz ---
def show_plot(fig):
    for widget in frame_plot.winfo_children():
        widget.destroy()  # Limpiar el frame de gráficos
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

# --- Función para reproducir el último tono al cerrar ---
def on_closing():
    if ultimo_tono is not None:
        sd.play(ultimo_tono, samplerate=fs)
        sd.wait()
    root.destroy()

# --- Configuración de la interfaz gráfica ---
root = tk.Tk()
root.title("Procesador de Audio")

# Crear la estructura de la ventana principal
root.geometry("800x600")
root.config(bg="lightgray")

# --- Sección superior para información ---
frame_top = tk.Frame(root, bg="lightgray")
frame_top.pack(pady=20)

# Etiqueta de creadores
label_creadores = Label(frame_top, text="By Carlos Soacha, Johan Leal, Jhordy Miranda", font=("Arial", 12), bg="lightgray")
label_creadores.pack()

# --- Sección para los botones ---
frame_buttons = tk.Frame(root, bg="lightgray")
frame_buttons.pack(pady=20)

# Botón para cargar y procesar audios
button = Button(frame_buttons, text="Cargar y Procesar Audios", command=cargar_y_procesar_varios, 
                bg="orange", fg="white", font=("Arial", 14), padx=20, pady=10)
button.pack()

# --- Frame para mostrar los gráficos ---
frame_plot = tk.Frame(root, bg="white")
frame_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=20, pady=20)

# Configurar el cierre de la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la interfaz gráfica
root.mainloop()
