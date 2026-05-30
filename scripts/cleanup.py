"""Clean up all data files: PDFs, processed data, and FAISS index."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.core.config import settings


def main():
    dirs_to_clean = [
        settings.pdf_upload_dir,
        settings.processed_dir,
        settings.faiss_index_dir,
    ]

    for directory in dirs_to_clean:
        if not directory.exists():
            continue

        count = 0
        for f in directory.iterdir():
            if f.name == ".gitkeep":
                continue
            f.unlink()
            count += 1

        print(f"Cleaned {count} file(s) from {directory}")

    print("Cleanup complete.")


if __name__ == "__main__":
    confirm = input("This will delete all data. Continue? (y/N): ")
    if confirm.lower() == "y":
        main()
    else:
        print("Cancelled.")
