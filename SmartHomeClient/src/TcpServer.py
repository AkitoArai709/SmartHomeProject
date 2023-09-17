import socket
import threading

class TCPServer:
    def __init__(self, host, port, handle_client):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connections = []
        self.handle_client = handle_client

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
                self.client_connections.append((client_socket, client_thread))

        except Exception as e:
            print(f"An error occurred while starting the server: {str(e)}")
            self.stop()
            
    def stop(self):
        try:
            self.server_socket.close()
            for client_socket, client_thread in self.client_connections:
                client_socket.close()
                client_thread.join()
            print("Server stopped")
        except Exception as e:
            print(f"An error occurred while stopping the server: {str(e)}")