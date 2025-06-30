from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from audio_monitor import start_audio_monitor
from gui import show_gui
import threading
import sys

running = True

def create_icon_image():
    icon = Image.new("RGB", (64, 64), (30, 30, 30))
    draw = ImageDraw.Draw(icon)
    draw.rectangle((16, 16, 48, 48), fill="purple")
    draw.text((22, 22), "PP", fill="white")
    return icon

def open_settings(icon, _):
    threading.Thread(target=show_gui, daemon=True).start()

def exit_app(icon, _):
    global running
    running = False
    icon.stop()
    sys.exit()

def run_tray_icon():
    icon_image = create_icon_image()
    menu = Menu(
        MenuItem("Settings", open_settings),
        MenuItem("Exit", exit_app)
    )
    tray_icon = Icon("PremiereProMute", icon_image, "PremiereProMute", menu)
    threading.Thread(target=start_audio_monitor, daemon=True).start()
    tray_icon.run()
