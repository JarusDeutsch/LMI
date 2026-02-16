import math
import tkinter as tk
from tkinter import ttk, messagebox


class FunctionCalculatorApp(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Лабораторна робота 1: Обчислення функції")
        self.geometry("640x260")
        self.minsize(520, 220)

        self.selected_function = tk.StringVar(value="trig")

        self.result_labels: dict[str, ttk.Label] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        lbl_choose = ttk.Label(main_frame, text="Оберіть функцію:")
        lbl_choose.grid(row=0, column=0, columnspan=2, sticky="w")

        func_frame = ttk.Frame(main_frame)
        func_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(5, 10))

        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        rb_trig = ttk.Radiobutton(
            func_frame,
            text="y = 2·sin(x) − cos(x)",
            value="trig",
            variable=self.selected_function,
        )
        rb_trig.grid(row=0, column=0, sticky="w")

        lbl_res_trig = ttk.Label(func_frame, text="Результат: —")
        lbl_res_trig.grid(row=0, column=1, sticky="w", padx=(10, 0))

        rb_pow = ttk.Radiobutton(
            func_frame,
            text="y = (2^x + 10) / 4 + 9 / 2^(x − 2)",
            value="pow",
            variable=self.selected_function,
        )
        rb_pow.grid(row=1, column=0, sticky="w", pady=(5, 0))

        lbl_res_pow = ttk.Label(func_frame, text="Результат: —")
        lbl_res_pow.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))

        func_frame.columnconfigure(0, weight=1)
        func_frame.columnconfigure(1, weight=1)

        self.result_labels["trig"] = lbl_res_trig
        self.result_labels["pow"] = lbl_res_pow

        lbl_x = ttk.Label(main_frame, text="Введіть x:")
        lbl_x.grid(row=2, column=0, sticky="w")

        self.entry_x = ttk.Entry(main_frame)
        self.entry_x.grid(row=2, column=1, sticky="ew", padx=(5, 0))
        self.entry_x.focus()

        btn_calc = ttk.Button(main_frame, text="Обчислити", command=self.calculate)
        btn_calc.grid(row=3, column=0, columnspan=2, pady=(10, 0))

    @staticmethod
    def _func_trig(x: float) -> float:
        return 2 * math.sin(x) - math.cos(x)

    @staticmethod
    def _func_pow(x: float) -> float:
        return (2 ** x + 10) / 4 + 9 / (2 ** (x - 2))

    def calculate(self) -> None:
        raw_x = self.entry_x.get().strip().replace(",", ".")
        try:
            x = float(raw_x)
        except ValueError:
            messagebox.showerror(
                "Помилка вводу",
                "Будь ласка, введіть коректне числове значення x.",
            )
            return

        func_key = self.selected_function.get()

        if func_key == "trig":
            y = self._func_trig(x)
            func_text = "y = 2·sin(x) − cos(x)"
        else:
            try:
                y = self._func_pow(x)
            except OverflowError:
                messagebox.showerror(
                    "Помилка обчислення",
                    "Занадто велике значення. Спробуйте інший x.",
                )
                return
            func_text = "y = (2^x + 10) / 4 + 9 / 2^(x − 2)"

        self.result_labels[func_key].configure(
            text=f"Результат: y({x}) = {y:.6g}"
        )

        message = (
            f"Функція: {func_text}\n"
            f"Точка: x = {x}\n"
            f"Результат: y = {y:.6g}"
        )
        messagebox.showinfo("Результат обчислення", message)


def main() -> None:
    app = FunctionCalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()

