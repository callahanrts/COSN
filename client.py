import client_gui

# UDP Socket to connect with server
udp_socket = socket(AF_INET, SOCK_DGRAM)

def peer_listener():
  tcp_socket = socket(AF_INET, SOCK_STREAM)
  tcp_socket.bind((HOST, PORT))
  tcp_socket.listen(1024)
  while 1:
    peer_socket, addr = tcp_socket.accept()
    recv_data, addr = peer_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    log(data)

    if data[STATUS] == "FRIEND":
      reply = confirm


if __name__ == '__main__':
  # Listen for incoming peer connections
  listener = threading.Thread(target = peer_listener)
  listener.start()

  # Create GUI
  view = client_gui.ClientGui()
  view.start()