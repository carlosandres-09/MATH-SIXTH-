import tkinter as tk
from tkinter import filedialog
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from scipy.io.wavfile import write
import sounddevice as sd

# Función para cargar y analizar múltiples audios ecualizados
def cargar_audios_ecualizados():
    filepaths = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.wav")])
    if filepaths:
        for filepath in filepaths:
            audio, sr = librosa.load(filepath)
            analizar_audio(audio, sr, filepath.split("/")[-1])
            play_audio(audio, sr)

# Función para cargar y analizar múltiples audios sin ecualizar
def cargar_audios_sin_ecualizar():
    filepaths = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.wav")])
    if filepaths:
        for filepath in filepaths:
            audio, sr = librosa.load(filepath)
            analizar_audio(audio, sr, filepath.split("/")[-1])
            play_audio(audio, sr)

# Función para cargar y analizar tonos puros
def cargar_tonos_puros():
    generar_tonos()

# Función para analizar y graficar el audio
def analizar_audio(audio, sr, title):
    plt.figure(figsize=(12, 8))

    # Tiempo vs Amplitud
    plt.subplot(3, 1, 1)
    plt.plot(np.linspace(0, len(audio) / sr, len(audio)), audio)
    plt.title(f'Tiempo vs Amplitud - {title}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')

    # Espectrograma
    plt.subplot(3, 1, 2)
    plt.specgram(audio, Fs=sr, NFFT=1024, noverlap=512)
    plt.title(f'Espectrograma - {title}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')

    # Amplitud vs Frecuencia
    freqs = np.fft.fftfreq(len(audio), d=1/sr)
    fft_audio = np.fft.fft(audio)
    amplitud = np.abs(fft_audio)

    plt.subplot(3, 1, 3)
    plt.plot(freqs[:len(freqs)//2], amplitud[:len(amplitud)//2])  # Solo la parte positiva del espectro
    plt.title(f'Amplitud vs Frecuencia - {title}')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Amplitud')
    
    plt.tight_layout()
    plt.show()

# Función para reproducir el audio
def play_audio(audio, samplerate):
    sd.play(audio, samplerate)
    sd.wait()

# Función para generar tonos puros de cuerdas
def generar_tonos():
    frecuencias = {'4ta cuerda': 146.832, '5ta cuerda': 110, '6ta cuerda': 82.407}
    duracion = 2
    sr = 44100

    for nombre, freq in frecuencias.items():
        tono = generar_tono(freq, duracion, sr)
        analizar_audio(tono, sr, f'{nombre} (Tono Puro - {freq} Hz)')
        play_audio(tono, sr)
        save_audio(f"Tono_Puro_{nombre.replace(' ', '_')}.wav", tono, sr)

# Función para generar un tono puro
def generar_tono(frequency, duration, samplerate):
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    return tone

# Función para guardar el audio generado
def save_audio(filename, audio, samplerate):
    write(filename, samplerate, np.int16(audio * 32767))

# Función para aislar la cuerda de guitarra
def aislar_cuerda(audio_file):
    print("Cargando archivo de audio...")
    audio, sr = librosa.load(audio_file, sr=None)
    
    print("Calculando espectrograma...")
    stft = librosa.stft(audio)
    spectrogram = np.abs(stft)
    
    print("Identificando armónicos...")
    peaks, _ = signal.find_peaks(spectrogram.sum(axis=0))
    
    print("Eliminando armónicos...")
    for peak in peaks:
        spectrogram[:, peak] = 0
    
    print("Reconstruyendo audio...")
    audio_filtrado = librosa.istft(spectrogram)
    
    analizar_audio(audio, sr, "Original")
    analizar_audio(audio_filtrado, sr, "Filtrado")
    play_audio(audio_filtrado, sr)

# Función para cargar y aislar cuerdas de guitarra
def cargar_y_aislar_cuerda():
    filepaths = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.wav")])
    if filepaths:
        for filepath in filepaths:
            aislar_cuerda(filepath)

# Función para crear la interfaz gráfica
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Análisis y Generación de Tonos Puros")

    # Ajuste del tamaño y estilo de la ventana principal
    ventana.geometry("500x500")
    ventana.config(bg="#f0f0f0")

    # Título de la ventana
    titulo = tk.Label(ventana, text="Procesamiento de Audio", font=("Arial", 20, "bold"), bg="#f0f0f0")
    titulo.pack(pady=20)

    # Botón para cargar audios ecualizados
    btn_cargar_ecualizados = tk.Button(ventana, text="Cargar Audios Ecualizados", font=("Arial", 14),
                                        command=cargar_audios_ecualizados, width=30, height=2, bg="#4CAF50", fg="white", relief="raised")
    btn_cargar_ecualizados.pack(pady=10)

    # Botón para cargar audios sin ecualizar
    btn_cargar_sin_ecualizar = tk.Button(ventana, text="Cargar Audios Sin Ecualizar", font=("Arial", 14),
                                          command=cargar_audios_sin_ecualizar, width=30, height=2, bg="#4CAF50", fg="white", relief="raised")
    btn_cargar_sin_ecualizar.pack(pady=10)

    # Botón para cargar tonos puros
    btn_cargar_tonos_puros = tk.Button(ventana, text="Cargar Tonos Puros", font=("Arial", 14),
                                        command=cargar_tonos_puros, width=30, height=2, bg="#4CAF50", fg="white", relief="raised")
    btn_cargar_tonos_puros.pack(pady=10)

    # Botón para aislar cuerdas de guitarra
    btn_aislar_cuerda = tk.Button(ventana, text="Aislar Cuerda de Guitarra", font=("Arial", 14),
                                  command=cargar_y_aislar_cuerda, width=30, height=2, bg="#4CAF50", fg="white", relief="raised")
    btn_aislar_cuerda.pack(pady=10)

    # Referencia a los creadores en la esquina inferior derecha
    referencia = tk.Label(ventana, text="By Carlos Soacha, Johan Leal, Jhordy Miranda",
                          font=("Arial", 10, "italic"), bg="#f0f0f0", anchor='e')
    referencia.pack(side="bottom", padx=10, pady=10)

    ventana.mainloop()

# Ejecutar la interfaz
crear_interfaz()
