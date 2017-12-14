import sys
from PyQt5 import QtWidgets

from chat_window import ChatWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = ChatWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
