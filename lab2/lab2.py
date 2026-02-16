import math
import tkinter as tk
from tkinter import ttk, messagebox


class FunctionTableApp(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Лабораторна робота 2: Таблиця значень функції")
        self.geometry("720x400")
        self.minsize(600, 360)

        self.selected_function = tk.StringVar(value="trig")

        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        lbl_choose = ttk.Label(main_frame, text="Оберіть функцію:")
        lbl_choose.grid(row=0, column=0, columnspan=3, sticky="w")

        func_frame = ttk.Frame(main_frame)
        func_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(5, 10))

        rb_trig = ttk.Radiobutton(
            func_frame,
            text="y = 2·sin(x) − cos(x)",
            value="trig",
            variable=self.selected_function,
        )
        rb_trig.grid(row=0, column=0, sticky="w")

        rb_pow = ttk.Radiobutton(
            func_frame,
            text="y = (2^x + 10) / 4 + 9 / 2^(x − 2)",
            value="pow",
            variable=self.selected_function,
        )
        rb_pow.grid(row=1, column=0, sticky="w", pady=(5, 0))

        func_frame.columnconfigure(0, weight=1)

        lbl_a = ttk.Label(main_frame, text="Початок інтервалу (a):")
        lbl_a.grid(row=2, column=0, sticky="w")

        self.entry_a = ttk.Entry(main_frame)
        self.entry_a.grid(row=2, column=1, sticky="ew", padx=(5, 5))

        lbl_b = ttk.Label(main_frame, text="Кінець інтервалу (b):")
        lbl_b.grid(row=3, column=0, sticky="w", pady=(5, 0))

        self.entry_b = ttk.Entry(main_frame)
        self.entry_b.grid(row=3, column=1, sticky="ew", padx=(5, 5), pady=(5, 0))

        lbl_n = ttk.Label(main_frame, text="Кількість точок (n ≥ 2):")
        lbl_n.grid(row=4, column=0, sticky="w", pady=(5, 0))

        self.entry_n = ttk.Entry(main_frame, width=8)
        self.entry_n.grid(row=4, column=1, sticky="w", padx=(5, 5), pady=(5, 0))

        btn_calc = ttk.Button(main_frame, text="Обчислити таблицю", command=self.calculate_table)
        btn_calc.grid(row=5, column=0, columnspan=3, pady=(10, 5), sticky="ew")

        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=0)
        main_frame.rowconfigure(6, weight=1)

        columns = ("index", "x", "y")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("index", text="№")
        self.tree.heading("x", text="x")
        self.tree.heading("y", text="y")

        self.tree.column("index", width=50, anchor="center")
        self.tree.column("x", width=150, anchor="e")
        self.tree.column("y", width=150, anchor="e")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.entry_a.focus()

    @staticmethod
    def _func_trig(x: float) -> float:
        return 2 * math.sin(x) - math.cos(x)

    @staticmethod
    def _func_pow(x: float) -> float:
        return (2 ** x + 10) / 4 + 9 / (2 ** (x - 2))

    def calculate_table(self) -> None:
        raw_a = self.entry_a.get().strip().replace(",", ".")
        raw_b = self.entry_b.get().strip().replace(",", ".")
        raw_n = self.entry_n.get().strip()

        try:
            a = float(raw_a)
            b = float(raw_b)
        except ValueError:
            messagebox.showerror(
                "Помилка вводу",
                "Межі інтервалу a і b повинні бути дійсними числами.",
            )
            return

        try:
            n = int(raw_n)
        except ValueError:
            messagebox.showerror(
                "Помилка вводу",
                "Кількість точок n повинна бути цілим числом.",
            )
            return

        if not a < b:
            messagebox.showerror(
                "Помилка вводу",
                "Ліва межа a повинна бути меншою за праву межу b.",
            )
            return

        if n < 2:
            messagebox.showerror(
                "Помилка вводу",
                "Кількість точок n повинна бути не меншою за 2.",
            )
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        func_key = self.selected_function.get()
        if func_key == "trig":
            func = self._func_trig
            func_text = "y = 2·sin(x) − cos(x)"
        else:
            func = self._func_pow
            func_text = "y = (2^x + 10) / 4 + 9 / 2^(x − 2)"

        step = (b - a) / (n - 1)

        errors: list[str] = []

        for i in range(n):
            x = a + i * step
            try:
                y = func(x)
                y_str = f"{y:.8g}"
            except Exception as exc:
                y_str = "—"
                errors.append(f"x = {x:.8g}: {exc!s}")

            self.tree.insert("", "end", values=(i + 1, f"{x:.8g}", y_str))

        if errors:
            messagebox.showwarning(
                "Виключні ситуації",
                "Під час обчислення в деяких точках виникли проблеми "
                "(розриви або неможливість обчислення).\n"
                "Деталі перших декількох:\n\n" + "\n".join(errors[:5]),
            )
        else:
            messagebox.showinfo(
                "Готово",
                f"Таблиця значень для функції:\n{func_text}\n\n"
                f"Інтервал: [{a}; {b}], кількість точок: {n}.",
            )


def main() -> None:
    app = FunctionTableApp()
    app.mainloop()


if __name__ == "__main__":
    main()

