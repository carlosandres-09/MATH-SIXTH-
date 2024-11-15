import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
import scipy.io.wavfile as wav
import os

def select_audio():
    audio_path = filedialog.askopenfilename(
        title="Selecciona tu archivo de audio",
        filetypes=[("Archivos de audio", "*.mp3 *.wav")]
    )
    
    if audio_path:
        try:
            clean_audio(audio_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el audio: {e}")

def clean_audio(audio_path):
    # Convertir a WAV si el archivo es MP3, o cargarlo si es WAV
    try:
        if audio_path.endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_path)
            temp_audio_path = audio_path.replace('.mp3', '_temp.wav')
            audio.export(temp_audio_path, format='wav')
            audio_path = temp_audio_path
        elif audio_path.endswith('.wav'):
            audio = AudioSegment.from_wav(audio_path)
        else:
            raise ValueError("Formato de archivo no compatible. Usa un archivo .mp3 o .wav")
        
        # Leer el archivo WAV
        rate, data = wav.read(audio_path)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo de audio: {e}")
        return
    
    # Reducir el ruido del audio
    try:
        reduced_noise = nr.reduce_noise(y=data, sr=rate)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reducir el ruido del archivo: {e}")
        return
    
    # Seleccionar la ubicación y nombre de archivo para guardar
    output_path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("Archivo WAV", "*.wav")],
        title="Guardar audio mejorado como"
    )
    
    if output_path:
        # Guardar el audio mejorado
        wav.write(output_path, rate, reduced_noise.astype(np.int16))
        
        # Eliminar archivo temporal si fue creado
        if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        
        messagebox.showinfo("Éxito", f"El audio mejorado ha sido guardado en {output_path}")
    else:
        messagebox.showwarning("Cancelado", "No se guardó el archivo de audio mejorado.")

# Crear la ventana principal
root = tk.Tk()
root.title("Mejorador de Audio")
root.geometry("300x150")

# Crear el botón para seleccionar el audio
select_button = tk.Button(root, text="Selecciona tu audio", command=select_audio)
select_button.pack(pady=50)

# Iniciar la interfaz
root.mainloop()
