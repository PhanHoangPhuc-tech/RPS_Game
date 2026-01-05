import tkinter as tk

class GameWindow:
    def __init__(self, root, send_callback):
        self.root = root
        self.send_callback = send_callback # Hàm này sẽ được gọi khi bấm nút
        self.root.title("Game Oan Tu Ti")
        self.root.geometry("300x250")

        self.label = tk.Label(root, text="Chon nuoc di:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.btn_rock = tk.Button(root, text="BUA (ROCK)", width=15, 
                                command=lambda: self.on_click("ROCK"))
        self.btn_rock.pack(pady=5)
        
        self.btn_paper = tk.Button(root, text="BAO (PAPER)", width=15, 
                                 command=lambda: self.on_click("PAPER"))
        self.btn_paper.pack(pady=5)
        
        self.btn_scissors = tk.Button(root, text="KEO (SCISSORS)", width=15, 
                                    command=lambda: self.on_click("SCISSORS"))
        self.btn_scissors.pack(pady=5)

        self.status_label = tk.Label(root, text="...", fg="blue")
        self.status_label.pack(pady=20)

    def on_click(self, move):
        self.send_callback(move) # Gọi hàm gửi mạng
        self.status_label.config(text=f"Ban chon {move}. Doi ket qua...")
        self.toggle_buttons('disabled')

    def update_status(self, message):
        self.status_label.config(text=message)

    def toggle_buttons(self, state):
        self.btn_rock['state'] = state
        self.btn_paper['state'] = state
        self.btn_scissors['state'] = state