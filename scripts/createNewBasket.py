from pathlib import Path
import subprocess
import argparse


def main():
    print("Do somethin")
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("input_string", help="")
    args = parser.parse_args()
    print(f"Passed argument: {args.input_string}")

    path = Path(args.input_string)
    create(path)

def create(pathString):
    print(f"Create Structure at {pathString}")
    source_folder = Path(pathString)
    path = source_folder / "basketSrc.ob"
    f = open(path, "w")
    if path.exists():
        print("Operation successfull -> created at " + str(path))
        result = subprocess.run(["python", "scripts/index.py", str(path)], capture_output=True, text=True)
        print(f"{result.stdout}")
        if result.stderr:
            print(result.stderr)
    else:
        print("Error")