import json
import math
import os
from typing import List, Tuple, Any, Dict

from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
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
    QAction,
    QFileDialog,
    QDialog,
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
                "Введіть параметри і виконайте обчислення.",
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

    def get_state(self) -> Dict[str, Any]:
        return {
            "selected_function": self.selected_function,
            "x": self.edit_x.text(),
            "result_text": self.lbl_result.text(),
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        func = state.get("selected_function", "trig")
        if func == "trig":
            self.rb_trig.setChecked(True)
        else:
            self.rb_pow.setChecked(True)
        self.edit_x.setText(state.get("x", ""))
        self.lbl_result.setText(state.get("result_text", "Результат: —"))


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

    def get_state(self) -> Dict[str, Any]:
        rows: List[List[str]] = []
        for r in range(self.table.rowCount()):
            row_vals: List[str] = []
            for c in range(3):
                item = self.table.item(r, c)
                row_vals.append(item.text() if item is not None else "")
            rows.append(row_vals)

        return {
            "selected_function": self.selected_function,
            "a": self.edit_a.text(),
            "b": self.edit_b.text(),
            "n": self.edit_n.text(),
            "rows": rows,
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        func = state.get("selected_function", "trig")
        if func == "trig":
            self.rb_trig.setChecked(True)
        else:
            self.rb_pow.setChecked(True)

        self.edit_a.setText(state.get("a", ""))
        self.edit_b.setText(state.get("b", ""))
        self.edit_n.setText(state.get("n", ""))

        self.table.setRowCount(0)
        for row_vals in state.get("rows", []):
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c in range(min(3, len(row_vals))):
                self.table.setItem(row, c, QTableWidgetItem(row_vals[c]))


class GraphWindow(QWidget):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Графік функції")
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

    def get_state(self) -> Dict[str, Any]:
        rows: List[List[str]] = []
        for r in range(self.table.rowCount()):
            row_vals: List[str] = []
            for c in range(3):
                item = self.table.item(r, c)
                row_vals.append(item.text() if item is not None else "")
            rows.append(row_vals)

        return {
            "selected_function": self.selected_function,
            "a": self.edit_a.text(),
            "b": self.edit_b.text(),
            "n": self.edit_n.text(),
            "rows": rows,
            "color_index": self.color_combo.currentIndex(),
            "width": self.width_spin.value(),
            "style_index": self.style_combo.currentIndex(),
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        func = state.get("selected_function", "trig")
        if func == "trig":
            self.rb_trig.setChecked(True)
        else:
            self.rb_pow.setChecked(True)

        self.edit_a.setText(state.get("a", ""))
        self.edit_b.setText(state.get("b", ""))
        self.edit_n.setText(state.get("n", ""))

        self.color_combo.setCurrentIndex(int(state.get("color_index", 0)))
        self.width_spin.setValue(int(state.get("width", 2)))
        self.style_combo.setCurrentIndex(int(state.get("style_index", 0)))
        self._update_graph_style()

        self.table.setRowCount(0)
        for row_vals in state.get("rows", []):
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c in range(min(3, len(row_vals))):
                self.table.setItem(row, c, QTableWidgetItem(row_vals[c]))

        points: List[Tuple[float, float]] = []
        for r in range(self.table.rowCount()):
            item_x = self.table.item(r, 1)
            item_y = self.table.item(r, 2)
            if item_x is None or item_y is None:
                continue
            try:
                x = float(item_x.text())
                y = float(item_y.text())
            except ValueError:
                continue
            points.append((x, y))
        self.graph_widget.set_data(points)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Сєргєєв 6.1212-1")
        self.resize(900, 650)

        self.current_file: str | None = None

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

        self.tabs.addTab(self.single_tab, "ЛР 1:Обчислення в одній точці")
        self.tabs.addTab(self.table_tab, "ЛР 2: Таблиця значень")
        self.tabs.addTab(self.graph_tab, "ЛР 3: Графік функції")

        layout.addWidget(self.tabs, stretch=1)

        tab_bar = self.tabs.tabBar()
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(self._on_tab_context_menu)

        self._detached_windows: List[QWidget] = []
        self._other_main_windows: List["MainWindow"] = []

        self._single_window: SinglePointWindow | None = None
        self._table_window: TableWindow | None = None
        self._graph_window: GraphWindow | None = None

        self._create_file_menu()

    def _create_file_menu(self) -> None:
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Файл")

        new_act = QAction("Нове вікно", self)
        new_act.setShortcut("Ctrl+N")
        new_act.triggered.connect(self.create_new_window)
        file_menu.addAction(new_act)

        open_act = QAction("Відкрити…", self)
        open_act.setShortcut("Ctrl+O")
        open_act.triggered.connect(self.open_file)
        file_menu.addAction(open_act)

        save_act = QAction("Зберегти", self)
        save_act.setShortcut("Ctrl+S")
        save_act.triggered.connect(self.save_file)
        file_menu.addAction(save_act)

        save_as_act = QAction("Зберегти як…", self)
        save_as_act.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_act)

        file_menu.addSeparator()

        print_act = QAction("Друк таблиці…", self)
        print_act.setShortcut("Ctrl+P")
        print_act.triggered.connect(self.print_table)
        file_menu.addAction(print_act)

        file_menu.addSeparator()

        exit_act = QAction("Вихід", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

    def _collect_state(self) -> Dict[str, Any]:
        return {
            "active_tab": self.tabs.currentIndex(),
            "single": self.single_tab.get_state(),
            "table": self.table_tab.get_state(),
            "graph": self.graph_tab.get_state(),
        }

    def _apply_state(self, state: Dict[str, Any]) -> None:
        self.single_tab.set_state(state.get("single", {}))
        self.table_tab.set_state(state.get("table", {}))
        self.graph_tab.set_state(state.get("graph", {}))
        active = int(state.get("active_tab", 0))
        if 0 <= active < self.tabs.count():
            self.tabs.setCurrentIndex(active)

    def create_new_window(self) -> None:
        new_win = MainWindow()
        self._other_main_windows.append(new_win)
        new_win.show()

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Відкрити файл стану",
            "",
            "Файли стану (*.json);;Усі файли (*.*)",
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Помилка відкриття",
                f"Не вдалося відкрити файл:\n{path}\n\n{exc}",
            )
            return

        self._apply_state(state)
        self.current_file = path
        self._update_title_with_filename()

    def save_file(self) -> None:
        if not self.current_file:
            self.save_file_as()
            return
        self._save_to_path(self.current_file)

    def save_file_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Зберегти файл стану як",
            "",
            "Файли стану (*.json);;Усі файли (*.*)",
        )
        if not path:
            return
        if not os.path.splitext(path)[1]:
            path += ".json"

        self._save_to_path(path)
        self.current_file = path
        self._update_title_with_filename()

    def _save_to_path(self, path: str) -> None:
        state = self._collect_state()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Помилка збереження",
                f"Не вдалося зберегти файл:\n{path}\n\n{exc}",
            )

    def _update_title_with_filename(self) -> None:
        if self.current_file:
            name = os.path.basename(self.current_file)
            self.setWindowTitle(f"Сєргєєв 6.1212-1 — {name}")
        else:
            self.setWindowTitle("Сєргєєв 6.1212-1")

    def print_table(self) -> None:
        idx = self.tabs.currentIndex()
        table_widget: QTableWidget | None
        table_widget: QTableWidget | None
        if idx == 1:
            table_widget = self.table_tab.table
        elif idx == 2:
            table_widget = self.graph_tab.table
        else:
            QMessageBox.information(
                self,
                "Друк таблиці",
                'Для друку виберіть вкладку з таблицею значень ("Таблиця" або "Графік").',
            )
            return

        if table_widget.rowCount() == 0 or table_widget.columnCount() == 0:
            QMessageBox.information(
                self,
                "Друк таблиці",
                "Таблиця порожня, нічого друкувати.",
            )
            return

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("Друк таблиці значень")

        if dialog.exec_() != QDialog.Accepted:
            return

        painter = QPainter(printer)
        if not painter.isActive():
            return

        page_rect = printer.pageRect()

        margin_left = 20
        margin_top = 20
        margin_right = 20
        margin_bottom = 20

        left = page_rect.left() + margin_left
        top = page_rect.top() + margin_top
        right = page_rect.right() - margin_right
        bottom = page_rect.bottom() - margin_bottom

        usable_width = max(0, right - left)
        usable_height = max(0, bottom - top)

        if usable_width <= 0 or usable_height <= 0:
            painter.end()
            return

        header = table_widget.horizontalHeader()
        v_header = table_widget.verticalHeader()

        column_count = table_widget.columnCount()
        row_count = table_widget.rowCount()

        col_widths = [header.sectionSize(c) for c in range(column_count)]
        total_col_width = sum(col_widths) or 1

        scale_x = usable_width / total_col_width
        col_widths = [w * scale_x for w in col_widths]

        base_header_height = header.height()
        base_row_height = v_header.defaultSectionSize()

        header_height = base_header_height * scale_x
        row_height = base_row_height * scale_x

        rows_per_page = max(
            1, int((usable_height - header_height) // max(1.0, row_height))
        )

        current_row = 0
        first_page = True

        while current_row < row_count:
            if not first_page:
                printer.newPage()
            first_page = False

            y = float(top)

            x = float(left)
            for c in range(column_count):
                w = col_widths[c]
                rect = QRectF(x, y, w, header_height)
                painter.drawRect(rect)
                header_item = header.model().headerData(
                    c, Qt.Horizontal, Qt.DisplayRole
                )
                text = str(header_item) if header_item is not None else ""
                painter.drawText(rect, Qt.AlignCenter, text)
                x += w

            y += header_height

            rows_drawn = 0
            while (
                current_row < row_count
                and rows_drawn < rows_per_page
                and y + row_height <= bottom
            ):
                x = float(left)
                for c in range(column_count):
                    w = col_widths[c]
                    rect = QRectF(x, y, w, row_height)
                    painter.drawRect(rect)
                    item = table_widget.item(current_row, c)
                    text = item.text() if item is not None else ""
                    text_rect = rect.adjusted(2, 0, -2, 0)
                    painter.drawText(
                        text_rect, Qt.AlignVCenter | Qt.AlignLeft, text
                    )
                    x += w

                y += row_height
                current_row += 1
                rows_drawn += 1

        painter.end()

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

