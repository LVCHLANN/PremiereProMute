@echo off
echo 🔨 Building PremiereProMute...
pyinstaller --onefile --windowed --name PremiereProMute main.py

echo 🧹 Cleaning up spec file...
del PremiereProMute.spec >nul 2>&1

echo ✅ Build complete! Check the dist\ folder.
pause
