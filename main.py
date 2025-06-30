import sys
import os
import threading
import subprocess
from gui import show_gui
from tray import run_tray_icon
from audio_monitor import start_audio_monitor

def print_help():
    print("""
PremiereProMute - Automatically mutes background audio when Premiere Pro is playing

Usage:
  PremiereProMute.exe [OPTIONS]

Options:
  --settings       Open the settings menu
  --console        Run with terminal output (works in windowed build too)
  --help, -h       Show this help message
    """)

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_help()
        return

    if "--settings" in args:
        show_gui()
        return

    if "--console" in args:
        # Relaunch in a new terminal window without the --console flag
        script_path = os.path.abspath(sys.argv[0])
        filtered_args = [arg for arg in args if arg != "--console"]
        cmd = f'start cmd /k "{script_path} {" ".join(filtered_args)}"'
        subprocess.Popen(cmd, shell=True)
        return

    # Normal tray + monitor launch
    monitor_thread = threading.Thread(target=start_audio_monitor, daemon=True)
    monitor_thread.start()
    run_tray_icon()

if __name__ == "__main__":
    main()
