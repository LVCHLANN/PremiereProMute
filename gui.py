import tkinter as tk
from tkinter import ttk

def show_gui():
    def on_close():
        root.withdraw()

    root = tk.Tk()
    root.title("PremiereProMute Settings")
    root.geometry("400x380")
    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(".", background="#1e1e1e", foreground="white")
    style.configure("TButton", padding=6)
    style.configure("TCheckbutton", padding=4)

    ttk.Label(root, text="🔧 Settings", font=("Segoe UI", 12)).pack(pady=10)

    ttk.Checkbutton(root, text="Enable automatic muting").pack(anchor="w", padx=20)
    ttk.Checkbutton(root, text="Start on system boot").pack(anchor="w", padx=20)
    ttk.Checkbutton(root, text="Show notifications").pack(anchor="w", padx=20)

    ttk.Label(root, text="Fade volume %").pack(pady=(15, 5))
    fade_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal")
    fade_slider.set(10)
    fade_slider.pack(padx=20, fill="x")

    ttk.Label(root, text="Fade duration (ms)").pack(pady=(15, 5))
    duration_entry = ttk.Entry(root)
    duration_entry.insert(0, "500")
    duration_entry.pack(padx=20, fill="x")

    ttk.Label(root, text="Example whitelist apps").pack(pady=(15, 5))
    app_list = tk.Listbox(root, height=4)
    for app in ["Discord", "Spotify", "Chrome"]:
        app_list.insert(tk.END, app)
    app_list.pack(padx=20, fill="both", expand=True)

    ttk.Button(root, text="Close", command=on_close).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
