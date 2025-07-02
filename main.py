import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils import preprocess_audio, transcribe

selected_file_path = None  # Global to store selected file path

def upload_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("WAV files", "*.wav"), ("All files", "*.*"))
    )
    if selected_file_path:
        file_name = os.path.basename(selected_file_path)
        status_label.config(text=f"✅ File uploaded: {file_name}", fg="#007BFF")

        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.config(state='disabled')

def start_transcription():
    global selected_file_path
    if not selected_file_path:
        messagebox.showwarning("No File", "Please upload a WAV file first.")
        return
    try:
        status_label.config(text="🔄 Transcribing...", fg="#333")
        root.update()

        processed_path = preprocess_audio(selected_file_path)
        result = transcribe(processed_path)

        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result)
        result_text.config(state='disabled')

        status_label.config(text="✅ Transcription completed.", fg="green")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="❌ Failed to transcribe audio.", fg="red")

# ---- GUI SETUP ----
root = tk.Tk()
root.title("🎙️ AI Speech to Text System")
root.geometry("700x520")
root.configure(bg="#f9f9f9")

# Title
title = tk.Label(root, text="AI Speech-to-Text Generetor", font=("Segoe UI", 18, "bold"), bg="#f9f9f9", fg="#333")
title.pack(pady=(20, 10))

# Main Frame
main_frame = tk.Frame(root, bg="#f9f9f9")
main_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Upload Button
upload_btn = tk.Button(
    main_frame, text="📁 Upload WAV File", command=upload_file,
    font=("Segoe UI", 12), bg="#2196F3", fg="white",
    activebackground="#1e88e5", padx=10, pady=5, relief="flat", cursor="hand2"
)
upload_btn.pack(pady=5)

# Transcribe Button
transcribe_btn = tk.Button(
    main_frame, text="📝 Transcribe", command=start_transcription,
    font=("Segoe UI", 12), bg="#4CAF50", fg="white",
    activebackground="#45a049", padx=10, pady=5, relief="flat", cursor="hand2"
)
transcribe_btn.pack(pady=5)

# Text area for result
result_text = tk.Text(main_frame, wrap="word", height=10, font=("Segoe UI", 11), padx=10, pady=10, relief="groove", bd=1)
result_text.pack(fill="both", expand=True, padx=10, pady=10)
result_text.config(state='disabled')

# Status Label
status_label = tk.Label(root, text="", font=("Segoe UI", 10), bg="#f9f9f9", fg="blue")
status_label.pack(pady=5)

# Footer
footer = tk.Label(root, text="Designed by Samrat Singh", font=("Segoe UI", 9), bg="#f9f9f9", fg="gray")
footer.pack(side="bottom", pady=10)

root.mainloop()
