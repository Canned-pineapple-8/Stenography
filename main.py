import sys
from PyQt5.QtWidgets import QApplication
from ui import SteganographyApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())


