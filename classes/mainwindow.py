from qtpy.QtWidgets import QMainWindow, QAbstractItemView, QFileDialog, QMessageBox
from qtpy import uic
from collections import deque
from .datamodel import DataModel
from pathlib import Path
from qtpy.QtCore import Qt, QSortFilterProxyModel
import subprocess


class ProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        return super().filterAcceptsRow(source_row, source_parent)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_model = DataModel({})
        self.proxyModel = ProxyModel()
        self.proxyModel.setSourceModel(self.table_model)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        
        self.ui = uic.loadUi("ui/main.ui", self)     
        self.ui.actionNew_Basket.triggered.connect(self.newBasket)
        self.ui.actionExit.triggered.connect(self.Exit)
        self.ui.actionLoad.triggered.connect(self.loadBasket)

        self.MainTable.setModel(self.proxyModel)
        self.MainTable.setSortingEnabled(True)
        self.MainTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.MainTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.MainTable.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.MainTable.horizontalHeader().hideSection(3)
        self.tagList.setMainTable(self.MainTable)
        self.searchButton.clicked.connect(self.search)

    def loadFolder(self, folderPath):
        index = folderPath / "index.ob"
        queue = deque()

        try:
            self.table_model.load_from_file(index)
        except Exception as e:
            print(f"ERROR: {e}")

        for item in folderPath.iterdir():
            if item.is_dir():
                queue.append(item)

        while queue:
            newFolder = queue.popleft()
            self.loadFolder(newFolder)


    def loadProject(self, path):
        self.table_model.clear()
        self.loadFolder(path.parent)

    def on_selection_changed(self, selected, deselected):
        index = self.MainTable.selectionModel().currentIndex()
        if not index.isValid():
            return
        
        value0 = index.siblingAtColumn(0).data()
        value2 = index.siblingAtColumn(2).data()
        value3 = index.siblingAtColumn(3).data()

        if value3 is None:
            print("Error: The path column for this row is empty.")
            return

        self.inspector.SetUp(Path(str(value3)), str(value0))
        self.tagList.SetUp(str(value2))

    def search(self):
        print(f"Search was clicked with {self.searchEdit.text()}!")
        self.proxyModel.setFilterKeyColumn(-1)
        self.proxyModel.setFilterFixedString(self.searchEdit.text())
        #self.proxyModel.setFilterRegularExpression(self.searchEdit.text())
        self.proxyModel.invalidateFilter()
        return
    
    def Exit(self):
        exit()

    def loadBasket(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select .ob file", 
            "", 
            "Orpheus Basket (*.ob);"
        )
        
        if file_path:
            print(f"Selected file: {file_path}")
            self.loadProject(Path(file_path))

    def newBasket(self):
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Directory to Process", 
            str(Path(__file__).resolve().parent),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            print(f"Selected directory: {directory}")
            self.create(directory)
        else:
            print("Selection cancelled.")

    def create(self, pathString):
        print(f"Create Structure at {pathString}")
        source_folder = Path(pathString)
        path = source_folder / "basketSrc.ob"
        f = open(path, "w")
        if path.exists():
            print("Operation successfull -> created at " + str(path.parent))
            result = subprocess.run(["python", "scripts/index.py", str(path.parent)], capture_output=False, text=True)
            print(f"{result.stdout}")
            if result.stderr:
                print(result.stderr)
        else:
            print("Error")
    
