import socket
import threading
import tkinter as tk
from tkinter import messagebox
from gui_layout import GameWindow

HOST = '127.0.0.1'
PORT = 65432


class ClientApp:
    def __init__(self):
        # 1. Khởi tạo giao diện TRƯỚC
        self.root = tk.Tk()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

        # Khởi tạo giao diện từ file gui_layout
        # Lưu ý: Lúc này chưa kết nối, nên hàm gửi (self.send_data) cần xử lý cẩn thận
        self.window = GameWindow(self.root, self.send_data)

        # Cập nhật trạng thái ban đầu
        self.window.update_status("Dang ket noi toi Server...")
        self.window.toggle_buttons('disabled')  # Khóa nút khi chưa kết nối

        # 2. Tạo luồng riêng để kết nối Server (để không bị đơ giao diện)
        threading.Thread(target=self.connect_to_server, daemon=True).start()

        # Xử lý khi đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def connect_to_server(self):
        try:
            self.sock.connect((HOST, PORT))
            self.is_connected = True

            # Nếu kết nối thành công:
            self.window.update_status("Da ket noi! Cho doi thu...")

            # Bắt đầu luồng nhận tin nhắn
            threading.Thread(target=self.receive_data, daemon=True).start()

        except Exception as e:
            # Nếu không kết nối được
            self.window.update_status("Khong tim thay Server!")
            # Có thể hiện popup báo lỗi nếu muốn, nhưng giao diện vẫn giữ nguyên
            # messagebox.showerror("Loi", "Khong the ket noi Server!")

    def send_data(self, move):
        if self.is_connected:
            try:
                self.sock.send(move.encode('utf-8'))
            except:
                self.window.update_status("Mat ket noi khi dang gui!")
                self.is_connected = False
        else:
            messagebox.showwarning("Canh bao", "Chua ket noi duoc voi Server!")

    def receive_data(self):
        while True:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data: break

                if "KETQUA" in data:
                    parts = data.split(":")
                    if len(parts) > 1:
                        result_text = parts[1].strip()
                        self.window.update_status(f"KET QUA: {result_text}")
                        self.window.toggle_buttons('normal')
                else:
                    self.window.update_status(data)
                    # --- SỬA ĐOẠN NÀY ---
                    # Nếu server gửi lời chào (có chữ "Player"), hãy mở khóa nút
                    if "Player" in data:
                        self.window.toggle_buttons('normal')
                        # --------------------
            except:
                break

        self.is_connected = False
        self.window.update_status("Ngat ket noi voi Server.")

    def on_closing(self):
        if self.is_connected:
            self.sock.close()
        self.root.destroy()


if __name__ == "__main__":
    ClientApp()
