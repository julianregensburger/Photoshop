import numpy
from PIL import Image
from tkinter import filedialog

def upload_file():
    dateipfad = filedialog.askopenfilename(
        title="Wähle eine Datei zum bearbeiten aus",
        initialdir="/", # Startverzeichnis
        filetypes=(("Bild Datei", "*.jpeg"), ("Alle Dateien", "*.*")) # Filter
    )

def export_file():
    pass

def new_file():
    pass

def zoom():
    pass

def back():
    pass

def forward():
    pass

def save():
    pass

def frame_change(window):
    pass
