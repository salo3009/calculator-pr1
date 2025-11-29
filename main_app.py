import tkinter as tk
from tkinter import messagebox
from basic_operations import add, subtract, multiply, divide
from advanced_operations import modulus, floor_divide, floor, ceil
from scientific_operations import sin, cos, power, square_root
from memory_operations import Memory

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.current_input = "0"
        self.memory = Memory()

        self.display_var = tk.StringVar()
        self.display_var.set(self.current_input)
        self.display = tk.Entry(
            root, textvariable=self.display_var, font=("Arial", 18),
            justify="right", state="readonly", bd=10, relief=tk.SUNKEN
        )
        self.display.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        self.create_buttons()

        for i in range(7):
            root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            root.grid_columnconfigure(j, weight=1)

    def create_buttons(self):
        buttons = [
            ("MC", 1, 0), ("MR", 1, 1), ("MS", 1, 2), ("M+", 1, 3), ("M-", 1, 4),
            ("sin", 2, 0), ("cos", 2, 1), ("√", 2, 2), ("x^y", 2, 3), ("CE", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("//", 3, 4),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3), ("%", 4, 4),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3), ("⌊x⌋", 5, 4),
            ("0", 6, 0), (".", 6, 1), ("=", 6, 2), ("+", 6, 3), ("⌈x⌉", 6, 4),
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(
                self.root, text=text, font=("Arial", 14), command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

    def update_display(self):
        display_text = self.current_input
        if len(display_text) > 20:
            display_text = display_text[:20] + "..."
        self.display_var.set(display_text)

    def on_button_click(self, char):
        try:
            if char == "CE":
                self.current_input = "0"
            elif char == "=":
                self.evaluate_expression()
            elif char in "0123456789":
                if self.current_input == "0":
                    self.current_input = char
                else:
                    self.current_input += char
            elif char == ".":
                if "." not in self.current_input and self.current_input not in "+-*/()":
                    self.current_input += char
            elif char == "+":
                self.current_input += "+"
            elif char == "-":
                self.current_input += "-"
            elif char == "*":
                self.current_input += "*"
            elif char == "/":
                self.current_input += "/"
            elif char == "//":
                self.current_input += "//"
            elif char == "%":
                self.current_input += "%"
            elif char == "x^y":
                self.current_input += "**"
            elif char == "√":
                if self.current_input == "0":
                    self.current_input = "sqrt("
                else:
                    self.current_input += "sqrt("
            elif char == "sin":
                self.current_input += "sin("
            elif char == "cos":
                self.current_input += "cos("
            elif char == "⌊x⌋":
                self.current_input += "floor("
            elif char == "⌈x⌉":
                self.current_input += "ceil("
            elif char == "MC":
                self.memory.memory_clear()
                return
            elif char == "MR":
                val = self.memory.memory_recall()
                self.current_input = str(val)
            elif char == "MS":
                try:
                    val = float(eval(self.get_safe_expression()))
                    self.memory.memory_store(val)
                except:
                    messagebox.showerror("Error", "Invalid value to store in memory!")
                return
            elif char == "M+":
                try:
                    val = float(eval(self.get_safe_expression()))
                    self.memory.memory_add(val)
                except:
                    messagebox.showerror("Error", "Invalid value to add to memory!")
                return
            elif char == "M-":
                try:
                    val = float(eval(self.get_safe_expression()))
                    self.memory.memory_subtract(val)
                except:
                    messagebox.showerror("Error", "Invalid value to subtract from memory!")
                return
            else:
                self.current_input += char

            self.update_display()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_safe_expression(self):
        expr = self.current_input
        expr = expr.replace("sin(", "sin(")
        expr = expr.replace("cos(", "cos(")
        expr = expr.replace("sqrt(", "square_root(")
        expr = expr.replace("floor(", "floor(")
        expr = expr.replace("ceil(", "ceil(")
        return expr

    def evaluate_expression(self):
        try:
            expr = self.get_safe_expression()
            allowed_names = {
                "sin": sin,
                "cos": cos,
                "sqrt": square_root,
                "square_root": square_root,
                "floor": floor,
                "ceil": ceil,
                "add": add,
                "subtract": subtract,
                "multiply": multiply,
                "divide": divide,
                "modulus": modulus,
                "floor_divide": floor_divide,
                "power": power,
                "__builtins__": {},
            }

            result = eval(expr, {"__builtins__": {}}, allowed_names)

            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.current_input = str(result)

        except ZeroDivisionError:
            self.current_input = "Error: Division by zero"
        except ValueError as ve:
            self.current_input = f"Error: {ve}"
        except Exception as e:
            self.current_input = f"Error: {e}"

        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()