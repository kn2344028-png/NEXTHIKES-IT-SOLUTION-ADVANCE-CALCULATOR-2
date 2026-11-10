
import tkinter as tk
from tkinter import ttk
import ast
import math
import operator
import re


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("520x740")
        self.root.minsize(400, 600)

        self.dark = True
        self.angle_mode = "DEG"
        self.expression = tk.StringVar()
        self.history = []

        self.colors = {}
        self.setup_theme()
        self.build_ui()
        self.bind_keys()
        self.update_display()

    def setup_theme(self):
        if self.dark:
            self.colors = {
                "bg": "#111827",
                "panel": "#1F2937",
                "display": "#0B1220",
                "text": "#F9FAFB",
                "muted": "#9CA3AF",
                "button": "#374151",
                "operator": "#2563EB",
                "function": "#4B5563",
                "equal": "#059669",
                "danger": "#DC2626",
                "border": "#374151",
            }
        else:
            self.colors = {
                "bg": "#F3F4F6",
                "panel": "#FFFFFF",
                "display": "#E5E7EB",
                "text": "#111827",
                "muted": "#6B7280",
                "button": "#E5E7EB",
                "operator": "#BFDBFE",
                "function": "#D1D5DB",
                "equal": "#6EE7B7",
                "danger": "#FCA5A5",
                "border": "#D1D5DB",
            }

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.colors["bg"])

        header = tk.Frame(self.root, bg=self.colors["bg"])
        header.pack(fill="x", padx=12, pady=(12, 4))

        tk.Label(
            header,
            text="SCIENTIFIC CALCULATOR",
            font=("Segoe UI", 15, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(side="left")

        tk.Button(
            header,
            text="☀ / ☾",
            command=self.toggle_theme,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            relief="flat",
            padx=10
        ).pack(side="right")

        self.mode_label = tk.Label(
            self.root,
            text="DEG MODE",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["muted"]
        )
        self.mode_label.pack(anchor="w", padx=16, pady=3)

        display_frame = tk.Frame(
            self.root,
            bg=self.colors["display"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        display_frame.pack(fill="x", padx=12, pady=8)

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("Consolas", 24),
            justify="right",
            bg=self.colors["display"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            bd=0
        )
        self.display.pack(fill="x", padx=12, pady=(15, 8), ipady=10)

        self.result_label = tk.Label(
            display_frame,
            text="Ready",
            font=("Segoe UI", 12),
            anchor="e",
            bg=self.colors["display"],
            fg=self.colors["muted"]
        )
        self.result_label.pack(fill="x", padx=12, pady=(0, 12))

        utility = tk.Frame(self.root, bg=self.colors["bg"])
        utility.pack(fill="x", padx=12, pady=3)

        self.make_button(
            utility, "DEG / RAD", self.toggle_angle,
            self.colors["function"]
        ).pack(side="left", expand=True, fill="x", padx=2)

        self.make_button(
            utility, "History", self.show_history,
            self.colors["function"]
        ).pack(side="left", expand=True, fill="x", padx=2)

        self.make_button(
            utility, "Clear", self.clear,
            self.colors["danger"]
        ).pack(side="left", expand=True, fill="x", padx=2)

        grid = tk.Frame(self.root, bg=self.colors["bg"])
        grid.pack(fill="both", expand=True, padx=10, pady=8)

        buttons = [
            [("sin", "sin(", "function"), ("cos", "cos(", "function"),
             ("tan", "tan(", "function"), ("√", "sqrt(", "function"),
             ("x²", "**2", "function")],
            [("asin", "asin(", "function"), ("acos", "acos(", "function"),
             ("atan", "atan(", "function"), ("ln", "ln(", "function"),
             ("log", "log(", "function")],
            [("π", "pi", "function"), ("e", "e", "function"),
             ("(", "(", "function"), (")", ")", "function"),
             ("÷", "/", "operator")],
            [("7", "7", "number"), ("8", "8", "number"),
             ("9", "9", "number"), ("×", "*", "operator"),
             ("⌫", "BACK", "danger")],
            [("4", "4", "number"), ("5", "5", "number"),
             ("6", "6", "number"), ("−", "-", "operator"),
             ("%", "%", "operator")],
            [("1", "1", "number"), ("2", "2", "number"),
             ("3", "3", "number"), ("+", "+", "operator"),
             ("!", "fact(", "function")],
            [("0", "0", "number"), (".", ".", "number"),
             ("EXP", "exp(", "function"), ("Ans", "ANS", "function"),
             ("=", "EQUAL", "equal")],
        ]

        for r, row in enumerate(buttons):
            grid.rowconfigure(r, weight=1)
            for c, (label, value, kind) in enumerate(row):
                grid.columnconfigure(c, weight=1)
                color = {
                    "number": self.colors["button"],
                    "function": self.colors["function"],
                    "operator": self.colors["operator"],
                    "equal": self.colors["equal"],
                    "danger": self.colors["danger"],
                }[kind]

                btn = self.make_button(
                    grid, label,
                    lambda v=value: self.handle_button(v),
                    color
                )
                btn.grid(
                    row=r, column=c, sticky="nsew",
                    padx=3, pady=3, ipady=7
                )

        footer = tk.Label(
            self.root, 
            text="Python • Tkinter • Safe Expression Evaluator",
            font=("Segoe UI", 8),
            bg=self.colors["bg"],
            fg=self.colors["muted"]
        )
        footer.pack(pady=(0, 8))

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg=self.colors["text"],
            activebackground=self.colors["operator"],
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=4,
            pady=5
        )

    def bind_keys(self):
        self.display.bind("<Return>", lambda event: self.calculate())
        self.display.bind("<KP_Enter>", lambda event: self.calculate())
        self.display.bind("<Escape>", lambda event: self.clear())
        self.display.bind("<Control-l>", lambda event: self.clear())
        self.display.bind("<Control-h>", lambda event: self.show_history())

    def update_display(self):
        self.mode_label.config(text=f"{self.angle_mode} MODE")

    def handle_button(self, value):
        if value == "EQUAL":
            self.calculate()
        elif value == "BACK":
            current = self.expression.get()
            self.expression.set(current[:-1])
        elif value == "ANS":
            if self.history:
                self.expression.set(
                    self.expression.get() + str(self.history[-1][1])
                )
        else:
            self.expression.set(self.expression.get() + value)

        self.display.focus_set()

    def clear(self):
        self.expression.set("")
        self.result_label.config(text="Ready")

    def toggle_theme(self):
        self.dark = not self.dark
        self.setup_theme()
        self.build_ui()
        self.bind_keys()
        self.update_display()

    def toggle_angle(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.update_display()

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title("Calculation History")
        window.geometry("400x420")
        window.configure(bg=self.colors["bg"])

        tk.Label(
            window,
            text="Calculation History",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        ).pack(pady=10)

        listing = tk.Listbox(
            window,
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Consolas", 11),
            selectbackground=self.colors["operator"]
        )
        listing.pack(fill="both", expand=True, padx=12, pady=8)

        for expr, result in reversed(self.history):
            listing.insert("end", f"{expr} = {result}")

        def reuse(event=None):
            selected = listing.curselection()
            if selected:
                item = listing.get(selected[0])
                if " = " in item:
                    self.expression.set(item.rsplit(" = ", 1)[0])
                    window.destroy()

        listing.bind("<Double-Button-1>", reuse)

        self.make_button(
            window, "Reuse Selected", reuse, self.colors["operator"]
        ).pack(fill="x", padx=12, pady=8)

        self.make_button(
            window, "Clear History",
            lambda: self.clear_history(listing),
            self.colors["danger"]
        ).pack(fill="x", padx=12, pady=(0, 12))

    def clear_history(self, listing):
        self.history.clear()
        listing.delete(0, "end")

    def calculate(self):
        source = self.expression.get().strip()
        if not source:
            return

        try:
            result = self.safe_evaluate(source)
            if isinstance(result, complex):
                raise ValueError("Complex results are not supported")
            if not math.isfinite(float(result)):
                raise ValueError("Result is outside the supported range")

            result = round(result, 12) if isinstance(result, float) else result
            display_result = str(result)

            self.history.append((source, result))
            self.result_label.config(text="= " + display_result)
            self.expression.set(display_result)

        except (ValueError, TypeError, ZeroDivisionError,
                OverflowError, SyntaxError, ArithmeticError) as exc:
            self.result_label.config(text=f"Error: {exc}")

    def safe_evaluate(self, source):
        source = source.replace("×", "*").replace("÷", "/")
        source = source.replace("^", "**")
        source = source.replace("−", "-")
        source = source.replace("π", "pi")

        source = re.sub(
            r"(?<=[0-9.)])\s*%",
            "/100",
            source
        )

        tree = ast.parse(source, mode="eval")
        return self.evaluate_node(tree.body)

    def evaluate_node(self, node):
        binary_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

        unary_ops = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)
            ):
                raise ValueError("Only numeric values are allowed")
            return node.value

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in binary_ops:
                raise ValueError("Unsupported operator")

            left = self.evaluate_node(node.left)
            right = self.evaluate_node(node.right)

            if op_type is ast.Pow and abs(right) > 1000:
                raise ValueError("Exponent is too large")

            result = binary_ops[op_type](left, right)

            if isinstance(result, complex):
                raise ValueError("Complex results are not supported")
            if abs(result) > 1e100:
                raise ValueError("Result is too large")
            return result

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in unary_ops:
                raise ValueError("Unsupported unary operator")
            return unary_ops[op_type](self.evaluate_node(node.operand))

        if isinstance(node, ast.Name):
            constants = {
                "pi": math.pi,
                "e": math.e,
            }
            if node.id in constants:
                return constants[node.id]
            raise ValueError(f"Unknown constant: {node.id}")

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if node.keywords or len(node.args) != 1:
                raise ValueError("Functions require one argument")

            x = self.evaluate_node(node.args[0])
            angle = math.radians(x) if self.angle_mode == "DEG" else x

            funcs = {
                "sin": lambda: math.sin(angle),
                "cos": lambda: math.cos(angle),
                "tan": lambda: math.tan(angle),
                "asin": lambda: self.inverse_angle(math.asin(x)),
                "acos": lambda: self.inverse_angle(math.acos(x)),
                "atan": lambda: self.inverse_angle(math.atan(x)),
                "sqrt": lambda: math.sqrt(x),
                "ln": lambda: math.log(x),
                "log": lambda: math.log10(x),
                "exp": lambda: math.exp(x),
                "fact": lambda: math.factorial(int(x))
                if x >= 0 and x == int(x) and x <= 170
                else (_ for _ in ()).throw(
                    ValueError("Factorial requires an integer from 0 to 170")
                ),
                "abs": lambda: abs(x),
            }

            if name not in funcs:
                raise ValueError(f"Unknown function: {name}")
            return funcs[name]()

        raise ValueError("Invalid expression")

    def inverse_angle(self, value):
        return math.degrees(value) if self.angle_mode == "DEG" else value


if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
