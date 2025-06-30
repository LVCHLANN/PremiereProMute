import tkinter as tk
from tkinter import ttk, simpledialog
import json
import os

CONFIG_FILE = "config.json"

class CreateToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip, text=self.text, justify="left",
            background="#333", foreground="white",
            relief="solid", borderwidth=1,
            font=("Segoe UI", 9), padx=6, pady=2
        )
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def load_config():
    if os.path.exists("config.json"):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "enable_muting": True,
        "start_on_boot": False,
        "show_notifications": True,
        "fade_volume": 10,
        "fade_duration": 500,
        "whitelist": ["Discord", "Spotify", "Chrome"]
    }

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def show_gui():
    config = load_config()

    def on_close():
        updated_config = {
            "enable_muting": enable_muting_var.get(),
            "start_on_boot": start_on_boot_var.get(),
            "show_notifications": show_notifications_var.get(),
            "fade_volume": int(fade_volume_entry.get() or "10"),
            "fade_duration": int(duration_entry.get() or "500"),
            "whitelist": [whitelist_listbox.get(i) for i in range(whitelist_listbox.size())]
        }
        save_config(updated_config)
        root.destroy()

    def add_app():
        app = simpledialog.askstring("Add App", "Enter app name (e.g. Discord):", parent=root)
        if app:
            whitelist_listbox.insert(tk.END, app)
            update_scrollbar()

    def remove_selected():
        selected = whitelist_listbox.curselection()
        for i in reversed(selected):
            whitelist_listbox.delete(i)
        update_scrollbar()

    def update_scrollbar(*_):
        if whitelist_listbox.size() > 8:
            whitelist_scroll.pack(side="right", fill="y")
        else:
            whitelist_scroll.pack_forget()

    root = tk.Tk()
    root.title("PremiereProMute Settings")
    root.geometry("480x660")
    root.minsize(480, 660)
    root.configure(bg="#1e1e1e")

    # Force theme reset to avoid weird light/dark mix
    style = ttk.Style()
    style.theme_use("alt")   # temporary
    style.theme_use("clam")  # actual theme

    style.configure(".", background="#1e1e1e", foreground="white", fieldbackground="#2a2a2a")
    style.configure("TLabel", background="#1e1e1e", foreground="white")
    style.configure("TButton", background="#2a2a2a", foreground="white")
    style.configure("TCheckbutton", background="#1e1e1e", foreground="white")
    style.map("TButton",
        background=[("active", "#3d3d3d")],
        foreground=[("disabled", "#777"), ("active", "white")]
    )
    style.map("TCheckbutton",
        background=[("active", "#2a2a2a")],
        foreground=[("active", "white")]
    )

    container = ttk.Frame(root, padding=20)
    container.pack(expand=True, fill="both")

    ttk.Label(container, text="🔧 General Settings", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

    enable_muting_var = tk.BooleanVar(value=config["enable_muting"])
    start_on_boot_var = tk.BooleanVar(value=config["start_on_boot"])
    show_notifications_var = tk.BooleanVar(value=config["show_notifications"])

    ttk.Checkbutton(container, text="Enable automatic muting", variable=enable_muting_var).pack(anchor="w", pady=2)
    ttk.Checkbutton(container, text="Start on system boot", variable=start_on_boot_var).pack(anchor="w", pady=2)
    ttk.Checkbutton(container, text="Show notifications", variable=show_notifications_var).pack(anchor="w", pady=2)

    ttk.Separator(container, orient="horizontal").pack(fill="x", pady=12)

    ttk.Label(container, text="🎚 Audio Settings", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

    ttk.Label(container, text="Fade Volume", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 0))
    ttk.Label(container, text="Volume (%) that background apps are reduced to during playback.").pack(anchor="w", pady=(0, 5))
    fade_frame = ttk.Frame(container)
    fade_frame.pack(fill="x", pady=0)
    fade_volume_entry = tk.Entry(fade_frame, bg="#2a2a2a", fg="white", insertbackground="white",
                                 relief="flat", highlightthickness=1, highlightbackground="#444")
    fade_volume_entry.insert(0, str(config["fade_volume"]))
    fade_volume_entry.pack(side="left", fill="x", expand=True)
    ttk.Label(fade_frame, text="%").pack(side="left", padx=(6, 0))
    CreateToolTip(fade_volume_entry, "Enter the target volume (0–100%) for background apps during Premiere playback.")

    ttk.Label(container, text="Fade Duration", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 0))
    ttk.Label(container, text="Time (ms) to fade volumes when Premiere starts or stops.").pack(anchor="w", pady=(0, 5))
    duration_frame = ttk.Frame(container)
    duration_frame.pack(fill="x")
    duration_entry = tk.Entry(duration_frame, bg="#2a2a2a", fg="white", insertbackground="white",
                              relief="flat", highlightthickness=1, highlightbackground="#444")
    duration_entry.insert(0, str(config["fade_duration"]))
    duration_entry.pack(side="left", fill="x", expand=True)
    ttk.Label(duration_frame, text="ms").pack(side="left", padx=(6, 0))
    CreateToolTip(duration_entry, "Higher values = slower fade. 500ms is smooth. Set to 0 for instant mute.")

    ttk.Separator(container, orient="horizontal").pack(fill="x", pady=12)

    ttk.Label(container, text="📃 Whitelist Apps", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))

    whitelist_frame = ttk.Frame(container)
    whitelist_frame.pack(fill="both", expand=True)

    whitelist_scroll = ttk.Scrollbar(whitelist_frame, orient="vertical")
    whitelist_listbox = tk.Listbox(
        whitelist_frame,
        height=8,
        yscrollcommand=whitelist_scroll.set,
        selectmode=tk.MULTIPLE,
        bg="#2a2a2a",
        fg="white",
        bd=0,
        highlightthickness=1,
        highlightbackground="#444",
        selectbackground="#007acc",
        relief="flat"
    )
    whitelist_listbox.pack(side="left", fill="both", expand=True)
    whitelist_scroll.config(command=whitelist_listbox.yview)

    for app in config["whitelist"]:
        whitelist_listbox.insert(tk.END, app)
    update_scrollbar()

    btn_frame = ttk.Frame(container)
    btn_frame.pack(pady=(8, 0), fill="x")
    ttk.Button(btn_frame, text="➕ Add App", command=add_app).pack(side="left", padx=(0, 10))
    ttk.Button(btn_frame, text="❌ Remove Selected", command=remove_selected).pack(side="left")

    ttk.Button(container, text="Close", command=on_close).pack(pady=(20, 0))

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
