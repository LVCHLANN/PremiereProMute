import time
import threading
import sys
import pythoncom
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation
from comtypes import CLSCTX_ALL
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# Configuration
FADE_STEPS = 10
FADE_INTERVAL = 0.05
TARGET_FADE_VOLUME = 0.1

faded = False
running = True

def get_audio_sessions():
    return AudioUtilities.GetAllSessions()

def is_premiere_playing():
    sessions = get_audio_sessions()
    for session in sessions:
        if not session.Process:
            continue
        if "premiere" in session.Process.name().lower():
            try:
                meter = session._ctl.QueryInterface(IAudioMeterInformation)
                level = meter.GetPeakValue()
                if level > 0.01:
                    return True
            except Exception:
                continue
    return False

def fade_volume(session, target_volume, duration=0.5):
    try:
        volume_obj = session._ctl.QueryInterface(ISimpleAudioVolume)
        current = volume_obj.GetMasterVolume()
        step = (target_volume - current) / FADE_STEPS
        for _ in range(FADE_STEPS):
            current += step
            volume_obj.SetMasterVolume(max(0.0, min(1.0, current)), None)
            time.sleep(duration / FADE_STEPS)
    except Exception:
        pass

def audio_monitor():
    pythoncom.CoInitialize()  # 🛠 Fix COM error in threads
    global faded, running
    print("🎬 Audio monitor started...")

    while running:
        try:
            premiere_active = is_premiere_playing()
            print(f"Premiere Playing: {premiere_active}")

            sessions = get_audio_sessions()

            for session in sessions:
                if not session.Process:
                    continue

                name = session.Process.name().lower()

                if "premiere" in name:
                    continue

                try:
                    volume_obj = session._ctl.QueryInterface(ISimpleAudioVolume)
                    current = volume_obj.GetMasterVolume()
                    print(f" - Session: {name}, volume={current:.2f}")
                except Exception:
                    continue

                if premiere_active and not faded:
                    print(f" -> Fading down {name}")
                    threading.Thread(target=fade_volume, args=(session, TARGET_FADE_VOLUME)).start()
                elif not premiere_active and faded:
                    print(f" -> Fading up {name}")
                    threading.Thread(target=fade_volume, args=(session, 1.0)).start()

            faded = premiere_active
            time.sleep(0.3)
        except Exception as e:
            print(f"[!] Error in audio_monitor loop: {e}")
            time.sleep(0.5)

def create_icon_image():
    icon = Image.new("RGB", (64, 64), (30, 30, 30))
    draw = ImageDraw.Draw(icon)
    draw.rectangle((16, 16, 48, 48), fill="purple")
    draw.text((22, 22), "PP", fill="white")
    return icon

def exit_app(icon, _item):
    global running
    running = False
    icon.stop()
    sys.exit()

def run_tray_icon():
    icon_image = create_icon_image()
    menu = Menu(MenuItem("Exit", exit_app))
    tray_icon = Icon("PremiereMute", icon_image, "Premiere Mute", menu)
    threading.Thread(target=audio_monitor, daemon=True).start()
    tray_icon.run()

if __name__ == "__main__":
    run_tray_icon()
