import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt 

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
    global img_ori, img_edit, img_edit_raw, image_lbl, img_edit_display, loaded, last_img

    dateipfad = filedialog.askopenfilename(
        title="Wähle eine Datei zum bearbeiten aus",
        initialdir="/home/julian/Dokumente/Dokumente/FSST/Software/Korber/Photoshop", # Startverzeichnis
        filetypes=(("Bild Datei", "*.jpg"), ("Alle Dateien", "*.*")) # Filter
    )
    #Bild anzeigen im editor frame
    img_edit, img_edit_raw = load_image(size=(3200,2100),img_path=dateipfad)
    image_lbl = modern_label(frame_editor, image=img_edit)
    image_lbl.bind("<Button-1>", draw)
    image_lbl.bind("<B1-Motion>",draw)
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
    global img_edit
    img_edit = load_image(img_array=img)
    image_lbl.config(image=img_edit)

def change_channel(value, channel):
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
    global channel_dragging, loaded

    if loaded and not channel_dragging:
        save_history()
        channel_dragging = True
    
def export_file():
    pass

def new_file():
    pass

def zoom():
    pass

def invert_x():
    global img_edit_raw, last_img, back_count
    save_history()
    img_edit_raw = img_edit_raw[::-1,:]
    show(img=img_edit_raw)

def invert_y():
    global img_edit_raw, last_img, back_count
    save_history()
    img_edit_raw = img_edit_raw[:,::-1]
    show(img=img_edit_raw)

def invert_color():
    global img_edit_raw, last_img, back_count
    save_history()
    for i in range(3):
        img_edit_raw[:,:,i] = 255 - img_edit_raw[:,:,i]
    show(img=img_edit_raw)

def back():
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
    pass

def change_colors(value, channel):
    global draw_colors
    draw_colors[int(channel)] = int(value)

def draw_circle(img, x, y):
    global draw_colors, brush_size
    h, w = img.shape[:2]

    yy, xx = np.ogrid[:h, :w]

    mask = (xx - x) ** 2 + (yy - y) ** 2 <= brush_size ** 2

    img[mask] = draw_colors
    return img

def draw(event):
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
    global menu_btn, r_channel, g_channel, b_channel
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

    zoom_btn = modern_button(frame_top_menu, text="Zoom", command=zoom)
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

    delete_btn = modern_button(frame_menu, text="Löschen", command=lambda: frame_change("delete"))
    delete_btn.place(x=50, y=600, height=menu_btn_height, width=menu_btn_width)

    insert_btn = modern_button(frame_menu, text="Einfügen", command=lambda: frame_change("insert"))
    insert_btn.place(x=50, y=800, height=menu_btn_height, width=menu_btn_width)

    edit_btn = modern_button(frame_menu, text="Ändern", command=lambda: frame_change("edit"))
    edit_btn.place(x=50, y=1000, height=menu_btn_height, width=menu_btn_width)

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

    #Buttons und Labels im Löschen layout 
    delete_lbl = modern_label(frame_delete,text="Löschen:", height=2, width=menu_label_width,font=FONT_TITLE)
    delete_lbl.place(x=0,y=0)


    #Buttons und Labels im Einfügen layout
    insert_lbl = modern_label(frame_insert,text="Einfügen:", height=2, width=menu_label_width,font=FONT_TITLE)
    insert_lbl.place(x=0,y=0)


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


    #Jedes Frame nach ganz oben setzen dass sie alle zu sehen sind
    frame_menu.lift()
    frame_ori.lift()
    frame_editor.lift()
    frame_top_menu.lift()


    root.mainloop()

main()