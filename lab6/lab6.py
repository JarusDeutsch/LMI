import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtWidgets import QApplication


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAB5_DIR = os.path.join(BASE_DIR, "..", "lab5")
if LAB5_DIR not in sys.path:
    sys.path.insert(0, LAB5_DIR)

import lab5 as lab5_module


class MainWindow(lab5_module.MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._add_qml_tab()

    def _add_qml_tab(self) -> None:
        qml_widget = QQuickWidget(self)
        qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)

        qml_path = os.path.join(BASE_DIR, "main.qml")
        qml_widget.setSource(QUrl.fromLocalFile(os.path.abspath(qml_path)))

        self.tabs.addTab(qml_widget, "ЛР 6")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

