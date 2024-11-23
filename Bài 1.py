import tkinter as tk
from tkinter import ttk

# Function definitions for arithmetic operations
def calculate(operation):
    try:
        a = float(number_a.get())
        b = float(number_b.get())
        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/':
            result = a / b if b != 0 else "Lỗi: Chia cho 0"
        result_var.set(result)
    except ValueError:
        result_var.set("Lỗi: Nhập không hợp lệ")

# Function to clear input and result
def clear():
    number_a.set("")
    number_b.set("")
    result_var.set("")

# Create main window
win = tk.Tk()
win.title("Ứng dụng Tính Toán Đơn Giản")

# Input labels and entry fields
ttk.Label(win, text="Số thứ nhất (a):").grid(column=0, row=0, padx=10, pady=5)
ttk.Label(win, text="Số thứ hai (b):").grid(column=0, row=1, padx=10, pady=5)

number_a = tk.StringVar()
number_b = tk.StringVar()

a_entry = ttk.Entry(win, width=15, textvariable=number_a)
a_entry.grid(column=1, row=0, padx=10, pady=5)

b_entry = ttk.Entry(win, width=15, textvariable=number_b)
b_entry.grid(column=1, row=1, padx=10, pady=5)

# Result display
ttk.Label(win, text="Kết quả:").grid(column=0, row=2, padx=10, pady=5)
result_var = tk.StringVar()
result_display = ttk.Entry(win, width=15, textvariable=result_var, state='readonly')
result_display.grid(column=1, row=2, padx=10, pady=5)

# Buttons for operations
button_frame = ttk.Frame(win)
button_frame.grid(column=0, row=3, columnspan=3, pady=10)

ttk.Button(button_frame, text="Cộng (+)", command=lambda: calculate('+')).grid(column=0, row=0, padx=5)
ttk.Button(button_frame, text="Trừ (-)", command=lambda: calculate('-')).grid(column=1, row=0, padx=5)
ttk.Button(button_frame, text="Nhân (×)", command=lambda: calculate('*')).grid(column=2, row=0, padx=5)
ttk.Button(button_frame, text="Chia (÷)", command=lambda: calculate('/')).grid(column=3, row=0, padx=5)

# Clear button
clear_button = ttk.Button(win, text="Xóa", command=clear)
clear_button.grid(column=1, row=4, pady=10)

# Start the application
win.mainloop()
