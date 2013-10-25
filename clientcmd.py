class ClientCommands:
  def __init__(self, constants):
    self.constants = constants

  def befriend_user(self, user):
    self.constants.friend[1] = user
    return self.constants.friend

  def chat_message(self, message, username):
    self.constants.chat[1] = message
    self.constants.chat[2] = username
    return self.constants.chat

  # def reply_message(self, friend_data):
  #   chat[1] = chat_message.get()
  #   log_message(USERNAME+": "+chat[1])
  #   chat[2] = USERNAME
  #   sendto_peer(friend_data, chat)
  #   return

  # def chatting(self, val):
  #   chat_flat = val

  # def is_chatting(self):
  #   global messaging
  #   if messaging.get() == 1:
  #     return True
  #   return False

  # def ping_user(self, user):
  #   ping[1] = user[1]
  #   ping[2] = user[2]
  #   ping[3] = user[3]
  #   return ping

  # def pong_user(self):
  #   pong[1] = USERNAME
  #   pong[2] = HOST
  #   pong[3] = PORT
  #   return pong

  # def request_profile(self, user, version):
  #   request[1] = user[1]
  #   request[2] = version
  #   return request

