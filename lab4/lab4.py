import math
from typing import List, Tuple

from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QRadioButton,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QTabWidget,
    QMenu,
)


def func_trig(x: float) -> float:
    return 2 * math.sin(x) - math.cos(x)


def func_pow(x: float) -> float:
    return (2 ** x + 10) / 4 + 9 / (2 ** (x - 2))


class GraphWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._points: List[Tuple[float, float]] = []

        self._color = QColor("blue")
        self._line_width = 2
        self._pen_style = Qt.SolidLine

        self.setMinimumHeight(200)

    def set_data(self, points: List[Tuple[float, float]]) -> None:
        self._points = points
        self.update()

    def set_line_color(self, color: QColor) -> None:
        self._color = color
        self.update()

    def set_line_width(self, width: int) -> None:
        self._line_width = max(1, width)
        self.update()

    def set_line_style(self, style: Qt.PenStyle) -> None:
        self._pen_style = style
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = self.rect().adjusted(10, 10, -10, -10)

        painter.fillRect(self.rect(), Qt.white)

        painter.setPen(QPen(Qt.lightGray, 1, Qt.SolidLine))
        painter.drawRect(rect)

        if not self._points:
            painter.setPen(Qt.black)
            painter.drawText(
                rect,
                Qt.AlignCenter,
                "Немає даних для відображення.\n"
                "Відкрийте відповідне вікно та виконайте обчислення.",
            )
            return

        xs = [p[0] for p in self._points]
        ys = [p[1] for p in self._points]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        if max_x == min_x:
            max_x += 1.0
            min_x -= 1.0
        if max_y == min_y:
            max_y += 1.0
            min_y -= 1.0

        dx = (max_x - min_x) * 0.05
        dy = (max_y - min_y) * 0.05
        min_x -= dx
        max_x += dx
        min_y -= dy
        max_y += dy

        def map_point(x: float, y: float) -> QPointF:
            px = rect.left() + (x - min_x) / (max_x - min_x) * rect.width()
            py = rect.bottom() - (y - min_y) / (max_y - min_y) * rect.height()
            return QPointF(px, py)

        painter.setPen(QPen(Qt.lightGray, 1, Qt.DashLine))
        if min_x < 0 < max_x:
            x0 = map_point(0, min_y).x()
            painter.drawLine(int(x0), rect.top(), int(x0), rect.bottom())
        if min_y < 0 < max_y:
            y0 = map_point(min_x, 0).y()
            painter.drawLine(rect.left(), int(y0), rect.right(), int(y0))

        pen = QPen(self._color, self._line_width, self._pen_style)
        painter.setPen(pen)

        prev_point = None
        for x, y in self._points:
            p = map_point(x, y)
            if prev_point is not None:
                painter.drawLine(prev_point, p)
            prev_point = p


class SinglePointWindow(QWidget):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Обчислення в одній точці")
        self.resize(400, 220)

        self.selected_function = "trig"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        lbl_choose = QLabel("Оберіть функцію:")
        layout.addWidget(lbl_choose)

        self.rb_trig = QRadioButton("y = 2·sin(x) − cos(x)")
        self.rb_trig.setChecked(True)
        self.rb_trig.toggled.connect(self._on_trig_selected)

        self.rb_pow = QRadioButton("y = (2^x + 10) / 4 + 9 / 2^(x − 2)")
        self.rb_pow.toggled.connect(self._on_pow_selected)

        layout.addWidget(self.rb_trig)
        layout.addWidget(self.rb_pow)

        grid = QGridLayout()
        grid.setHorizontalSpacing(6)
        grid.setVerticalSpacing(4)
        lbl_x = QLabel("Введіть x:")
        self.edit_x = QLineEdit()
        grid.addWidget(lbl_x, 0, 0)
        grid.addWidget(self.edit_x, 0, 1)

        layout.addLayout(grid)

        self.lbl_result = QLabel("Результат: —")
        layout.addWidget(self.lbl_result)

        self.btn_calc = QPushButton("Обчислити")
        self.btn_calc.clicked.connect(self.calculate)
        layout.addWidget(self.btn_calc)

        self.edit_x.setFocus()

    def _on_trig_selected(self, checked: bool) -> None:
        if checked:
            self.selected_function = "trig"

    def _on_pow_selected(self, checked: bool) -> None:
        if checked:
            self.selected_function = "pow"

    def calculate(self) -> None:
        raw_x = self.edit_x.text().strip().replace(",", ".")
        try:
            x = float(raw_x)
        except ValueError:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Будь ласка, введіть коректне числове значення x.",
            )
            return

        if self.selected_function == "trig":
            y = func_trig(x)
            func_text = "y = 2·sin(x) − cos(x)"
        else:
            try:
                y = func_pow(x)
            except OverflowError:
                QMessageBox.critical(
                    self,
                    "Помилка обчислення",
                    "Занадто велике значення. Спробуйте інший x.",
                )
                return
            func_text = "y = (2^x + 10) / 4 + 9 / 2^(x − 2)"

        self.lbl_result.setText(f"Результат: y({x}) = {y:.6g}")

        QMessageBox.information(
            self,
            "Результат обчислення",
            f"Функція: {func_text}\nТочка: x = {x}\nРезультат: y = {y:.6g}",
        )


class TableWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Таблиця значень функції")
        self.resize(700, 400)

        self.selected_function = "trig"

        main_layout = QVBoxLayout(self)

        func_layout = QVBoxLayout()
        lbl_choose = QLabel("Оберіть функцію:")
        func_layout.addWidget(lbl_choose)

        self.rb_trig = QRadioButton("y = 2·sin(x) − cos(x)")
        self.rb_trig.setChecked(True)
        self.rb_trig.toggled.connect(self._on_trig_selected)

        self.rb_pow = QRadioButton("y = (2^x + 10) / 4 + 9 / 2^(x − 2)")
        self.rb_pow.toggled.connect(self._on_pow_selected)

        func_layout.addWidget(self.rb_trig)
        func_layout.addWidget(self.rb_pow)

        main_layout.addLayout(func_layout)

        params_layout = QGridLayout()

        lbl_a = QLabel("Початок інтервалу (a):")
        self.edit_a = QLineEdit()
        lbl_b = QLabel("Кінець інтервалу (b):")
        self.edit_b = QLineEdit()
        lbl_n = QLabel("Кількість точок (n ≥ 2):")
        self.edit_n = QLineEdit()

        params_layout.addWidget(lbl_a, 0, 0)
        params_layout.addWidget(self.edit_a, 0, 1)
        params_layout.addWidget(lbl_b, 1, 0)
        params_layout.addWidget(self.edit_b, 1, 1)
        params_layout.addWidget(lbl_n, 0, 2)
        params_layout.addWidget(self.edit_n, 0, 3)

        main_layout.addLayout(params_layout)

        self.btn_calc = QPushButton("Обчислити таблицю")
        self.btn_calc.clicked.connect(self.calculate_table)
        main_layout.addWidget(self.btn_calc)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["№", "x", "y"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        main_layout.addWidget(self.table)

        self.edit_a.setFocus()

    def _on_trig_selected(self, checked: bool) -> None:
        if checked:
            self.selected_function = "trig"

    def _on_pow_selected(self, checked: bool) -> None:
        if checked:
            self.selected_function = "pow"

    def calculate_table(self) -> None:
        raw_a = self.edit_a.text().strip().replace(",", ".")
        raw_b = self.edit_b.text().strip().replace(",", ".")
        raw_n = self.edit_n.text().strip()

        try:
            a = float(raw_a)
            b = float(raw_b)
        except ValueError:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Межі інтервалу a і b повинні бути дійсними числами.",
            )
            return

        try:
            n = int(raw_n)
        except ValueError:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Кількість точок n повинна бути цілим числом.",
            )
            return

        if not a < b:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Ліва межа a повинна бути меншою за праву межу b.",
            )
            return

        if n < 2:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Кількість точок n повинна бути не меншою за 2.",
            )
            return

        self.table.setRowCount(0)

        if self.selected_function == "trig":
            func = func_trig
            func_text = "y = 2·sin(x) − cos(x)"
        else:
            func = func_pow
            func_text = "y = (2^x + 10) / 4 + 9 / 2^(x − 2)"

        step = (b - a) / (n - 1)
        errors: List[str] = []

        for i in range(n):
            x = a + i * step
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{x:.8g}"))

            try:
                y = func(x)
                self.table.setItem(row, 2, QTableWidgetItem(f"{y:.8g}"))
            except Exception as exc:
                self.table.setItem(row, 2, QTableWidgetItem("—"))
                errors.append(f"x = {x:.8g}: {exc!s}")

        if errors:
            QMessageBox.warning(
                self,
                "Виключні ситуації",
                "Під час обчислення в деяких точках виникли проблеми "
                "(розриви або неможливість обчислення).\n"
                "Деталі перших декількох:\n\n" + "\n".join(errors[:5]),
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                f"Таблиця значень для функції:\n{func_text}\n\n"
                f"Інтервал: [{a}; {b}], кількість точок: {n}.",
            )


class GraphWindow(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("ЛР 3:Графік функції")
        self.resize(900, 600)

        self.selected_function = "trig"

        main_layout = QVBoxLayout(self)

        func_layout = QVBoxLayout()
        lbl_choose = QLabel("Оберіть функцію:")
        func_layout.addWidget(lbl_choose)

        self.rb_trig = QRadioButton("y = 2·sin(x) − cos(x)")
        self.rb_trig.setChecked(True)
        self.rb_trig.toggled.connect(self._on_trig_selected)

        self.rb_pow = QRadioButton("y = (2^x + 10) / 4 + 9 / 2^(x − 2)")
        self.rb_pow.toggled.connect(self._on_pow_selected)

        func_layout.addWidget(self.rb_trig)
        func_layout.addWidget(self.rb_pow)

        main_layout.addLayout(func_layout)

        params_layout = QGridLayout()

        lbl_a = QLabel("Початок інтервалу (a):")
        self.edit_a = QLineEdit()
        lbl_b = QLabel("Кінець інтервалу (b):")
        self.edit_b = QLineEdit()
        lbl_n = QLabel("Кількість точок (n ≥ 2):")
        self.edit_n = QLineEdit()

        params_layout.addWidget(lbl_a, 0, 0)
        params_layout.addWidget(self.edit_a, 0, 1)
        params_layout.addWidget(lbl_b, 1, 0)
        params_layout.addWidget(self.edit_b, 1, 1)
        params_layout.addWidget(lbl_n, 0, 2)
        params_layout.addWidget(self.edit_n, 0, 3)

        main_layout.addLayout(params_layout)

        style_layout = QHBoxLayout()

        lbl_color = QLabel("Колір лінії:")
        self.color_combo = QComboBox()
        self.color_combo.addItems(["Синій", "Червоний", "Зелений", "Чорний"])

        lbl_width = QLabel("Товщина лінії:")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10)
        self.width_spin.setValue(2)

        lbl_style = QLabel("Стиль лінії:")
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Суцільна", "Штрихова", "Пунктирна", "Штрих-пунктир"])

        style_layout.addWidget(lbl_color)
        style_layout.addWidget(self.color_combo)
        style_layout.addSpacing(20)
        style_layout.addWidget(lbl_width)
        style_layout.addWidget(self.width_spin)
        style_layout.addSpacing(20)
        style_layout.addWidget(lbl_style)
        style_layout.addWidget(self.style_combo)
        style_layout.addStretch()

        main_layout.addLayout(style_layout)

        self.btn_calc = QPushButton("Обчислити таблицю та побудувати графік")
        self.btn_calc.clicked.connect(self.calculate_and_plot)
        main_layout.addWidget(self.btn_calc)

        bottom_layout = QHBoxLayout()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["№", "x", "y"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        self.graph_widget = GraphWidget()

        self.color_combo.currentIndexChanged.connect(self._update_graph_style)
        self.width_spin.valueChanged.connect(self._update_graph_style)
        self.style_combo.currentIndexChanged.connect(self._update_graph_style)

        bottom_layout.addWidget(self.table, stretch=1)
        bottom_layout.addWidget(self.graph_widget, stretch=1)

        main_layout.addLayout(bottom_layout, stretch=1)

        self.edit_a.setFocus()

    def _on_trig_selected(self, checked: bool) -> None:
        if checked:
            self.selected_function = "trig"

    def _on_pow_selected(self, checked: bool) -> None:
        if checked:
            self.selected_function = "pow"

    def _update_graph_style(self) -> None:
        color_text = self.color_combo.currentText()
        if color_text == "Синій":
            color = QColor("blue")
        elif color_text == "Червоний":
            color = QColor("red")
        elif color_text == "Зелений":
            color = QColor("green")
        else:
            color = QColor("black")

        self.graph_widget.set_line_color(color)
        self.graph_widget.set_line_width(self.width_spin.value())

        style_text = self.style_combo.currentText()
        if style_text == "Суцільна":
            style = Qt.SolidLine
        elif style_text == "Штрихова":
            style = Qt.DashLine
        elif style_text == "Пунктирна":
            style = Qt.DotLine
        else:
            style = Qt.DashDotLine

        self.graph_widget.set_line_style(style)

    def calculate_and_plot(self) -> None:
        raw_a = self.edit_a.text().strip().replace(",", ".")
        raw_b = self.edit_b.text().strip().replace(",", ".")
        raw_n = self.edit_n.text().strip()

        try:
            a = float(raw_a)
            b = float(raw_b)
        except ValueError:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Межі інтервалу a і b повинні бути дійсними числами.",
            )
            return

        try:
            n = int(raw_n)
        except ValueError:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Кількість точок n повинна бути цілим числом.",
            )
            return

        if not a < b:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Ліва межа a повинна бути меншою за праву межу b.",
            )
            return

        if n < 2:
            QMessageBox.critical(
                self,
                "Помилка вводу",
                "Кількість точок n повинна бути не меншою за 2.",
            )
            return

        self.table.setRowCount(0)

        if self.selected_function == "trig":
            func = func_trig
            func_text = "y = 2·sin(x) − cos(x)"
        else:
            func = func_pow
            func_text = "y = (2^x + 10) / 4 + 9 / 2^(x − 2)"

        step = (b - a) / (n - 1)
        points_for_graph: List[Tuple[float, float]] = []
        errors: List[str] = []

        for i in range(n):
            x = a + i * step
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{x:.8g}"))

            try:
                y = func(x)
                y_str = f"{y:.8g}"
                self.table.setItem(row, 2, QTableWidgetItem(y_str))
                points_for_graph.append((x, y))
            except Exception as exc:
                self.table.setItem(row, 2, QTableWidgetItem("—"))
                errors.append(f"x = {x:.8g}: {exc!s}")

        self.graph_widget.set_data(points_for_graph)

        if errors:
            QMessageBox.warning(
                self,
                "Виключні ситуації",
                "Під час обчислення в деяких точках виникли проблеми "
                "(розриви або неможливість обчислення).\n"
                "Деталі перших декількох:\n\n" + "\n".join(errors[:5]),
            )
        else:
            QMessageBox.information(
                self,
                "Готово",
                f"Таблиця значень та графік для функції:\n{func_text}\n\n"
                f"Інтервал: [{a}; {b}], кількість точок: {n}.",
            )


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Лабораторна робота 4: Багатовіконний інтерфейс")
        self.resize(900, 650)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        top_layout = QHBoxLayout()
        lbl_title = QLabel("Режими в окремих вікнах:")
        top_layout.addWidget(lbl_title)

        self.btn_single = QPushButton("Одна точка")
        self.btn_table = QPushButton("Таблиця")
        self.btn_graph = QPushButton("Графік")

        self.btn_single.clicked.connect(self.open_single_point_window)
        self.btn_table.clicked.connect(self.open_table_window)
        self.btn_graph.clicked.connect(self.open_graph_window)

        top_layout.addWidget(self.btn_single)
        top_layout.addWidget(self.btn_table)
        top_layout.addWidget(self.btn_graph)
        top_layout.addStretch()

        layout.addLayout(top_layout)

        self.tabs = QTabWidget()
        self.single_tab = SinglePointWindow(self)
        self.table_tab = TableWindow(self)
        self.graph_tab = GraphWindow(self)

        self.tabs.addTab(self.single_tab, "ЛР 1: Обчислення в одній точці")
        self.tabs.addTab(self.table_tab, "ЛР 2: Таблиця значень")
        self.tabs.addTab(self.graph_tab, "ЛР 3: Графік функції")

        layout.addWidget(self.tabs, stretch=1)

        tab_bar = self.tabs.tabBar()
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(self._on_tab_context_menu)

        self._detached_windows: list[QWidget] = []

        self._single_window: SinglePointWindow | None = None
        self._table_window: TableWindow | None = None
        self._graph_window: GraphWindow | None = None

    def _show_child(self, window_attr: str, window_cls) -> None:
        window = getattr(self, window_attr)
        if window is None or not isinstance(window, QWidget) or not window.isVisible():
            window = window_cls()
            setattr(self, window_attr, window)
        window.show()
        window.raise_()
        window.activateWindow()

    def open_single_point_window(self) -> None:
        self._show_child("_single_window", SinglePointWindow)

    def open_table_window(self) -> None:
        self._show_child("_table_window", TableWindow)

    def open_graph_window(self) -> None:
        self._show_child("_graph_window", GraphWindow)

    def _on_tab_context_menu(self, pos: QPoint) -> None:
        tab_bar = self.tabs.tabBar()
        index = tab_bar.tabAt(pos)
        if index < 0:
            return

        menu = QMenu(self)
        detach_action = menu.addAction("Відкрити в окремому вікні")
        chosen = menu.exec_(tab_bar.mapToGlobal(pos))

        if chosen is detach_action:
            if index == 0:
                win_cls = SinglePointWindow
            elif index == 1:
                win_cls = TableWindow
            else:
                win_cls = GraphWindow

            win = win_cls()
            self._detached_windows.append(win)
            win.show()


def main() -> None:
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

