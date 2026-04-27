from qtpy.QtWidgets import QWidget
from qtpy import uic
from qtpy.QtCore import Qt

class TagList(QWidget) :
    mainTableView = None

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi("ui/taglist.ui", self)
        self.saveButton.clicked.connect(self.on_save)
    
    def SetUp(self, tagList):
        print(f"SetUp tags: {str(tagList)}")
        self.tagList.setPlainText(str(tagList))

    def on_save(self):
        text = self.tagList.toPlainText()
        index = self.mainTableView.selectionModel().currentIndex()
        targetIndex = index.siblingAtColumn(2)

        if targetIndex.isValid():
            self.mainTableView.model().setData(targetIndex, text, Qt.EditRole)
        else:
            print(f"Erro: Index at row {index.row()} is invalid")

    def setMainTable(self, mainTable):
        self.mainTableView = mainTable

