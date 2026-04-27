import argparse
import shutil
from pathlib import Path
import sys

def delete_index_ob(root_directory):
    root_path = Path(root_directory)
    
    if not root_path.exists() or not root_path.is_dir():
        print(f"Error: The path '{root_directory}' is not a valid directory.")
        return

    found = False
    for path in root_path.rglob('index.ob'):
        found = True
        try:
            if path.is_file():
                path.unlink()
                print(f"Deleted file: {path}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"Deleted folder: {path}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")
    
    if not found:
        print("No 'index.ob' files or folders found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively delete 'index.ob' files/folders.")
    parser.add_argument("folder", help="The root folder to start searching from")
    
    args = parser.parse_args()
    
    confirm = input(f"Are you sure you want to delete all 'index.ob' items in '{args.folder}'? (y/n): ")
    if confirm.lower() == 'y':
        delete_index_ob(args.folder)
    else:
        print("Operation cancelled.")