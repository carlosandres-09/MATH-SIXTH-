import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os

def select_video():
    video_path = filedialog.askopenfilename(
        title="Selecciona tu video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    
    if video_path:
        save_audio(video_path)

def save_audio(video_path):
    output_path = os.path.splitext(video_path)[0] + ".mp3"
    
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_path)
        messagebox.showinfo("Éxito", f"El audio ha sido guardado en {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Conversor de Video a MP3")
root.geometry("300x150")

# Crear el botón para seleccionar el video
select_button = tk.Button(root, text="Selecciona tu video", command=select_video)
select_button.pack(pady=50)

# Iniciar la interfaz
root.mainloop()
