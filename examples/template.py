import tkinter as tk

def flip_img(img):
    """
    Spiegelt ein Bild horizontal.

    Parameter:
        img (numpy.ndarray)
    Rückgabewert:
        numpy.ndarray: horizontal gespiegeltes Bild
    """
    pass


def setup_gui(root):
    """
    Konfiguriert das Hauptfenster und erstellt die 4 Frames.

    Parameter:
        root (tk.Tk): Das Hauptfenster der Anwendung.
    Rückgabewert:
        tuple: (frame1, frame2, frame3, frame4)
    """
    root.title("NumPy Bildverarbeitung")
    root.geometry("700x500")

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)



# ── Hauptprogramm ──────────────────────────────────────────────────────────

def main():
    
    # tkinter setup
    root = tk.Tk()
    setup_gui(root)
    
    # create Buttons etc.
    
    
    # run mainloop
    root.mainloop()

main()

