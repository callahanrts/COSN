class ServerCommands:
  def __init__(self, constants):
    self.constants = constants

  def register_user(): 
    return register

  def query_user(username): 
    query[MESSAGE] = username
    client_socket.sendto(pickle.dumps(query), SERVER_ADDR)
    recv_data, addr = client_socket.recvfrom(1024)
    data = pickle.loads(recv_data) 
    return data

  def logout_user(): 
    return logout

  def down_user(username):
    down[MESSAGE] = username
    return down