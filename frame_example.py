import tkinter as tk


def setup_gui(root):
    root.title("Template")
    root.geometry("600x400")
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)


def main():
    root = tk.Tk()
    setup_gui(root)

    frame1 = tk.LabelFrame(root, text="Panel 1", bg="lightblue")
    frame1.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

    frame2 = tk.LabelFrame(root, text="Panel 2", bg="lightgreen")
    frame2.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

    frame3 = tk.LabelFrame(root, text="Panel 3", bg="lightyellow")
    frame3.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

    frame4 = tk.LabelFrame(root, text="Panel 4", bg="lightsalmon")
    frame4.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")

    tk.Button(frame1, text="Button A").pack(pady=5)
    tk.Button(frame1, text="Button B").pack(pady=5)

    tk.Button(frame2, text="Button C").pack(pady=5)
    tk.Button(frame2, text="Button D").pack(pady=5)

    tk.Button(frame3, text="Button E").pack(pady=5)
    tk.Button(frame3, text="Button F").pack(pady=5)

    tk.Button(frame4, text="Button G").pack(pady=5)
    tk.Button(frame4, text="Button H").pack(pady=5)

    root.mainloop()


main()
