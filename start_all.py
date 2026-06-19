"""
SyncLyft - Start Both Services
Run: py -3.11 start_all.py
"""
import subprocess
import sys
import os

interview_dir = r"C:\project-main\interview_service"
voice_dir = r"C:\project-main\voice_service"
python = r"C:\Users\MOHAMMAD MUSTAKEEM\AppData\Local\Programs\Python\Python311\python.exe"

print("=" * 50)
print("  SyncLyft - Starting All Services")
print("=" * 50)

# Start Interview Service
print("\n🚀 Starting Interview Service (port 8000)...")
p1 = subprocess.Popen(
    [python, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=interview_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE
)

# Start Voice Service
print("🎙️  Starting Voice Service (port 8001)...")
p2 = subprocess.Popen(
    [python, "main.py"],
    cwd=voice_dir,
    creationflags=subprocess.CREATE_NEW_CONSOLE
)

print("\n✅ Dono services start ho gayi!")
print("   Interview → http://127.0.0.1:8000/docs")
print("   Voice     → http://127.0.0.1:8001/docs")
print("\n   Band karne ke liye dono windows close karo!")
print("=" * 50)

try:
    p1.wait()
    p2.wait()
except KeyboardInterrupt:
    p1.terminate()
    p2.terminate()
    print("\nServices band ho gayi!")
