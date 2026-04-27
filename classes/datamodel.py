from qtpy.QtCore import QAbstractTableModel, Qt
import json
from pathlib import Path

class DataModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = [list(item) for item in data.items()]
        self._headers = ["Filename", "Format", "Tags", "Path"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 4
    
    def data(self, ModelIndex, role=Qt.DisplayRole):
        if not ModelIndex.isValid():
            return None
        
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = ModelIndex.row()
            col = ModelIndex.column()
            
            row_data = self._data[row]

            if col == 0:
                return row_data[0]
            elif col == 1:
                return row_data[1]["format"]
            elif col == 2:
                tagList = list(row_data[1]["tags"])
                return ", ".join(tagList)
            elif col == 3:
                return row_data[1]["path"]
                
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False    

        row = index.row()
        col = index.column()
        row_data = self._data[row]
        metadata = row_data[1]

        if col == 1:
            metadata["format"] = value
        elif col == 2:
            metadata["tags"] = [t.strip() for t in value.split(",")]
        elif col == 3:
            metadata["path"] = value
        else:
            return False

        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        indexPath = Path(metadata["path"]).parent / "index.ob"
        self.updateEntry(indexPath, row_data[0], [t.strip() for t in value.split(",")])
        return True

    def update_data(self, new_data):
        print(f"update")
        self.beginResetModel()
        self._data = [list(item) for item in new_data.items()]
        self.endResetModel()

    def clear(self):
        self._data = []

    def load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            new_data = json.load(f)

        complete_data = self._data + [list(item) for item in new_data.items()]

        self.beginResetModel()
        self._data = complete_data
        self.endResetModel()
        print("Load Finished!")

    def updateEntry(self, indexFilePath : Path, name, newValue : list):
        print(f"Try to update with {str(indexFilePath)}, {name}, {newValue}")

        if not isinstance(newValue, list):
            print("ERROR")
            return

        with open(indexFilePath, 'r') as f:
            data = json.load(f)

        print(f"Loaded {data}")

        for n in data:
            print(f"Check {n} == {name}")
            if n == name:
                print(f"Found {data[n]} update {data[n]["tags"]} with {newValue}")
                data[n]["tags"] = newValue
                break
        
        with open(indexFilePath, 'w') as f:
            updated_json = json.dump(data, f, indent=4)
        print(updated_json)
