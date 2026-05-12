import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

img = Image.open("/home/julian/Dokumente/Dokumente/FSST/Software/Korber/Photoshop/photo.jpg")
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo)
label.pack()

root.mainloop()
