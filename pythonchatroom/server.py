import socket
import threading
import tkinter as tk

server_socket = None
client_sockets = {}
client_usernames = {}

def handle_client(client_socket, client_address):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        client_usernames[client_socket] = username
        print(f"{username} 连接自 {client_address}")
        broadcast(f"{username} 加入了聊天。")
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{username}: {message}")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        if client_socket in client_sockets:
            username = client_usernames[client_socket]
            del client_usernames[client_socket]
            client_sockets.pop(client_socket)
            broadcast(f"{username} 离开了聊天。")
            client_socket.close()

def broadcast(message):
    for client_socket in client_sockets:
        client_socket.send(message.encode('utf-8'))

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print("服务器正在监听...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_sockets[client_socket] = client_address
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

def start_server_ui():
    start_server_button.config(state='disabled')
    stop_server_button.config(state='normal')
    status_label.config(text='服务器正在运行...')
    threading.Thread(target=start_server).start()

def stop_server_ui():
    if server_socket:
        server_socket.close()
    start_server_button.config(state='normal')
    stop_server_button.config(state='disabled')
    status_label.config(text='服务器已停止。')

root = tk.Tk()
root.title('服务器')

start_server_button = tk.Button(root, text='启动服务器', command=start_server_ui)
start_server_button.grid(row=0, column=0, padx=10, pady=10)

stop_server_button = tk.Button(root, text='停止服务器', command=stop_server_ui, state='disabled')
stop_server_button.grid(row=1, column=0, padx=10, pady=10)

status_label = tk.Label(root, text='服务器已停止。')
status_label.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
