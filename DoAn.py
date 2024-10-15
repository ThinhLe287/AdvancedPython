import tkinter as tk
import random
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import psycopg2

# Kích thước cửa sổ game
WIDTH = 500
HEIGHT = 500
SNAKE_SIZE = 20
INITIAL_SPEED = 100  # Thời gian giữa các lần cập nhật (ms)

# Hàm kết nối cơ sở dữ liệu
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="test",
        user="myuser",
        password="mypassword"
    )

class SnakeGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lê Ngô Gia Thịnh")
        self.icon = tk.PhotoImage(file="Đồ án Python/icon.png")
        self.root.iconphoto(False, self.icon)

        self.create_menu_bar()
        
        # Tạo Canvas cho game
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="light green")
        self.canvas.pack(padx=10, pady=10)
        
        # Tạo nhãn hiển thị điểm số 
        self.score = 0
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14), bg="lightgray")
        self.score_label.pack()

        # Tạo ScrolledText để hiển thị nhật ký trò chơi
        self.log_text = ScrolledText(root, width=40, height=8, wrap=tk.WORD, state="disabled")
        self.log_text.pack(pady=10)
        
        # Khởi tạo các biến trò chơi
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Tọa độ các phần của rắn
        self.direction = "Right"  # Hướng ban đầu của rắn
        self.food = self.create_food()  # Tạo thức ăn
        self.game_running = True

        # Điều khiển bằng phím
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<Escape>", lambda event: self.pause_game())

        # Bắt đầu trò chơi
        self.update_snake()
        self.log_event("Game started!")

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)

        # Menu "File"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_command(label="View High Scores", command=self.view_high_scores)  # Thêm chức năng xem thành tích
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Menu "Settings"
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Game Settings", command=self.game_setting)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Menu "Help"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def new_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.game_running = True
        self.update_snake()
        self.log_event("New game started!")

    def game_setting(self):
        print("Game settings opened")

    def show_about(self):
        messagebox.showinfo("About", "Rắn Săn Mồi - V1")

    def create_food(self):
        # Tạo thức ăn ở vị trí ngẫu nhiên
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        return (x, y)

    def change_direction(self, new_direction):
        # Thay đổi hướng di chuyển của rắn (không cho phép quay ngược)
        if new_direction == "Up" and self.direction != "Down":
            self.direction = new_direction
        elif new_direction == "Down" and self.direction != "Up":
            self.direction = new_direction
        elif new_direction == "Left" and self.direction != "Right":
            self.direction = new_direction
        elif new_direction == "Right" and self.direction != "Left":
            self.direction = new_direction

    def update_snake(self):
        if not self.game_running:
            return

        # Tính toán vị trí mới của đầu rắn
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= SNAKE_SIZE
        elif self.direction == "Down":
            head_y += SNAKE_SIZE
        elif self.direction == "Left":
            head_x -= SNAKE_SIZE
        elif self.direction == "Right":
            head_x += SNAKE_SIZE
        
        # Kiểm tra va chạm tường hoặc tự cắn đuôi
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or (head_x, head_y) in self.snake:
            self.save_score()
            self.end_game()
            return

        # Thêm vị trí mới vào đầu rắn
        new_snake = [(head_x, head_y)] + self.snake[:-1]

        # Kiểm tra nếu rắn ăn thức ăn
        if (head_x, head_y) == self.food:
            new_snake.append(self.snake[-1])  # Tăng chiều dài rắn
            self.food = self.create_food()  # Tạo thức ăn mới
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.log_event(f"Snake ate food! Score: {self.score}")

        self.snake = new_snake

        # Vẽ lại rắn và thức ăn
        self.canvas.delete("all")
        self.draw_snake()
        self.draw_food()

        # Cập nhật rắn sau 100ms
        self.root.after(INITIAL_SPEED, self.update_snake)

    def draw_snake(self):
        # Vẽ rắn trên Canvas
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE, fill="blue")

    def draw_food(self):
        # Vẽ thức ăn trên Canvas
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + SNAKE_SIZE, self.food[1] + SNAKE_SIZE, fill="red")

    def log_event(self, event):
        # Ghi lại các sự kiện vào ScrolledText
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, event + "\n")
        self.log_text.yview(tk.END)  # Tự động cuộn xuống cuối
        self.log_text.config(state="disabled")

    def end_game(self):
        self.game_running = False
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
        self.log_event("Game over!")
        self.new_game()

    def pause_game(self):
        self.game_running = False
        messagebox.showinfo("Paused", "Game paused! Press 'OK' to continue.")
        self.game_running = True
        self.update_snake()  # Bắt đầu lại trò chơi

    def save_score(self):
        try:
            connection = connect_db()
            cursor = connection.cursor()

            # Lưu điểm vào cơ sở dữ liệu
            player_name = "Player1"  # Có thể thay đổi để yêu cầu người chơi nhập tên
            insert_query = """
                INSERT INTO player_scores (player_name, score) 
                VALUES (%s, %s);
            """
            cursor.execute(insert_query, (player_name, self.score))
            connection.commit()

            self.log_event(f"Score saved to database: {self.score}")

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to save score: {error}")

        finally:
            if connection:
                cursor.close()
                connection.close()

    def view_high_scores(self):
        try:
            connection = connect_db()
            cursor = connection.cursor()

            # Truy vấn tất cả các thành tích
            cursor.execute("SELECT player_name, score FROM player_scores ORDER BY score DESC LIMIT 10;")
            high_scores = cursor.fetchall()

            # Tạo chuỗi hiển thị thành tích
            high_score_text = "\n".join([f"{name}: {score}" for name, score in high_scores])

            # Hiển thị thành tích trong messagebox
            messagebox.showinfo("High Scores", f"Top 10 Scores:\n\n{high_score_text}")

        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Error", f"Error fetching high scores: {error}")

        finally:
            if connection:
                cursor.close()
                connection.close()

# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    gui = SnakeGameGUI(root)
    root.mainloop()
