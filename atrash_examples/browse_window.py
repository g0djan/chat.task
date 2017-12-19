import sys
import os
from PyQt5 import QtWidgets

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QPlainTextEdit, QGridLayout, QLabel


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = BrowseWindow()
    window.show()

    sys.exit(app.exec_())

class BrowseWindow(QWidget):
    def __init__(self):
        super(BrowseWindow, self).__init__()
        self.setGeometry(600, 300, 400, 200)
        #btn = QPushButton('Browse', self)
        layout = QGridLayout()
        label = QLabel()
        label.setText('kek')
        layout.addWidget(label, 0, 0)
        label2 = QLabel('yo')
        layout.addWidget(label2, 0, 1)
        self.setLayout(layout)
        #btn.clicked.connect(self.open_finder)

        self.show()

    def open_finder(self):
        #f = QFileDialog.getOpenFileNames(self, 'Choose file', QDir.currentPath(), 'All files (*.*)')
        f = QFileDialog.getExistingDirectory(self, 'Choose directory', QDir.currentPath())
        # print(os.path.join('C:/Users/godja/OneDrive/Study', 'kek.txt'))
        print(f)
        # print(os.path.split(f[0][0])[1])
        # with open(f[0][0], 'rb') as f:
        #     content = f.read()
        # print(content)





if __name__ == '__main__':
    main()
