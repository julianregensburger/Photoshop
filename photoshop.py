import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

def upload_file():
    global img_ori, img_edit

    dateipfad = filedialog.askopenfilename(
        title="Wähle eine Datei zum bearbeiten aus",
        initialdir="/home/julian/Dokumente/Dokumente/FSST/Software/Korber/Photoshop", # Startverzeichnis
        filetypes=(("Bild Datei", "*.jpg"), ("Alle Dateien", "*.*")) # Filter
    )
    #Bild anzeigen im editor frame
    img_edit = load_image(size=(3200,2100),img_path=dateipfad)
    image_lbl = tk.Label(frame_editor, image=img_edit)
    image_lbl.place(x=0,y=0)

    #Bild anzeigen im original frame
    img_ori = load_image(size=(800,700),img_path=dateipfad)
    image_lbl = tk.Label(frame_ori, image=img_ori)
    image_lbl.place(x=0,y=0)
    image_lbl.lift()

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

def setup_gui(root):
    """
    Konfiguriert das Hauptfenster und erstellt die 4 Haupt Frames und die 6 Neben Frames vom Menu.

    Parameter:
        root (tk.Tk): Das Hauptfenster der Anwendung.
    Rückgabewert:
        tuple: (frame1, frame2, frame3, frame4)
    """
    global frame_ori, frame_menu, frame_editor, frame_top_menu, frame_channel, frame_draw, frame_delete, frame_insert, frame_edit, frame_grey

    root.title("NumPy Bildverarbeitung")
    root.geometry("4000x2000")

    #4 Haupt Frames erstellen
    frame_ori = tk.Frame(root, width=800, height=700, bg="white")
    frame_ori.place(x=0,y=0)

    frame_menu = tk.Frame(root, width=800, height=1600, bg="grey")
    frame_menu.place(x=0,y=700)
 
    frame_editor = tk.Frame(root,width=3200, height=2100, bg="white")
    frame_editor.place(x=800,y=150)

    frame_top_menu = tk.Frame(root, width=3200, height=150, bg="grey")
    frame_top_menu.place(x=800,y=0)

    #6 Neben Frames im Menu erstellen
    frame_channel = tk.Frame(root, width=800, height=1600, bg="grey")
    frame_draw = tk.Frame(root, width=800, height=1600, bg="grey")
    frame_delete = tk.Frame(root, width=800, height=1600, bg="grey")
    frame_insert = tk.Frame(root, width=800, height=1600, bg="grey")
    frame_edit = tk.Frame(root, width=800, height=1600, bg="grey")
    frame_grey= tk.Frame(root, width=800, height=1600, bg="grey")

def frame_change(window):
    match window:
        case "channel":
            frame_menu.place_forget()
            frame_channel.place(x=0,y=700)
            frame_channel.lift()
            menu_btn.lift()
        case "draw":
            frame_draw.place_forget()
            frame_draw.place(x=0,y=700)
            frame_draw.lift()
            menu_btn.lift()
        case "delete":
            frame_delete.place_forget()
            frame_delete.place(x=0,y=700)
            frame_delete.lift()
            menu_btn.lift()
        case "insert":
            frame_insert.place_forget()
            frame_insert.place(x=0,y=700)
            frame_insert.lift()
            menu_btn.lift()
        case "edit":
            frame_edit.place_forget()
            frame_edit.place(x=0,y=700)
            frame_edit.lift()
            menu_btn.lift()
        case "grey":
            frame_grey.place_forget()
            frame_grey.place(x=0,y=700)
            frame_grey.lift()
            menu_btn.lift()
        case "menu":
            frame_draw.place_forget()
            frame_delete.place_forget()
            frame_insert.place_forget()
            frame_edit.place_forget()
            frame_grey.place_forget()
            frame_menu.place(x=0,y=700)
            frame_menu.lift()

def load_image(size, img_path):
    if img_path:
        img_raw = Image.open(img_path)
        img_resized = img_raw.resize(size) # Breite, Höhe anpassen
        img = ImageTk.PhotoImage(img_resized)
        return img

def main():
    global menu_btn

    root = tk.Tk()

    setup_gui(root)

    menu_btn_height = 100
    menu_btn_width = 200

    menu_label_width = 10

    #Buttons im top_menu für allgemeine Funktionen

    upload_btn = tk.Button(frame_top_menu, text="Hochladen", command=upload_file)
    upload_btn.place(x=50, y=25, height=menu_btn_height, width=menu_btn_width)    

    export_btn = tk.Button(frame_top_menu, text="Exportieren", command=export_file)
    export_btn.place(x=300, y=25, height=menu_btn_height, width=menu_btn_width)

    new_btn = tk.Button(frame_top_menu, text="Neu", command=new_file)
    new_btn.place(x=550, y=25, height=menu_btn_height, width=menu_btn_width)

    zoom_btn = tk.Button(frame_top_menu, text="Zoom", command=zoom)
    zoom_btn.place(x=800, y=25, height=menu_btn_height, width=menu_btn_width)

    back_btn = tk.Button(frame_top_menu, text="Zurück", command=back)
    back_btn.place(x=1050, y=25, height=menu_btn_height, width=menu_btn_width)

    forward_btn = tk.Button(frame_top_menu, text="Vor", command=forward)
    forward_btn.place(x=1300, y=25, height=menu_btn_height, width=menu_btn_width)

    save_btn = tk.Button(frame_top_menu, text="Speichern", command=save)
    save_btn.place(x=1550, y=25, height=menu_btn_height, width=menu_btn_width)

    #Text in frame_ori und frame_edit falls noch kein Bild geladen ist
    no_picture = tk.Label(frame_editor, text="Kein Bild geladen")
    no_picture.place(x=1600,y=1050)

    no_picture_2 = tk.Label(frame_ori, text="Kein Bild geladen")
    no_picture_2.place(x=250,y=350)

    #Text sowie Buttons im frame_menu
    home_lbl = tk.Label(frame_menu,text="Home:", height=2, width=menu_label_width,font=("Arial", 25))
    home_lbl.place(x=0,y=0)

    channel_btn = tk.Button(frame_menu, text="Kanal", command=lambda: frame_change("channel"))
    channel_btn.place(x=50, y=200, height=menu_btn_height, width=menu_btn_width)

    draw_btn = tk.Button(frame_menu, text="Zeichnen", command=lambda: frame_change("draw"))
    draw_btn.place(x=50, y=400, height=menu_btn_height, width=menu_btn_width)

    delete_btn = tk.Button(frame_menu, text="Löschen", command=lambda: frame_change("delete"))
    delete_btn.place(x=50, y=600, height=menu_btn_height, width=menu_btn_width)

    insert_btn = tk.Button(frame_menu, text="Einfügen", command=lambda: frame_change("insert"))
    insert_btn.place(x=50, y=800, height=menu_btn_height, width=menu_btn_width)

    edit_btn = tk.Button(frame_menu, text="Ändern", command=lambda: frame_change("edit"))
    edit_btn.place(x=50, y=1000, height=menu_btn_height, width=menu_btn_width)

    grey_btn = tk.Button(frame_menu, text="Graustufen", command=lambda: frame_change("grey"))
    grey_btn.place(x=450, y=200, height=menu_btn_height, width=menu_btn_width)

    #Menu Button im Root layout
    menu_btn = tk.Button(root, text="Menu", command=lambda: frame_change("menu"))
    menu_btn.place(x=550, y=750, height=menu_btn_height, width=menu_btn_width)

    #Buttons und Labels im Kanal layout
    channel_lbl = tk.Label(frame_channel,text="Kanal:", height=2, width=menu_label_width,font=("Arial", 25))
    channel_lbl.place(x=0,y=0)


    #Buttons und Labels im Zeichnen layout
    draw_lbl = tk.Label(frame_draw,text="Zeichnen:", height=2, width=menu_label_width,font=("Arial", 25))
    draw_lbl.place(x=0,y=0)


    #Buttons und Labels im Löschen layout 
    delete_lbl = tk.Label(frame_delete,text="Löschen:", height=2, width=menu_label_width,font=("Arial", 25))
    delete_lbl.place(x=0,y=0)


    #Buttons und Labels im Einfügen layout
    insert_lbl = tk.Label(frame_insert,text="Einfügen:", height=2, width=menu_label_width,font=("Arial", 25))
    insert_lbl.place(x=0,y=0)


    #Buttons und Labels im Ändern layout
    edit_lbl = tk.Label(frame_edit,text="Ändern:", height=2, width=menu_label_width,font=("Arial", 25))
    edit_lbl.place(x=0,y=0)


    #Buttons und Labels im Graustufen layout
    grey_lbl = tk.Label(frame_grey,text="Graustufen:", height=2, width=menu_label_width,font=("Arial", 25))
    grey_lbl.place(x=0,y=0)


    #Jedes Frame nach ganz oben setzen dass sie alle zu sehen sind
    frame_menu.lift()
    frame_ori.lift()
    frame_editor.lift()
    frame_top_menu.lift()


    root.mainloop()

main()
