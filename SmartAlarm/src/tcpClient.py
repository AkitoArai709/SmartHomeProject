import socket

class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to {self.server_ip}:{self.server_port}")
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")
        except Exception as e:
            print(f"An error occurred while connecting: {str(e)}")

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode())
        except Exception as e:
            print(f"An error occurred while sending data: {str(e)}")
            
    def send_hex(self, data):
        try:
            self.client_socket.send(data)
        except Exception as e:
            print(f"An error occurred while sending data: {str(e)}")

    def receive_message(self, buffer_size=1024):
        try:
            data = self.client_socket.recv(buffer_size)
            return data.decode()
        except Exception as e:
            print(f"An error occurred while receiving data: {str(e)}")

    def close(self):
        try:
            self.client_socket.close()
            print("Connection closed.")
        except Exception as e:
            print(f"An error occurred while closing the connection: {str(e)}")