##############################################################
# These functions are used to preload parameters to commands
# that will be sent to another client
##############################################################
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

  def request_file(self, filename):
    self.constants.get[1] = filename
    return self.constants.get

  def send_file(self, filename, filesize, content):
    self.constants.file[1] = filename
    self.constants.file[2] = filesize
    self.constants.file[3] = content
    return self.constants.file

  def request_profile_relay(self, user, version):
    self.constants.relay[1] = user
    self.constants.relay[2] = version
    return self.constants.relay

  def profile_message(self, user, version, profile):
    self.constants.profile[1] = user
    self.constants.profile[2] = version
    self.constants.profile[3] = profile
    return self.constants.profile

  def pong_server(self, username, host, port):
    self.constants.pong[1] = username
    self.constants.pong[2] = host
    self.constants.pong[3] = port
    return self.constants.pong

  def user_offline(self, username):
    self.constants.down[1] = username
    return self.constants.down
