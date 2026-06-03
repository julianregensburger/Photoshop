import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import numpy as np
import time
import os
import sys

img_edit_raw = None
img_edit_display = None
img_edit = None
img_ori = None
image_lbl = None
undo_stack = []
redo_stack = []
loaded = False
draw_colors = [0,0,0]
brush_size = 1
updating_sliders = False
channel_dragging = False
last_save = time.time()
last_change = time.time()
save_path = None
zoom_enabled = False
points = []

# Modernes Design
BG_DARK = "#151821"
BG_PANEL = "#1f2430"
BG_CARD = "#2a3040"
BG_EDITOR = "#10131a"
BG_INPUT = "#343b4f"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#9b83ff"
TEXT = "#f5f7fb"
TEXT_MUTED = "#aab1c5"
BORDER = "#3d465c"

FONT_NORMAL = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 25, "bold")
FONT_SMALL = ("Segoe UI", 10)

def modern_frame(parent, **kwargs):
    kwargs.setdefault("bg", BG_PANEL)
    kwargs.setdefault("highlightthickness", 0)
    return tk.Frame(parent, **kwargs)

def modern_label(parent, **kwargs):
    kwargs.setdefault("bg", BG_PANEL)
    kwargs.setdefault("fg", TEXT)
    kwargs.setdefault("font", FONT_NORMAL)
    kwargs.setdefault("bd", 0)
    return tk.Label(parent, **kwargs)

def modern_button(parent, **kwargs):
    kwargs.setdefault("bg", BG_CARD)
    kwargs.setdefault("fg", TEXT)
    kwargs.setdefault("activebackground", ACCENT)
    kwargs.setdefault("activeforeground", "#ffffff")
    kwargs.setdefault("font", FONT_BOLD)
    kwargs.setdefault("bd", 0)
    kwargs.setdefault("relief", "flat")
    kwargs.setdefault("cursor", "hand2")
    kwargs.setdefault("highlightthickness", 0)
    return tk.Button(parent, **kwargs)

def modern_scale(parent, **kwargs):
    kwargs.setdefault("bg", BG_PANEL)
    kwargs.setdefault("fg", TEXT)
    kwargs.setdefault("activebackground", ACCENT)
    kwargs.setdefault("troughcolor", BG_INPUT)
    kwargs.setdefault("highlightthickness", 0)
    kwargs.setdefault("bd", 0)
    kwargs.setdefault("relief", "flat")
    kwargs.setdefault("font", FONT_SMALL)
    return tk.Scale(parent, **kwargs)


def upload_file():
    """
    Öffnet einen Dateidialog zum Laden eines Bildes.

    Funktion:
    - Lässt den Nutzer ein Bild (PNG/JPG) auswählen.
    - Lädt das Bild in voller Auflösung für den Editor und verkleinert für die Original-Ansicht.
    - Bindet Maus-Events (Zeichnen, Zoom) an das Editor-Label.
    - Setzt den globalen Status auf geladen ('loaded = True').

    Parameter:
        Keine

    Rückgabewert:
        Keiner (None) - Modifiziert globale Variablen (img_ori, img_edit_raw, etc.).
    """
    global img_ori, img_edit, img_edit_raw, image_lbl, img_edit_display, loaded, last_img, last_change

    last_change = time.time()

    dateipfad = filedialog.askopenfilename(
        title="Wähle eine Datei zum bearbeiten aus",
        initialdir="/home/julian/Dokumente/Dokumente/FSST/Software/Korber/Photoshop", # Startverzeichnis
        filetypes=[("PNG-Bild", "*.png"), ("JPEG-Bild", "*.jpg"), ("Alle Dateien", "*.*")] # Filter
    )
    #Bild anzeigen im editor frame
    img_edit, img_edit_raw = load_image(size=(3200,2100),img_path=dateipfad)
    image_lbl = modern_label(frame_editor, image=img_edit)
    image_lbl.bind("<Button-1>", draw)
    image_lbl.bind("<B1-Motion>",draw)
    image_lbl.bind("<Button-1>", zoom)
    image_lbl.place(x=0,y=0)
    img_edit_display = img_edit_raw.copy()
    save_history()


    #Bild anzeigen im original frame
    img_ori,_ = load_image(size=(800,700),img_path=dateipfad)
    image_lbl_ori = modern_label(frame_ori, image=img_ori)
    image_lbl_ori.place(x=0,y=0)
    image_lbl_ori.lift()

    #Setze geladen variable auf True dass alle Funktionen es wissen
    loaded = True

def show(img):
    """
    Aktualisiert die Bildanzeige im Tkinter-Editor-Fenster.

    Funktion:
    - Konvertiert das übergebene NumPy-Array in ein Tkinter-kompatibles Bildformat.
    - Aktualisiert das bestehende 'image_lbl' im GUI, um Änderungen sofort sichtbar zu machen.

    Parameter:
        img (numpy.ndarray): Das anzuzeigende Bild-Array.

    Rückgabewert:
        Keiner (None)
    """
    global img_edit
    last_change = time.time()
    img_edit = load_image(img_array=img)
    image_lbl.config(image=img_edit)

def change_channel(value, channel):
    """
    Manipuliert die Intensität eines einzelnen Farbkanals (R, G oder B).

    Funktion:
    - Multipliziert den gewählten Kanal des Originalbildes mit dem Faktor des Sliders.
    - Begrenzt die Pixelwerte auf das Intervall [0, 255].
    - Aktualisiert die Live-Vorschau im GUI über die show()-Funktion.

    Parameter:
        value (str/int): Der aktuelle Wert des Sliders (wird durch 100 geteilt).
        channel (int): Der Index des Farbkanals (0 = Rot, 1 = Grün, 2 = Blau).

    Rückgabewert:
        Keiner (None)
    """
    global img_edit_raw, img_edit_display, loaded, updating_sliders

    if updating_sliders:
        return

    if loaded:
        value = int(value) / 100

        img_edit_display = img_edit_raw.copy()
        img_edit_display[:, :, int(channel)] = img_edit_raw[:, :, int(channel)] * value
        img_edit_display = np.clip(img_edit_display, 0, 255).astype(np.uint8)

        show(img_edit_display)

def save_channel(event):
    """
    Speichert die aktuelle Kanaländerung dauerhaft im Bearbeitungsbild.

    Funktion:
    - Übernimmt die Live-Vorschau der Kanaländerung in das echte Bearbeitungsbild.
    - Wird beim Loslassen eines RGB-Sliders ausgeführt.
    - Beendet den Status, dass gerade ein Kanal-Slider bewegt wird.

    Parameter:
        event (tkinter.Event): Das Event, das beim Loslassen des Sliders ausgelöst wird.

    Rückgabewert:
        Keiner (None)
    """
    global img_edit_raw, img_edit_display, channel_dragging

    if loaded and img_edit_display is not None:
        img_edit_raw = img_edit_display.copy()

    channel_dragging = False

# Modernes Design
BG_DARK = "#151821"
BG_PANEL = "#1f2430"
BG_CARD = "#2a3040"
BG_EDITOR = "#10131a"
BG_INPUT = "#343b4f"
ACCENT = "#7c5cff"
ACCENT_HOVER = "#9b83ff"
TEXT = "#f5f7fb"
TEXT_MUTED = "#aab1c5"
BORDER = "#3d465c"

FONT_NORMAL = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 25, "bold")
FONT_SMALL = ("Segoe UI", 10)

def modern_frame(parent, **kwargs):
    kwargs.setdefault("bg", BG_PANEL)
    kwargs.setdefault("highlightthickness", 0)
    return tk.Frame(parent, **kwargs)

def modern_label(parent, **kwargs):
    kwargs.setdefault("bg", BG_PANEL)
    kwargs.setdefault("fg", TEXT)
    kwargs.setdefault("font", FONT_NORMAL)
    kwargs.setdefault("bd", 0)
    return tk.Label(parent, **kwargs)

def modern_button(parent, **kwargs):
    kwargs.setdefault("bg", BG_CARD)
    kwargs.setdefault("fg", TEXT)
    kwargs.setdefault("activebackground", ACCENT)
    kwargs.setdefault("activeforeground", "#ffffff")
    kwargs.setdefault("font", FONT_BOLD)
    kwargs.setdefault("bd", 0)
    kwargs.setdefault("relief", "flat")
    kwargs.setdefault("cursor", "hand2")
    kwargs.setdefault("highlightthickness", 0)
    return tk.Button(parent, **kwargs)

def modern_scale(parent, **kwargs):
    kwargs.setdefault("bg", BG_PANEL)
    kwargs.setdefault("fg", TEXT)
    kwargs.setdefault("activebackground", ACCENT)
    kwargs.setdefault("troughcolor", BG_INPUT)
    kwargs.setdefault("highlightthickness", 0)
    kwargs.setdefault("bd", 0)
    kwargs.setdefault("relief", "flat")
    kwargs.setdefault("font", FONT_SMALL)
    return tk.Scale(parent, **kwargs)


def save_start_channel(event):
    """
    Speichert den aktuellen Bildzustand vor einer Kanaländerung in der History.

    Funktion:
    - Wird beim Anklicken eines RGB-Sliders ausgeführt.
    - Speichert den aktuellen Zustand nur einmal pro Slider-Bewegung.
    - Aktiviert den Status, dass gerade ein Kanal bearbeitet wird.

    Parameter:
        event (tkinter.Event): Das Event, das beim Drücken auf den Slider ausgelöst wird.

    Rückgabewert:
        Keiner (None)
    """
    global channel_dragging, loaded

    if loaded and not channel_dragging:
        save_history()
        channel_dragging = True
    
def export_file():
    """
    Speichert das bearbeitete Bild auf der Festplatte.

    Funktion:
    - Fragt beim ersten Speichern über einen Dialog nach dem Zielpfad.
    - Konvertiert das aktuelle NumPy-Array zurück in ein PIL-Image und speichert es.
    - Überschreibt die Datei direkt, falls bereits ein Pfad existiert.

    Parameter:
        Keine

    Rückgabewert:
        Keiner (None)
    """
    global img_edit_raw, last_save, save_path, loaded
    if loaded:    
        if save_path is None:
            save_path = filedialog.asksaveasfilename(
                title="Bild speichern unter...",
                defaultextension=".png",
                filetypes=[("PNG-Bild", "*.png"), ("JPEG-Bild", "*.jpg"), ("Alle Dateien", "*.*")]
            )

            if save_path:
                last_save = time.time()
                img = Image.fromarray(img_edit_raw)
                img.save(save_path)
        else:
            save()
    

def new_file():
    """
    Schließt das aktuelle Projekt und startet die Anwendung sauber neu.

    Funktion:
    - Prüft auf ungespeicherte Änderungen und öffnet ggf. eine Ja/Nein-Abfrage zum Speichern.
    - Schließt das aktuelle Tkinter-Fenster.
    - Startet das Skript im exakten virtuellen Environment (venv) komplett neu.

    Parameter:
        Keine

    Rückgabewert:
        Keiner (None) - Beendet den aktuellen Python-Prozess.
    """
    global last_save, last_change, root, loaded
    if loaded:
        if (last_save - last_change) < 0:
            answer = messagebox.askyesno("Schließen ohne speichern", "Möchten Sie die Datei vorher speichern?")
            if answer:
                export_file()
        root.destroy()
        python_pfad = "/home/julian/venvs/fsst/bin/python"
        skript_pfad = (
            "/home/julian/Dokumente/Dokumente/FSST/Software/Korber/Photoshop/photoshop.py"
        )
        # Prozess mit der genauen venv-Python-Umgebung neu starten
        os.execv(python_pfad, [python_pfad, skript_pfad] + sys.argv[1:])


def switch_zoom():
    global zoom_enabled
    if zoom_enabled:
        zoom_enabled = False
    else:
        zoom_enabled = True

def zoom(event):
    """
    Führt das Zuschneiden (Slicing) des Bildes basierend auf zwei Klicks aus.

    Funktion:
    - Berechnet die relativen Pixelkoordinaten auf dem echten Bild anhand der Klickposition im Widget.
    - Sammelt Punkte. Sobald zwei Punkte vorliegen, wird die History gesichert.
    - Schneidet das NumPy-Array auf das gewählte Rechteck zu und aktualisiert die Anzeige.

    Parameter:
        event (tkinter.Event): Das Maus-Klick-Event, das X- und Y-Koordinaten liefert.

    Rückgabewert:
        Keiner (None)
    """
    global zoom_enabled, img_edit_raw, points
    if zoom_enabled:
        widget_w = event.widget.winfo_width()
        widget_h = event.widget.winfo_height()

        img_h, img_w = img_edit_raw.shape[:2]

        x = int(event.x * img_w / widget_w)
        y = int(event.y * img_h / widget_h)
        
        points.append([x,y])

        if len(points) == 2:
            save_history()

            x_max, x_min, y_max, y_min, points = calculate_rectangle(points)

            img_edit_raw = img_edit_raw[y_min : y_max + 1, x_min : x_max + 1]

            show(img=img_edit_raw)

def calculate_rectangle(points):
    """
    Berechnet die minimalen und maximalen Grenzen aus zwei diagonalen Punkten.

    Funktion:
    - Ermittelt die Extremwerte (Min/Max) für X und Y, um ein achsenparalleles Rechteck aufzuspannen.
    - Leert die temporäre Punkteliste für den nächsten Zoom-Vorgang.

    Parameter:
        points (list): Eine Liste, die zwei Koordinaten-Paare [[x1, y1], [x2, y2]] enthält.

    Rückgabewert:
        tuple: (x_max, x_min, y_max, y_min, points)
               Die Koordinatengrenzen als Integer und eine leere Liste zum Zurücksetzen.
    """
    x1, y1 = points[0]
    x2, y2 = points[1]
    
    # Eckpunkte ermitteln
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    points = []

    return x_max, x_min, y_max, y_min, points       

def invert_x():
    global img_edit_raw
    save_history()
    img_edit_raw = img_edit_raw[::-1,:]
    show(img=img_edit_raw)

def invert_y():
    global img_edit_raw
    save_history()
    img_edit_raw = img_edit_raw[:,::-1]
    show(img=img_edit_raw)

def invert_color():
    global img_edit_raw
    save_history()
    for i in range(3):
        img_edit_raw[:,:,i] = 255 - img_edit_raw[:,:,i]
    show(img=img_edit_raw)

def white_black():
    global img_edit_raw
    save_history()
    img_edit_raw = np.mean(img_edit_raw[..., :3], axis=2).astype(np.uint8)
    img_edit_raw = np.stack([img_edit_raw, img_edit_raw, img_edit_raw], axis=-1)
    show(img=img_edit_raw)

def back():
    """
    Macht die letzte Bildänderung rückgängig.

    Funktion:
    - Prüft, ob ein Bild geladen ist und ob Einträge im Undo-Stack vorhanden sind.
    - Speichert den aktuellen Zustand im Redo-Stack.
    - Lädt den letzten gespeicherten Zustand aus dem Undo-Stack.
    - Stellt auch die RGB-Slider-Werte wieder her.
    - Aktualisiert anschließend die Anzeige im Editor.

    Parameter:
        Keine

    Rückgabewert:
        Keiner (None)
    """
    global img_edit_raw, img_edit_display, undo_stack, redo_stack, loaded, last_channel, r_channel, g_channel, b_channel, aktiv_frame

    if loaded and len(undo_stack) > 0:
        redo_stack.append({
            "img": img_edit_raw.copy(),
            "channels": [r_channel.get(),g_channel.get(),b_channel.get()]
        })

        state = undo_stack.pop()

        img_edit_raw = state["img"].copy()
        img_edit_display = img_edit_raw.copy()

        updating_sliders = True
        r_channel.set(state["channels"][0])
        g_channel.set(state["channels"][1])
        b_channel.set(state["channels"][2])
        updating_sliders = False

        show(img_edit_raw)

def save_history():
    global undo_stack, redo_stack, img_edit_raw, r_channel, g_channel, b_channel

    if img_edit_raw is not None:
        undo_stack.append({
            "img": img_edit_raw.copy(),
            "channels": [r_channel.get(),g_channel.get(),b_channel.get()]
        })
        redo_stack.clear()

def forward():
    """
    Stellt eine zuvor rückgängig gemachte Änderung wieder her.

    Funktion:
    - Prüft, ob ein Bild geladen ist und ob Einträge im Redo-Stack vorhanden sind.
    - Speichert den aktuellen Zustand im Undo-Stack.
    - Lädt den letzten Zustand aus dem Redo-Stack.
    - Stellt auch die RGB-Slider-Werte wieder her.
    - Aktualisiert anschließend die Anzeige im Editor.

    Parameter:
        Keine

    Rückgabewert:
        Keiner (None)
    """
    global img_edit_raw, undo_stack, redo_stack, loaded, r_channel, g_channel, b_channel

    if loaded and len(redo_stack) > 0:
        undo_stack.append({
            "img": img_edit_raw.copy(),
            "channels": [r_channel.get(),g_channel.get(),b_channel.get()]
        })

        state = redo_stack.pop()

        img_edit_raw = state["img"].copy()
        img_edit_display = img_edit_raw.copy()
        show(img_edit_raw)

        updating_sliders = True
        r_channel.set(state["channels"][0])
        g_channel.set(state["channels"][1])
        b_channel.set(state["channels"][2])
        updating_sliders = False


def save():
    global save_path, img_edit_raw, loaded
    if loaded:   
        if save_path:
            last_save = time.time()
            img = Image.fromarray(img_edit_raw)
            img.save(save_path)
        else:
            messagebox.showwarning("Fehlender Pfad", "Sie müssen die Datei zuerst exportiern und eine Pfad auswählen!")
    

def change_colors(value, channel):
    global draw_colors
    draw_colors[int(channel)] = int(value)

def draw_circle(img, x, y):
    """
    Zeichnet einen gefüllten Kreis auf das Bild.

    Funktion:
    - Berechnet eine kreisförmige Maske um die angegebene Position.
    - Färbt alle Pixel innerhalb des Kreises mit der aktuellen Pinselfarbe.
    - Nutzt die globale Pinselgröße als Radius.

    Parameter:
        img (numpy.ndarray): Das Bild, auf dem gezeichnet wird.
        x (int): Die X-Koordinate des Kreismittelpunkts.
        y (int): Die Y-Koordinate des Kreismittelpunkts.

    Rückgabewert:
        numpy.ndarray: Das bearbeitete Bildarray.
    """
    global draw_colors, brush_size
    h, w = img.shape[:2]

    yy, xx = np.ogrid[:h, :w]

    mask = (xx - x) ** 2 + (yy - y) ** 2 <= brush_size ** 2

    img[mask] = draw_colors
    return img

def draw(event):
    """
    Zeichnet mit dem aktuellen Pinsel auf das Bild.

    Funktion:
    - Prüft, ob der Zeichenmodus aktiv ist.
    - Rechnet die Mausposition im Widget auf die echten Bildkoordinaten um.
    - Zeichnet an dieser Position einen Kreis mit der aktuellen Pinselfarbe und Pinselgröße.
    - Aktualisiert anschließend die Anzeige im Editor.

    Parameter:
        event (tkinter.Event): Das Maus-Event mit X- und Y-Koordinaten.

    Rückgabewert:
        Keiner (None)
    """
    global img_edit_raw, aktiv_frame
    if aktiv_frame.get() == "draw":

        widget_w = event.widget.winfo_width()
        widget_h = event.widget.winfo_height()

        img_h, img_w = img_edit_raw.shape[:2]

        x = int(event.x * img_w / widget_w)
        y = int(event.y * img_h / widget_h)

        if 0 <= x < img_w and 0 <= y < img_h:
            img_edit_raw[y, x] = [0, 0, 0]

        img_edit_raw = draw_circle(img_edit_raw, x, y)

        show(img=img_edit_raw)

def change_brush_size(value):
    global brush_size
    brush_size = int(value)

def setup_gui(root):
    """
    Konfiguriert das Hauptfenster und erstellt die 4 Haupt Frames und die 6 Neben Frames vom Menu.

    Parameter:
        root (tk.Tk): Das Hauptfenster der Anwendung.
    Rückgabewert:
        tuple: (frame1, frame2, frame3, frame4)
    """
    global frame_ori, frame_menu, frame_editor, frame_top_menu, frame_channel, frame_draw, frame_delete, frame_insert, frame_edit, frame_grey, aktiv_frame

    root.title("NumPy Bildverarbeitung")
    root.geometry("4000x2000")
    root.configure(bg=BG_DARK)

    #4 Haupt Frames erstellen
    frame_ori = modern_frame(root, width=800, height=700, bg=BG_EDITOR)
    frame_ori.place(x=0,y=0)

    frame_menu = modern_frame(root, width=800, height=1600, bg=BG_PANEL)
    frame_menu.place(x=0,y=700)
    aktiv_frame = tk.StringVar(value="menu")
 
    frame_editor = modern_frame(root,width=3200, height=2100, bg=BG_EDITOR)
    frame_editor.place(x=800,y=150)

    frame_top_menu = modern_frame(root, width=3200, height=150, bg=BG_DARK)
    frame_top_menu.place(x=800,y=0)

    #6 Neben Frames im Menu erstellen
    frame_channel = modern_frame(root, width=800, height=1600, bg=BG_PANEL)
    frame_draw = modern_frame(root, width=800, height=1600, bg=BG_PANEL)
    frame_delete = modern_frame(root, width=800, height=1600, bg=BG_PANEL)
    frame_insert = modern_frame(root, width=800, height=1600, bg=BG_PANEL)
    frame_edit = modern_frame(root, width=800, height=1600, bg=BG_PANEL)
    frame_grey= modern_frame(root, width=800, height=1600, bg=BG_PANEL)

def frame_change(window):
    """
    Wechselt zwischen den verschiedenen Menü-Frames der Anwendung.

    Funktion:
    - Blendet je nach Auswahl den passenden Menübereich ein.
    - Hebt den aktiven Frame nach vorne.
    - Setzt die Variable aktiv_frame auf den aktuellen Bereich.
    - Ermöglicht den Wechsel zwischen Home, Kanal, Zeichnen, Löschen, Einfügen, Ändern und Graustufen.

    Parameter:
        window (str): Der Name des Frames, zu dem gewechselt werden soll.

    Rückgabewert:
        Keiner (None)
    """
    global aktiv_frame
    match window:
        case "channel":
            frame_menu.place_forget()
            frame_channel.place(x=0,y=700)
            frame_channel.lift()
            menu_btn.lift()
            aktiv_frame.set("channel")
        case "draw":
            frame_draw.place_forget()
            frame_draw.place(x=0,y=700)
            frame_draw.lift()
            menu_btn.lift()
            aktiv_frame.set("draw")
        case "delete":
            frame_delete.place_forget()
            frame_delete.place(x=0,y=700)
            frame_delete.lift()
            menu_btn.lift()
            aktiv_frame.set("delete")
        case "insert":
            frame_insert.place_forget()
            frame_insert.place(x=0,y=700)
            frame_insert.lift()
            menu_btn.lift()
            aktiv_frame.set("insert")
        case "edit":
            frame_edit.place_forget()
            frame_edit.place(x=0,y=700)
            frame_edit.lift()
            menu_btn.lift()
            aktiv_frame.set("edit")
        case "grey":
            frame_grey.place_forget()
            frame_grey.place(x=0,y=700)
            frame_grey.lift()
            menu_btn.lift()
            aktiv_frame.set("grey")
        case "menu":
            frame_draw.place_forget()
            frame_delete.place_forget()
            frame_insert.place_forget()
            frame_edit.place_forget()
            frame_grey.place_forget()
            frame_menu.place(x=0,y=700)
            frame_menu.lift()
            aktiv_frame.set("menu")

def load_image(size=(3200,2100), img_path=None, img_array=None):
    """
    Lädt ein Bild aus einer Datei oder aus einem NumPy-Array.

    Funktion:
    - Wenn ein Dateipfad übergeben wird, wird das Bild geöffnet, skaliert und als Tkinter-Bild zurückgegeben.
    - Zusätzlich wird beim Laden aus einer Datei das unbearbeitete Bild als NumPy-Array zurückgegeben.
    - Wenn ein NumPy-Array übergeben wird, wird daraus ein Tkinter-kompatibles Bild erstellt.
    - Wird sowohl zum ersten Laden als auch zum Aktualisieren der Anzeige verwendet.

    Parameter:
        size (tuple): Die gewünschte Anzeigegröße als (Breite, Höhe).
        img_path (str): Optionaler Dateipfad zu einem Bild.
        img_array (numpy.ndarray): Optionales Bildarray, aus dem ein Bild erzeugt wird.

    Rückgabewert:
        tuple oder ImageTk.PhotoImage:
            - Bei img_path: (PhotoImage, numpy.ndarray)
            - Bei img_array: PhotoImage
    """
    if img_path:
        img = Image.open(img_path).convert("RGB")
        img_resized = img.resize(size) # Breite, Höhe anpassen
        img = ImageTk.PhotoImage(img_resized)

        img_raw = np.array(Image.open(img_path))
        return img, img_raw
    
    img = Image.fromarray(img_array).convert("RGB")
    img_resized = img.resize(size)
    img = ImageTk.PhotoImage(img_resized)
    return img

def main():
    """
    Startet die komplette Tkinter-Anwendung.

    Funktion:
    - Erstellt das Hauptfenster.
    - Ruft setup_gui() auf, um die Grundstruktur der Oberfläche zu erzeugen.
    - Erstellt alle Buttons, Labels und Slider.
    - Verknüpft die GUI-Elemente mit den passenden Funktionen.
    - Startet die Tkinter-Hauptschleife.

    Parameter:
        Keine

    Rückgabewert:
        Keiner (None)
    """
    global menu_btn, r_channel, g_channel, b_channel, root
    root = tk.Tk()

    setup_gui(root)

    menu_btn_height = 100
    menu_btn_width = 200

    menu_label_width = 10

    #Buttons im top_menu für allgemeine Funktionen

    upload_btn = modern_button(frame_top_menu, text="Hochladen", command=upload_file)
    upload_btn.place(x=50, y=25, height=menu_btn_height, width=menu_btn_width)    

    export_btn = modern_button(frame_top_menu, text="Exportieren", command=export_file)
    export_btn.place(x=300, y=25, height=menu_btn_height, width=menu_btn_width)

    new_btn = modern_button(frame_top_menu, text="Neu", command=new_file)
    new_btn.place(x=550, y=25, height=menu_btn_height, width=menu_btn_width)

    zoom_btn = modern_button(frame_top_menu, text="Zoom", command=switch_zoom)
    zoom_btn.place(x=800, y=25, height=menu_btn_height, width=menu_btn_width)

    back_btn = modern_button(frame_top_menu, text="Zurück", command=back)
    back_btn.place(x=1050, y=25, height=menu_btn_height, width=menu_btn_width)

    forward_btn = modern_button(frame_top_menu, text="Vor", command=forward)
    forward_btn.place(x=1300, y=25, height=menu_btn_height, width=menu_btn_width)

    save_btn = modern_button(frame_top_menu, text="Speichern", command=save)
    save_btn.place(x=1550, y=25, height=menu_btn_height, width=menu_btn_width)

    #Text in frame_ori und frame_edit falls noch kein Bild geladen ist
    no_picture = modern_label(frame_editor, text="Kein Bild geladen")
    no_picture.place(x=1600,y=1050)

    no_picture_2 = modern_label(frame_ori, text="Kein Bild geladen")
    no_picture_2.place(x=250,y=350)

    #Text sowie Buttons im frame_menu
    home_lbl = modern_label(frame_menu,text="Home:", height=2, width=menu_label_width,font=FONT_TITLE)
    home_lbl.place(x=0,y=0)

    channel_btn = modern_button(frame_menu, text="Kanal", command=lambda: frame_change("channel"))
    channel_btn.place(x=50, y=200, height=menu_btn_height, width=menu_btn_width)

    draw_btn = modern_button(frame_menu, text="Zeichnen", command=lambda: frame_change("draw"))
    draw_btn.place(x=50, y=400, height=menu_btn_height, width=menu_btn_width)

    edit_btn = modern_button(frame_menu, text="Ändern", command=lambda: frame_change("edit"))
    edit_btn.place(x=450, y=400, height=menu_btn_height, width=menu_btn_width)

    grey_btn = modern_button(frame_menu, text="Graustufen", command=lambda: frame_change("grey"))
    grey_btn.place(x=450, y=200, height=menu_btn_height, width=menu_btn_width)

    #Menu Button im Root layout
    menu_btn = modern_button(root, text="Menu", command=lambda: frame_change("menu"))
    menu_btn.place(x=550, y=750, height=menu_btn_height, width=menu_btn_width)

    #Buttons und Labels im Kanal layout
    channel_lbl = modern_label(frame_channel,text="Kanal:", height=2, width=menu_label_width,font=FONT_TITLE)
    channel_lbl.place(x=0,y=0)

    r_lbl = modern_label(frame_channel,text="R", height=2, width=menu_label_width,font=FONT_SMALL)
    r_lbl.place(x=50, y=200)
    g_lbl = modern_label(frame_channel,text="G", height=2, width=menu_label_width,font=FONT_SMALL)
    g_lbl.place(x=200, y=200)
    b_lbl = modern_label(frame_channel,text="B", height=2, width=menu_label_width,font=FONT_SMALL)
    b_lbl.place(x=350, y=200)
    r_channel = modern_scale(frame_channel, from_=100, to=0, width=40, command=lambda val: change_channel(val,0))
    r_channel.set(100)
    r_channel.bind("<ButtonPress-1>", save_start_channel)
    r_channel.bind("<ButtonRelease-1>", save_channel)
    r_channel.place(x=50,y=300, height=600)
    g_channel = modern_scale(frame_channel, from_=100, to=0, width=40, command=lambda val: change_channel(val,1))
    g_channel.set(100)
    g_channel.bind("<ButtonPress-1>", save_start_channel)
    g_channel.bind("<ButtonRelease-1>", save_channel)
    g_channel.place(x=230,y=300, height=600)
    b_channel = modern_scale(frame_channel, from_=100, to=0, width=40, command=lambda val: change_channel(val,2))
    b_channel.set(100)
    b_channel.bind("<ButtonPress-1>", save_start_channel)
    b_channel.bind("<ButtonRelease-1>", save_channel)
    b_channel.place(x=410,y=300, height=600)

    #Buttons und Labels im Zeichnen layout
    draw_lbl = modern_label(frame_draw,text="Zeichnen:", height=2, width=menu_label_width,font=FONT_TITLE)
    draw_lbl.place(x=0,y=0)

    r_lbl_draw = modern_label(frame_draw,text="R", height=2, width=menu_label_width,font=FONT_SMALL)
    r_lbl_draw.place(x=50, y=200)
    g_lbl_draw = modern_label(frame_draw,text="G", height=2, width=menu_label_width,font=FONT_SMALL)
    g_lbl_draw.place(x=200, y=200)
    b_lbl_draw = modern_label(frame_draw,text="B", height=2, width=menu_label_width,font=FONT_SMALL)
    b_lbl_draw.place(x=350, y=200)
    r_draw = modern_scale(frame_draw, from_=255, to=0, width=40, command=lambda val: change_colors(val,0))  
    r_draw.place(x=50,y=300, height=600)
    g_draw = modern_scale(frame_draw, from_=255, to=0, width=40, command=lambda val: change_colors(val,1)) 
    g_draw.place(x=230,y=300, height=600)
    b_draw = modern_scale(frame_draw, from_=255, to=0, width=40, command=lambda val: change_colors(val,2)) 
    b_draw.place(x=410,y=300, height=600)

    paint_lbl = modern_label(frame_draw, text="Pinsel Größe", height=2, width=40, font=FONT_SMALL)
    paint_lbl.place(x=50, y=950)
    paint_size = modern_scale(frame_draw,from_=1 ,to=200, width=40, orient=tk.HORIZONTAL, command=change_brush_size)
    paint_size.place(x=50,y=1000, width=604)


    #Buttons und Labels im Ändern layout
    edit_lbl = modern_label(frame_edit,text="Ändern:", height=2, width=menu_label_width,font=FONT_TITLE)
    edit_lbl.place(x=0,y=0)

    inv_x = modern_button(frame_edit, text="Invert X", command=invert_x)
    inv_x.place(x=50, y=200, height=menu_btn_height, width=menu_btn_width)

    inv_y = modern_button(frame_edit, text="Invert Y", command=invert_y)
    inv_y.place(x=50, y=400, height=menu_btn_height, width=menu_btn_width)

    inv_color = modern_button(frame_edit, text="Invert Color", command=invert_color)
    inv_color.place(x=50, y=600, height=menu_btn_height, width=menu_btn_width)
  
    #Buttons und Labels im Graustufen layout
    grey_lbl = modern_label(frame_grey,text="Graustufen:", height=2, width=menu_label_width,font=FONT_TITLE)
    grey_lbl.place(x=0,y=0)

    make_grey = modern_button(frame_grey, text="Schwarz/Weiß", command=white_black)
    make_grey.place(x=50, y=200, height=menu_btn_height, width=menu_btn_width+50)


    #Jedes Frame nach ganz oben setzen dass sie alle zu sehen sind
    frame_menu.lift()
    frame_ori.lift()
    frame_editor.lift()
    frame_top_menu.lift()


    root.mainloop()

main()