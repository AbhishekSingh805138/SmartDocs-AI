"""Delete existing index and rebuild from all PDFs."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.vector_service import delete_index
from scripts.create_index import main as create_index


def main():
    print("Deleting existing FAISS index...")
    try:
        delete_index()
        print("Index deleted.")
    except Exception as e:
        print(f"No existing index to delete: {e}")

    print("\nRebuilding index...")
    create_index()


if __name__ == "__main__":
    main()
