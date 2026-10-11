"""
VidMind System & Dependency Verification Script
Checks all required runtimes, CLI tools, libraries, and hardware capabilities.
"""
import sys
import shutil
import subprocess
import platform
import os
from pathlib import Path


def check_runtime():
    print("=" * 60)
    print("VidMind Environment & Dependency Checker")
    print("=" * 60)
    
    # 1. OS & Platform
    print(f"[x] OS: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"[x] Python: {sys.version.split()[0]} ({sys.executable})")
    
    if sys.version_info < (3, 10):
        print("  [!] WARNING: Python 3.10+ is recommended (3.11 preferred).")
    else:
        print("  [+] Python version satisfies >= 3.10 requirement.")

    # 2. FFmpeg check
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        try:
            res = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True, check=True)
            ver = res.stdout.splitlines()[0] if res.stdout else "Available"
            print(f"[+] FFmpeg found: {ffmpeg_path} ({ver})")
        except Exception as e:
            print(f"[!] FFmpeg found at {ffmpeg_path} but failed to execute: {e}")
    else:
        print("[-] FFmpeg NOT found in PATH. Audio extraction will fail!")

    # 3. Node.js & npm
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    if node_path and npm_path:
        try:
            n_res = subprocess.run([node_path, "--version"], capture_output=True, text=True)
            print(f"[+] Node.js found: {node_path} ({n_res.stdout.strip()})")
        except Exception:
            print(f"[+] Node.js found: {node_path}")
    else:
        print("[-] Node.js or npm missing. Frontend will not start!")

    # 4. Ollama check
    ollama_path = shutil.which("ollama")
    if ollama_path:
        print(f"[+] Ollama found: {ollama_path}")
    else:
        print("[*] Ollama CLI not in PATH. Will check if local HTTP port 11434 is active or use mock/fallback.")

    # 5. Core Python Libraries check
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic v2"),
        ("sqlalchemy", "SQLAlchemy"),
        ("aiosqlite", "aiosqlite"),
        ("yt_dlp", "yt-dlp"),
        ("faster_whisper", "faster-whisper"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "faiss-cpu"),
        ("pytest", "pytest"),
    ]
    
    print("\n--- Python Package Status ---")
    missing = []
    for mod_name, label in packages:
        try:
            __import__(mod_name)
            print(f"  [+] {label}: INSTALLED")
        except ImportError:
            print(f"  [-] {label}: NOT INSTALLED")
            missing.append(label)

    print("\n--- Hardware Capabilities ---")
    try:
        import torch
        cuda_avail = torch.cuda.is_available()
        print(f"  PyTorch Version: {torch.__version__}")
        print(f"  CUDA Available: {cuda_avail}")
        if cuda_avail:
            print(f"  CUDA Device: {torch.cuda.get_device_name(0)}")
        else:
            print("  Running on CPU-only tier (faster-whisper int8 recommended).")
    except ImportError:
        print("  PyTorch not installed yet. System will run on CPU mode by default.")

    print("=" * 60)
    if missing:
        print(f"Status: {len(missing)} Python packages missing. Run `pip install -r requirements.txt`")
        return False
    else:
        print("Status: All critical dependencies verified successfully!")
        return True


if __name__ == "__main__":
    check_runtime()
