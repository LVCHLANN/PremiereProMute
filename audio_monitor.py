import time
import pythoncom
import threading
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation

FADE_STEPS = 10
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
                if meter.GetPeakValue() > 0.01:
                    return True
            except Exception:
                continue
    return False

def fade_volume(session, target_volume, duration=0.5):
    try:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        current = volume.GetMasterVolume()
        step = (target_volume - current) / FADE_STEPS
        for _ in range(FADE_STEPS):
            current += step
            volume.SetMasterVolume(max(0, min(1, current)), None)
            time.sleep(duration / FADE_STEPS)
    except Exception:
        pass

def start_audio_monitor():
    global faded
    pythoncom.CoInitialize()
    while running:
        try:
            sessions = get_audio_sessions()
            active = is_premiere_playing()

            for session in sessions:
                if not session.Process:
                    continue
                name = session.Process.name().lower()
                if "premiere" in name:
                    continue

                if active and not faded:
                    threading.Thread(target=fade_volume, args=(session, TARGET_FADE_VOLUME)).start()
                elif not active and faded:
                    threading.Thread(target=fade_volume, args=(session, 1.0)).start()

            faded = active
            time.sleep(0.3)
        except Exception:
            time.sleep(0.5)
