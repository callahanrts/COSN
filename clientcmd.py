class ClientCommands:
  def __init__(self, constants):
    self.constants = constants

  def sendto_peer(data, send_message):
    chat_conn = socket(AF_INET, SOCK_STREAM)  
    try: 
      chat_conn.connect((data[2], int(data[3])))
      chat_conn.send(pickle.dumps(send_message))  
    except: 
      log("User is offline")
      down_user(username.get())
      return

    recv_data, addr = chat_conn.recvfrom(1024)
    chat_conn.close()
    return pickle.loads(recv_data) 

  def reply_message(friend_data):
    chat[MESSAGE] = chat_message.get()
    log_message(USERNAME+": "+chat[MESSAGE])
    chat[2] = USERNAME
    sendto_peer(friend_data, chat)
    return

  def chatting(val):
    chat_flat = val

  def is_chatting():
    global messaging
    if messaging.get() == 1:
      return True
    return False


  def ping_user(user):
    ping[MESSAGE] = user[MESSAGE]
    ping[2] = user[2]
    ping[3] = user[3]
    return ping

  def pong_user():
    pong[MESSAGE] = USERNAME
    pong[2] = HOST
    pong[3] = PORT
    return pong

  def request_profile(user, version):
    request[MESSAGE] = user[MESSAGE]
    request[2] = version
    return request


  def befriend_user(user):
    friend[MESSAGE] = user[MESSAGE]
    return friend