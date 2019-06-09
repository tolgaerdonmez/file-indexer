from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QMessageBox
import shutil, os
from pathlib import Path
from indexer import Indexer 
import json

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.indexer = Indexer()
        self.source = None
        self.destination = None
        self.init_ui()
        self.load()

    def init_ui(self):
        
        # WIDGETS
        browse_btn = QPushButton("Browse")
        dest_btn = QPushButton("Browse")
        add_btn = QPushButton("Add")
        order_btn = QPushButton("Order Files")
        self.file_label = QLabel("Select a file to add")
        self.dest_label = QLabel("Select Indexing Destination")
        self.index_input = QLineEdit()
        self.index_input.setPlaceholderText("Enter the index of the new file")

        # LAYOUTS
        dest_box = QHBoxLayout()
        browse_box = QHBoxLayout()
        input_box = QHBoxLayout()
        vbox = QVBoxLayout()

        # Setting elements

        # destination box layout
        dest_box.addWidget(self.dest_label)
        dest_box.addStretch()
        dest_box.addWidget(dest_btn)

        # browse box layout
        browse_box.addWidget(self.file_label)
        browse_box.addStretch()
        browse_box.addWidget(browse_btn)

        # input box layout
        input_box.addWidget(self.index_input)
        input_box.addWidget(add_btn)

        # VBox layout
        vbox.addStretch()
        vbox.addLayout(dest_box)
        vbox.addLayout(browse_box)
        vbox.addLayout(input_box)
        vbox.addWidget(order_btn)
        vbox.addStretch()

        # Events
        browse_btn.clicked.connect(self.select_new)
        dest_btn.clicked.connect(self.select_dest)
        add_btn.clicked.connect(self.add_file)
        order_btn.clicked.connect(self.order)

        self.setLayout(vbox)
        self.setWindowTitle("File Indexer")
        self.setGeometry(400,200,350,150)
        self.show()

    def load(self):
        try:
            with open("conf.json","r") as file:
                loads = json.load(file)
                self.destination = loads["last_dest"]
                self.dest_label.setText(self.destination)
                self.indexer.path = self.destination
        except:
            pass
              
    def select_new(self):
        file = QFileDialog.getOpenFileName(self,'Select File to Add')
        self.source = file[0]
        self.file_label.setText(file[0])
    
    def select_dest(self):
        file = QFileDialog.getExistingDirectory(self,'Select Indexing Destination')
        if file == "":
            return False
        self.destination = file
        self.dest_label.setText(file)

        self.indexer.path = self.destination
        
        with open("conf.json","w") as file:
            loads = {"last_dest":self.destination}
            json.dump(loads,file)

    def add_file(self):
        try:
            shutil.copy(self.source, self.destination, follow_symlinks=True)
        except:
            pass
        
        self.indexer.index()
        self.indexer.increment(int(self.index_input.text()))
        
        msg_box = QMessageBox.about(self, "Status", "File Added !")

        self.clear()

    def clear(self):
        self.file_label.setText("Select a file to add")
        self.index_input.clear()

    def order(self):
        self.indexer.index()
        self.indexer.order_rename()
        msg_box = QMessageBox.about(self, "Status", "Files are now in order !")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
        