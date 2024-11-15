import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from scipy.signal import butter, filtfilt
import sounddevice as sd
import soundfile as sf
from scipy.fft import fft, ifft, fftfreq
import os
from tkinter import Tk, Button, Label, filedialog

# Definir el filtro pasa-bajos
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Función para cargar y procesar varios audios
def cargar_y_procesar_varios():
    files = filedialog.askopenfilenames(title="Selecciona archivos de audio", 
                                        filetypes=[("Archivos de Audio", ".wav;.mp3;.ogg;.flac")])
    if not files:
        print("No se seleccionó ningún archivo.")
        return

    for file in files:
        # Cargar el audio
        signal, fs = librosa.load(file, sr=None)

        # Reproducir el sonido original
        print(f"Reproduciendo el sonido original: {file}")
        sd.play(signal, samplerate=fs)
        sd.wait()

        # Realizar la FFT y encontrar la frecuencia fundamental
        Y = fft(signal)
        freqs = fftfreq(len(Y), 1 / fs)
        magnitude = np.abs(Y)
        fundamental_frequency = freqs[np.argmax(magnitude)]
        print(f"Frecuencia fundamental detectada para {file}: {fundamental_frequency:.2f} Hz")

        # Crear un filtro que conserve frecuencias cercanas a la fundamental
        filtered_spectrum = np.zeros_like(Y)
        frequency_bandwidth = 100
        for i in range(len(freqs)):
            if abs(freqs[i] - fundamental_frequency) < frequency_bandwidth:
                filtered_spectrum[i] = Y[i]

        # Reconstruir el sonido a partir del espectro filtrado
        reconstructed_signal = ifft(filtered_spectrum).real

        # Crear el tono puro
        duration = len(signal) / fs
        t = np.linspace(0, duration, len(signal), endpoint=False)
        tone_pure = np.sin(2 * np.pi * fundamental_frequency * t)

        # Reproducir el tono puro
        print(f"Reproduciendo el tono puro para {file}...")
        sd.play(tone_pure, samplerate=fs)
        sd.wait()

        # Reproducir el sonido reconstruido
        print(f"Reproduciendo el sonido reconstruido (resultado de la IFFT) para {file}...")
        sd.play(reconstructed_signal, samplerate=fs)
        sd.wait()

        # Aplicar el filtro pasa-bajos
        cutoff = 300
        order = 4
        b, a = butter_lowpass(cutoff, fs, order)
        filtered_signal = filtfilt(b, a, signal)

        # Aumentar el volumen de la señal filtrada
        filtered_signal = np.clip(filtered_signal, -1.0, 1.0)

        # Gráficos
        plt.figure(figsize=(14, 10))

        plt.subplot(3, 2, 1)
        plt.plot(signal, color='blue', label='Señal Original')
        plt.plot(filtered_signal, color='orange', label='Señal Filtrada', linestyle='--')
        plt.title(f'Señal Original y Filtrada: {file}')
        plt.xlabel('Muestra')
        plt.ylabel('Amplitud')
        plt.legend()

        # Espectrogramas
        D_original = librosa.amplitude_to_db(np.abs(librosa.stft(signal)), ref=np.max)
        D_filtered = librosa.amplitude_to_db(np.abs(librosa.stft(filtered_signal)), ref=np.max)

        plt.subplot(3, 2, 4)
        librosa.display.specshow(D_original, sr=fs, x_axis='time', y_axis='log', cmap='plasma')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Espectrograma Señal Original')

        plt.subplot(3, 2, 5)
        librosa.display.specshow(D_filtered, sr=fs, x_axis='time', y_axis='log', cmap='plasma')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Espectrograma Señal Filtrada')

        plt.tight_layout()
        plt.show()

        # Guardar el audio filtrado
        output_file = os.path.join(os.path.dirname(file), f"filtered_{os.path.basename(file)}")
        sf.write(output_file, filtered_signal, fs)
        print(f"Audio filtrado guardado en: {output_file}")

# Crear la ventana principal y el botón
root = Tk()
root.title("Procesador de Audio")

# Crear un label para los creadores
label_creadores = Label(root, text="By Carlos Soacha, Johan Leal, Jhordy Miranda", font=("Arial", 12))
label_creadores.pack(pady=10)

# Crear el botón con mayor tamaño, color naranja y un padding adecuado
button = Button(root, text="Cargar y Procesar Varios Audios", command=cargar_y_procesar_varios, 
                bg="orange", fg="white", font=("Arial", 14), padx=20, pady=10)
button.pack(pady=20)

# Ejecutar la ventana
root.geometry("400x200")  # Ajustar el tamaño de la ventana
root.mainloop()
