from PyQt5.QtWidgets import QApplication
from controller import *
import sys

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.showLogin()
    app.exec_()

if __name__ == '__main__':
    main()