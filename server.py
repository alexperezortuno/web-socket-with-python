import socket
import threading

PORT = 5050
header = 64
FORMAT = 'utf-8'
disconnect_message = 'DISCONNECTED!'
SERVER_ADDR = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (SERVER_ADDR, PORT)

server.bind(address)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(header).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == disconnect_message:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


def start():
    try:
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER_ADDR}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    except KeyboardInterrupt:
        print("\n Server close...")


print("[STARTING] Server is starting...")
start()
