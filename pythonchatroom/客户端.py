import socket
import tkinter as tk
import threading

client_socket = None
connected = False
username = None

def receive_messages():
    global client_socket
    global connected
    while connected:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            text_area.insert('end', message + '\n')
            text_area.see('end')
        except OSError:
            break

def connect_to_server(ip, port, uname):
    global client_socket
    global connected
    global username
    username = uname
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        connected = True
        client_socket.send(username.encode('utf-8'))
        threading.Thread(target=receive_messages).start()
        status_label.config(text='Connected to server')
    except Exception as e:
        status_label.config(text=f'Error: {e}')

def send_message(event=None):
    message = input_field.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        
        text_area.see('end')
        input_field.delete(0, 'end')

def on_closing():
    global connected
    connected = False
    client_socket.close()
    root.destroy()

root = tk.Tk()
root.title('Heated')

text_area = tk.Text(root)
text_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

input_field = tk.Entry(root)
input_field.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
input_field.bind("<Return>", send_message)

send_button = tk.Button(root, text='Send', command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

ip_label = tk.Label(root, text='Server IP:')
ip_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
ip_entry = tk.Entry(root)
ip_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

port_label = tk.Label(root, text='Port:')
port_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
port_entry = tk.Entry(root)
port_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

username_label = tk.Label(root, text='Username:')
username_label.grid(row=4, column=0, padx=10, pady=5, sticky='e')
username_entry = tk.Entry(root)
username_entry.grid(row=4, column=1, padx=10, pady=5, sticky='ew')

connect_button = tk.Button(root, text='Connect', command=lambda: connect_to_server(ip_entry.get(), int(port_entry.get()), username_entry.get()))
connect_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

status_label = tk.Label(root, text='Not connected to server')
status_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
