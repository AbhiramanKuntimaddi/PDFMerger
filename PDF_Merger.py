import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import threading

# Global list to store selected file paths
selected_file_paths = []

def open_file_dialog():
    global selected_file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    # Update the listbox with selected file paths
    for file_path in file_paths:
        listbox.insert(tk.END, file_path)
        selected_file_paths.append(file_path)

def merge_pdfs():
    global selected_file_paths
    output_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_file_path:
        # Create a progress bar
        progress_bar = ttk.Progressbar(root, length=200, mode='indeterminate')
        progress_bar.pack(padx=10, pady=10)
        progress_bar.start()

        # Function to run the PDF merge in a separate thread
        def run_merge():
            cmd = ['gs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_file_path]
            cmd.extend(selected_file_paths)
            subprocess.run(cmd)
            # Show success message or update UI after merging
            selected_file_paths = []  # Clear selected file paths after merging
            listbox.delete(0, tk.END)  # Clear listbox
            progress_bar.stop()  # Stop progress bar
            progress_bar.destroy()  # Destroy progress bar widget

        # Start PDF merge in a separate thread
        t = threading.Thread(target=run_merge)
        t.start()

def clear_selection():
    global selected_file_paths
    selected_file_paths = []  # Clear selected file paths
    listbox.delete(0, tk.END)  # Clear listbox

# Create main window
root = tk.Tk()
root.title("PDF Merger")

# Create UI elements
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.pack(padx=10, pady=10)

merge_button = tk.Button(root, text="Merge PDFs", command=merge_pdfs)
merge_button.pack(padx=10, pady=10)

clear_button = tk.Button(root, text="Clear Selection", command=clear_selection)
clear_button.pack(padx=10, pady=10)

add_button = tk.Button(root, text="Add PDFs", command=open_file_dialog)
add_button.pack(padx=10, pady=10)

root.mainloop()
