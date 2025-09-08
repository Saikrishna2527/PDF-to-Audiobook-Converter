import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import pyttsx3
import threading
import os
import time

# ----- PDF Text Extraction -----
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text_content = []
    for page in doc:
        txt = page.get_text()
        if txt.strip():
            text_content.append(txt)
    return "\n".join(text_content)

def clean_text(text):
    return " ".join(text.split())

# ----- Text-to-Speech -----
def text_to_speech_pyttsx3(text, volume=1.0, rate=150, output_filename="output.wav"):
    engine = pyttsx3.init()
    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)
    engine.save_to_file(text, output_filename)
    engine.runAndWait()

# ----- Tkinter GUI -----
class PDFtoAudioApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF to Audiobook Converter")

        self.pdf_path = ""
        self.text_content = ""

        # File selection
        self.upload_btn = tk.Button(root, text="Upload PDF", command=self.upload_file)
        self.upload_btn.pack(pady=10)

        self.file_label = tk.Label(root, text="No file selected.")
        self.file_label.pack()

        # Volume slider
        self.volume = tk.DoubleVar(value=1.0)
        self.volume_slider = tk.Scale(root, variable=self.volume, from_=0, to=1, resolution=0.1, label="Volume", orient=tk.HORIZONTAL)
        self.volume_slider.pack()

        # Speed slider
        self.rate = tk.IntVar(value=150)
        self.rate_slider = tk.Scale(root, variable=self.rate, from_=50, to=300, label="Speed", orient=tk.HORIZONTAL)
        self.rate_slider.pack()

        # Convert and Play/Export buttons
        self.convert_btn = tk.Button(root, text="Convert to Audio", command=self.start_conversion)
        self.convert_btn.pack(pady=8)

        self.play_btn = tk.Button(root, text="Play", state=tk.DISABLED, command=self.play_audio)
        self.play_btn.pack(pady=4)

        self.export_btn = tk.Button(root, text="Export WAV", state=tk.DISABLED, command=self.export_audio)
        self.export_btn.pack(pady=4)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def upload_file(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            self.pdf_path = pdf_path
            self.file_label.config(text=os.path.basename(pdf_path))
            self.status_label.config(text="Extracting text...")
            self.root.update()
            text = extract_pdf_text(pdf_path)
            if not text.strip():
                messagebox.showerror("Error", "The selected PDF has no extractable text.")
                self.status_label.config(text="Extraction failed.")
                self.text_content = ""
                self.play_btn.config(state=tk.DISABLED)
                self.export_btn.config(state=tk.DISABLED)
            else:
                self.text_content = clean_text(text)
                self.status_label.config(text="Text extracted successfully.")
                self.play_btn.config(state=tk.NORMAL)
                self.export_btn.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="No file selected.")

    def start_conversion(self):
        if not self.text_content:
            messagebox.showwarning("No Text", "Nothing to convert.")
            return
        self.status_label.config(text="Converting to audio...")
        self.root.update()
        threading.Thread(target=self.convert_and_notify).start()

    def convert_and_notify(self):
        try:
            output_wav = "output.wav"
            text_to_speech_pyttsx3(
                self.text_content,
                volume=self.volume.get(),
                rate=self.rate.get(),
                output_filename=output_wav
            )
            # Ensure file is saved before next steps
            time.sleep(1)
            self.status_label.config(text="Conversion complete! Ready to play or export.")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def play_audio(self):
        try:
            self.status_label.config(text="Playing audio...")
            self.root.update()
            # Use os.startfile for Windows
            wav_path = os.path.abspath("output.wav")
            if os.name == "nt":  # Windows
                os.startfile(wav_path)
            else:  # Other platforms (Linux/Mac)
                import subprocess
                subprocess.call(["open", wav_path])  # For MacOS
                # For Linux you may use: subprocess.call(["aplay", wav_path])
            self.status_label.config(text="Playback initiated.")
        except Exception as e:
            self.status_label.config(text=f"Playback failed: {e}")

    def export_audio(self):
        dst = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if dst:
            try:
                import shutil
                shutil.copyfile("output.wav", dst)
                self.status_label.config(text=f"Exported as {os.path.basename(dst)}")
            except Exception as e:
                self.status_label.config(text=f"Export failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFtoAudioApp(root)
    root.mainloop()
