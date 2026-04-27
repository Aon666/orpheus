import argparse
import json
from pathlib import Path 

supported_formats = {".mp3", ".wav", ".flac", ".ogg"}

def main():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("input_string", help="")
    args = parser.parse_args()
    print(f"Passed argument: {args.input_string}")

    path = Path(args.input_string)
    index(path)


def index(folderPath):
    print(f"Start Indexing at {folderPath}")
    indexPath = folderPath / "index.ob"
    try:
        indexFile = open(indexPath,"r", encoding='utf-8')
    except FileNotFoundError:
        print(f"File not found. Create new one")
        initial_data = {}
        with open(indexPath, "w", encoding='utf-8') as newFile:
            json.dump(initial_data, newFile, indent=4)
        
        indexFile = open(indexPath,"r", encoding='utf-8')

    except Exception as e:
        print(e)

    #array
    indexedEntries = parseThroughIndexFile(indexPath)
    print(indexedEntries)
    folders = []

    #geh durch alle Dinge im Ordner durch
    for item in folderPath.iterdir():
        if item.is_file():
            print(f"got object {item.name}")
            #Dateien mit spezifischen Endungen werden überprüft
            if item.suffix.lower() in supported_formats:
                #removeEntry(item, indexPath)
                #continue;

                if item.name in indexedEntries:
                    #Nach Name: insd sie in der Liste? Nimm aus der Liste
                    print(f"found existing file")
                    del indexedEntries[item.name]
                else:
                    #Nicht in der Liste: Füge neue Einträge hinzu zu indexFile
                    addNewEntry(item, indexPath)
                
                #TODO pass Werte mit aggregaten an bpsw. Länge oä

        elif item.is_dir(): 
            #Folder werden in eigene Liste gespeichert
            print(f"got folder {item.name}")
            folders.append(item)

    #Liste noch nicht null -> es wurde etwas gelöscht
    if len(indexedEntries) > 0:
        print(f"There a still entries left: Something has been deleted!")
    
    #Rekursive durch alle Ordner
    for folder in folders:
        index(folder)

def removeEntry(item, indexFilePath):
    print(f"Try to remove {item.name}")
    with open(indexFilePath) as f:
        data = json.load(f)

    if data.pop(item.name, None) is not None:
        print(f"Successfully removed: {item.name}")    
        with open(indexFilePath, 'w') as f:
            json.dump(data, f, indent=4)

def addNewEntry(item, indexFilePath):
    new_entry = {
        item.stem:{
            "format": item.suffix.lower(),
            "tags": [],
            "path": str(indexFilePath.parent / item.name)
        }
    }

    print(f"add new Entry: {new_entry}")

    with open(indexFilePath) as f:
        data = json.load(f)

    data.update(new_entry)

    with open(indexFilePath, 'w') as f:
        json.dump(data, f, indent=4)

def parseThroughIndexFile(file):
    result = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"Parse {key}")
                    result[key] = value

    except Exception as e:
        print(e)

    return result

if __name__ == "__main__":
    main()