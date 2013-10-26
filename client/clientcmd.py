class ClientCommands:
  def __init__(self, constants):
    self.constants = constants

  def befriend_user(self, user):
    self.constants.friend[1] = user
    return self.constants.friend

  def chat_message(self, message, username, counter):
    self.constants.chat[1] = message
    self.constants.chat[2] = username
    self.constants.chat[3] = counter
    return self.constants.chat

  def delivered_message(self, counter):
    self.constants.delivered[1] = counter
    return self.constants.delivered

  def request_profile(self, user, version):
    self.constants.request[1] = user
    self.constants.request[2] = version
    return self.constants.request

  def profile_message(self, user, version, profile):
    self.constants.profile[1] = user
    self.constants.profile[2] = version
    self.constants.profile[3] = profile
    print("WFT0*****************")
    print(profile)
    return self.constants.profile
 
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

