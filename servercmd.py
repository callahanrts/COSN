class ServerCommands:
  def __init__(self, constants):
    self.constants = constants

  def register_user(self): 
    return self.constants.register

  def query_user(self, username): 
    query[MESSAGE] = username
    client_socket.sendto(pickle.dumps(query), SERVER_ADDR)
    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    return data

  def logout_user(self): 
    return logout

  def down_user(self, username):
    down[MESSAGE] = username
    return down