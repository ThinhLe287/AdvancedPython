import tkinter as tk

# Kích thước cửa sổ game
WIDTH = 500
HEIGHT = 500
SNAKE_SIZE = 20

class SnakeGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Đồ Án")
        
        # Tạo Canvas cho game
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="light green")
        self.canvas.pack(padx=10, pady=10)
        
        # Tạo các nhãn cho điểm số 
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14), bg="lightgray")
        self.score_label.pack()
        
        # Tạo các nút điều khiển
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        self.btn_up = tk.Button(control_frame, text="Up", width=10, height=2)
        self.btn_up.grid(row=0, column=1)
        
        self.btn_left = tk.Button(control_frame, text="Left", width=10, height=2)
        self.btn_left.grid(row=1, column=0)
        
        self.btn_down = tk.Button(control_frame, text="Down", width=10, height=2)
        self.btn_down.grid(row=1, column=1)
        
        self.btn_right = tk.Button(control_frame, text="Right", width=10, height=2)
        self.btn_right.grid(row=1, column=2)
        
        # Hiển thị sẵn rắn và thức ăn tĩnh
        self.create_static_snake_and_food()
    
    def create_static_snake_and_food(self):
        # Vẽ một con rắn tĩnh (dài 3 đoạn)
        self.canvas.create_rectangle(100, 100, 100 + SNAKE_SIZE, 100 + SNAKE_SIZE, fill="blue")
        self.canvas.create_rectangle(80, 100, 80 + SNAKE_SIZE, 100 + SNAKE_SIZE, fill="blue")
        self.canvas.create_rectangle(60, 100, 60 + SNAKE_SIZE, 100 + SNAKE_SIZE, fill="blue")
        
        # Vẽ thức ăn tĩnh
        self.canvas.create_oval(200, 200, 200 + SNAKE_SIZE, 200 + SNAKE_SIZE, fill="red")

# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    gui = SnakeGameGUI(root)
    root.mainloop()
