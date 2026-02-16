import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtWidgets import QApplication


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAB7_DIR = os.path.join(BASE_DIR, "..", "lab7")
if LAB7_DIR not in sys.path:
    sys.path.insert(0, LAB7_DIR)

import lab7 as lab7_module


class MainWindow(lab7_module.MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._add_lab8_tab()

    def _add_lab8_tab(self) -> None:
        qml_widget = QQuickWidget(self)
        qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)

        qml_path = os.path.join(BASE_DIR, "main.qml")
        qml_widget.setSource(QUrl.fromLocalFile(os.path.abspath(qml_path)))

        engine = qml_widget.engine()
        if engine is not None and QApplication.instance() is not None:
            engine.quit.connect(QApplication.instance().quit)

        self.tabs.addTab(qml_widget, "ЛР 8")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

