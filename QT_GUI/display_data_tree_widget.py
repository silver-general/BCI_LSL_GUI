import sys
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
        "Project B": ["file_b.csv", "photo.jpg"],
        "Project C": []}

app = QApplication()

tree = QTreeWidget()
tree.setColumnCount(2)
tree.setHeaderLabels(["Name", "Type"])

items = []
# iterate over the data dictionary
for key, values in data.items():
    # create a treewidgetitem whose name is the data key (ProjectA,ProjectB,ProjectC)
    item = QTreeWidgetItem([key])
    # for each key, there are some files in the folder
    for value in values:
        # extract file extention
        ext = value.split(".")[-1].upper()
        # create another tree widget item, add it as a child to the superior
        child = QTreeWidgetItem([value, ext])
        item.addChild(child)
    items.append(item)

tree.insertTopLevelItems(0, items)

tree.show()
sys.exit(app.exec())
