import sys

import jsonpickle
import qdarkstyle
from PyQt5.QtWidgets import QApplication

from notes.ui.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow(None)

    app_settings_path = "app_settings.json"

    with open(app_settings_path, "r") as f:
        app_settings = jsonpickle.decode(f.read())

    if app_settings["app_theme"] == "dark":
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    window.show()

    app.exec_()


if __name__ == "__main__":
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    main()
