import tkinter as tk


class MessageBox:
    def __init__(self, message):
        self.root = tk.Tk()
        self.root.title("游戏结果")
        self.root.geometry(self.center_window())  # 设置窗口位置和大小
        tk.Label(self.root, text=message).pack(pady=20)
        tk.Button(self.root, text="确定", command=self.close).pack(pady=10)

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 150  # 窗口宽度
        window_height = 100  # 窗口高度
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        return f"{window_width}x{window_height}+{x}+{y}"

    def close(self):
        self.root.destroy()

    def show(self):
        self.root.mainloop()