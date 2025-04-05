import tkinter as tk
from tkinter import ttk, messagebox
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("공학용 계산기")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # 계산 관련 변수
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 결과 표시창
        result_entry = ttk.Entry(
            self.root,
            textvariable=self.result_var,
            justify="right",
            font=("Arial", 20)
        )
        result_entry.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")
        
        # 버튼 텍스트와 위치
        buttons = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3), ('ln', 1, 4),
            ('π', 2, 0), ('e', 2, 1), ('x²', 2, 2), ('√', 2, 3), ('1/x', 2, 4),
            ('(', 3, 0), (')', 3, 1), ('C', 3, 2), ('←', 3, 3), ('%', 3, 4),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3), ('*', 4, 4),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3), ('+', 5, 4),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('±', 6, 3), ('=', 6, 4),
            ('0', 7, 0), ('.', 7, 1)
        ]
        
        # 버튼 생성
        for (text, row, col) in buttons:
            if text == '=':
                button = ttk.Button(
                    self.root,
                    text=text,
                    command=self.calculate
                )
                button.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
            elif text == '0':
                button = ttk.Button(
                    self.root,
                    text=text,
                    command=lambda x=text: self.append_number(x)
                )
                button.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
            elif text.isdigit() or text == '.':
                button = ttk.Button(
                    self.root,
                    text=text,
                    command=lambda x=text: self.append_number(x)
                )
                button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            else:
                button = ttk.Button(
                    self.root,
                    text=text,
                    command=lambda x=text: self.button_click(x)
                )
                button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # 그리드 가중치 설정
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
    
    def button_click(self, key):
        if key in ['sin', 'cos', 'tan', 'log', 'ln', 'x²', '√', '1/x']:
            self.function_click(key)
        elif key in ['π', 'e']:
            self.constant_click(key)
        elif key in ['(', ')']:
            self.append_operator(key)
        elif key == 'C':
            self.clear_display()
        elif key == '←':
            self.delete_last_char()
        elif key == '±':
            self.change_sign()
        elif key in ['+', '-', '*', '/', '%']:
            self.append_operator(key)
    
    def append_number(self, number):
        if self.result_var.get() == "0" and number != ".":
            self.result_var.set(number)
        else:
            self.result_var.set(self.result_var.get() + number)
    
    def append_operator(self, operator):
        current = self.result_var.get()
        if current and current[-1] not in ['+', '-', '*', '/', '%', '(', '.']:
            self.result_var.set(current + operator)
    
    def function_click(self, func):
        try:
            current = float(self.result_var.get())
            result = None
            error_msg = None

            if func == 'sin':
                result = math.sin(math.radians(current))
            elif func == 'cos':
                result = math.cos(math.radians(current))
            elif func == 'tan':
                if abs(math.cos(math.radians(current))) < 1e-10:
                    error_msg = "탄젠트 함수 정의되지 않음"
                else:
                    result = math.tan(math.radians(current))
            elif func == 'log':
                if current <= 0:
                    error_msg = "로그함수의 정의역은 양수"
                else:
                    result = math.log10(current)
            elif func == 'ln':
                if current <= 0:
                    error_msg = "자연로그함수의 정의역은 양수"
                else:
                    result = math.log(current)
            elif func == 'x²':
                result = current ** 2
            elif func == '√':
                if current < 0:
                    error_msg = "제곱근의 정의역은 0 이상"
                else:
                    result = math.sqrt(current)
            elif func == '1/x':
                if abs(current) < 1e-10:
                    error_msg = "0으로 나눌 수 없음"
                else:
                    result = 1 / current
            
            if error_msg:
                messagebox.showerror("Error", error_msg)
                self.result_var.set("Error")
            else:
                self.result_var.set(str(result))
                
        except ValueError as e:
            messagebox.showerror("Error", "잘못된 입력값")
            self.result_var.set("Error")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.result_var.set("Error")
    
    def constant_click(self, const):
        if const == 'π':
            self.result_var.set(str(math.pi))
        elif const == 'e':
            self.result_var.set(str(math.e))
    
    def clear_display(self):
        self.result_var.set("0")
    
    def delete_last_char(self):
        current = self.result_var.get()
        if len(current) > 1:
            self.result_var.set(current[:-1])
        else:
            self.result_var.set("0")
    
    def change_sign(self):
        current = self.result_var.get()
        if current.startswith('-'):
            self.result_var.set(current[1:])
        else:
            self.result_var.set('-' + current)
    
    def calculate(self):
        try:
            expression = self.result_var.get()
            # π와 e를 실제 값으로 변환
            expression = expression.replace('π', str(math.pi))
            expression = expression.replace('e', str(math.e))
            result = eval(expression)
            self.result_var.set(str(result))
        except ZeroDivisionError:
            messagebox.showerror("Error", "0으로 나눌 수 없습니다")
            self.result_var.set("Error")
        except Exception as e:
            messagebox.showerror("Error", "잘못된 수식입니다")
            self.result_var.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop() 
