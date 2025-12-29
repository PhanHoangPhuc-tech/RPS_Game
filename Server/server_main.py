import socket
import threading
from game_logic import check_winner

HOST = '127.0.0.1'
PORT = 65432

clients = []
moves = {}


def handle_client(client_socket, player_id):
    global clients, moves
    try:
        client_socket.send(f"Chao mung Player {player_id}. Doi doi thu...".encode('utf-8'))

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data: break

            print(f"Player {player_id} chon: {data}")
            moves[client_socket] = data

            # Khi đủ 2 người chọn (và phải đảm bảo đủ 2 người đang kết nối)
            if len(moves) == 2 and len(clients) == 2:
                p1_sock = clients[0]
                p2_sock = clients[1]

                # Kiểm tra xem socket trong moves có khớp với người chơi hiện tại không
                if p1_sock in moves and p2_sock in moves:
                    p1_move = moves[p1_sock]
                    p2_move = moves[p2_sock]

                    result = check_winner(p1_move, p2_move)

                    # Gửi kết quả
                    if result == 0:
                        p1_sock.send("KETQUA: HOA".encode('utf-8'))
                        p2_sock.send("KETQUA: HOA".encode('utf-8'))
                    elif result == 1:
                        p1_sock.send("KETQUA: THANG".encode('utf-8'))
                        p2_sock.send("KETQUA: THUA".encode('utf-8'))
                    else:
                        p1_sock.send("KETQUA: THUA".encode('utf-8'))
                        p2_sock.send("KETQUA: THANG".encode('utf-8'))

                    moves = {}  # Reset ván mới cho cả 2
    except Exception as e:
        print(f"Loi tai Player {player_id}: {e}")
    finally:
        # Dọn dẹp khi ngắt kết nối
        if client_socket in clients: clients.remove(client_socket)
        if client_socket in moves: del moves[client_socket]
        client_socket.close()
        print(f"Player {player_id} da ngat ket noi.")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Cho phép hàng đợi nhiều hơn
    print("SERVER DANG CHAY... (Cho ket noi)")

    id_counter = 0
    while True:
        client, addr = server.accept()

        if len(clients) < 2:
            clients.append(client)
            id_counter += 1
            print(f"Player {id_counter} da ket noi tu {addr}")
            threading.Thread(target=handle_client, args=(client, id_counter)).start()
        else:
            # Nếu phòng đầy, báo bận rồi ngắt
            client.send("Phong da day. Vui long thu lai sau.".encode('utf-8'))
            client.close()


if __name__ == "__main__":
    start_server()