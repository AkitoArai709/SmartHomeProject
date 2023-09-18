from TcpServer import TCPServer
from AlarmSpeaker import AlarmSpeaker

alarmSpeaker = AlarmSpeaker()

def received_handler(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received message from client{client_address}: {[hex(x) for x in data]}")
            
            if data[0] == 0x01:
                ctlCode = data[1]
                if ctlCode == 0x00:
                    alarmSpeaker.StartThread()
                elif ctlCode == 0x01:
                    alarmSpeaker.StopThread()
                    
            result = bytes([0x00])
            client_socket.send(result)
                
    except Exception as e:
        print(f"An error occurred while handling client: {str(e)}")
    finally:
        client_socket.close()
        print("Client connection closed")


# サーバーの使用例
if __name__ == "__main__":
    server_host = "0.0.0.0"  # すべてのネットワークインターフェースを受け入れる場合
    server_port = 4000

    server = TCPServer(server_host, server_port, received_handler)
    server.start()

    server.stop()