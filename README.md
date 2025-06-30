# 🎬 PremiereProMute

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078D7)
![Python](https://img.shields.io/badge/python-3.12+-informational)
![License](https://img.shields.io/github/license/LVCHLANN/PremiereProMute)

**PremiereProMute** is a lightweight tray application for Windows that automatically mutes all other system audio when Adobe Premiere Pro starts playing audio — and fades it back in when playback stops.

This is useful for editors who want to focus on playback audio without distractions from background media (e.g., music, browser videos, Discord sounds).

---

## ⚙️ Features

- ✅ Automatically detects when Premiere Pro is outputting audio  
- ✅ Smoothly fades out all other app volumes (e.g. Chrome, Spotify, etc.)  
- ✅ Restores volumes when Premiere stops  
- ✅ Runs silently in the background from the system tray  
- ✅ Exit anytime from the tray icon  

---

## 🚧 Known Bugs / Limitations

- 🎧 Premiere must play audio through the **default output device**  
- 🔇 If Premiere audio is **too quiet or silent**, it may not be detected  
- 📺 Some apps (e.g., system sounds, UWP apps) may not respond to volume fading  
- 💻 Only works on **Windows** (cross-platform support planned)  
- 🎚 Volume fade settings are currently hardcoded  

---

## 🛠️ Building From Source

### 📦 Requirements

- Python 3.12  
- [pip](https://pip.pypa.io/)  

### 📁 Install Dependencies

`pip install -r requirements.txt`

### ▶️ Run the Script

`python main.py`

### 📦 Bundle Into a Standalone .EXE

`
pyinstaller --onefile --windowed --name PremiereProMute main.py
`

The output will appear in the `dist/` folder as `PremiereProMute.exe`.

---

## 📅 Roadmap

- [ ] Add configuration UI for fade settings  
- [ ] Allow per-app volume overrides  
- [ ] Add macOS/Linux support (via `pulsectl` or `pyobjc`)  
- [ ] Option to exclude apps (e.g. Discord)  
- [ ] Minimize-to-tray installer and auto-updater  

---

## 🤝 Contributing

PRs welcome! If you have ideas or bug reports, feel free to open an issue or fork the repo.

---

## 📄 License

MIT — free to use, modify, or distribute.

