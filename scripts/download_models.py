"""
VidMind Model Downloader
Pre-downloads the configured faster-whisper model and embedding model.
"""
import os
import sys

def download_models():
    print("=" * 60)
    print("VidMind Model Downloader")
    print("=" * 60)
    
    # 1. Download faster-whisper model
    whisper_model = os.getenv("TRANSCRIPTION_MODEL", "base")
    print(f"[*] Downloading / verifying faster-whisper model: {whisper_model}...")
    try:
        from faster_whisper import WhisperModel
        # Download and test loading
        model = WhisperModel(whisper_model, device="cpu", compute_type="int8", download_root="./data/cache/models")
        print(f"[+] faster-whisper model '{whisper_model}' downloaded and ready.")
    except ImportError:
        print("[!] faster-whisper is not installed. Install with `pip install faster-whisper`")
    except Exception as e:
        print(f"[-] Error downloading Whisper model: {e}")

    # 2. Download sentence-transformers embedding model
    embed_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    print(f"\n[*] Downloading / verifying embedding model: {embed_model}...")
    try:
        from sentence_transformers import SentenceTransformer
        s_model = SentenceTransformer(embed_model, cache_folder="./data/cache/models")
        print(f"[+] Embedding model '{embed_model}' downloaded and ready.")
    except ImportError:
        print("[!] sentence-transformers is not installed. Install with `pip install sentence-transformers`")
    except Exception as e:
        print(f"[-] Error downloading embedding model: {e}")

    print("\n[+] Model check complete.")

if __name__ == "__main__":
    download_models()
