
class Command:
  def __init__(self, host, port, username):
    # Client-Server Command Strings
    self.register = ["REGISTER", host, port, username]  # Response => ACK
    self.query    = ["QUERY", "1"]                      # Response => LOCATION
    self.logout   = ["LOGOUT", username]                # Response => none  
    self.down     = ["DOWN", username]                  # Response => none 

    # P2P Command Strings
    self.ping      = ["PING", "user", "ip", "port"]     # Response => PONG
    self.pong      = ["PONG", "user", "ip", "port"]     # Response => none
    self.friend    = ["FRIEND", ""]                     # Response => CONFIRM
    self.confirm   = ["CONFIRM", username]              # Response => none
    self.busy      = ["BUSY", username]                 # Response => none
    self.chat      = ["CHAT", 'msg', "user", "ctr"]     # Response => DELIVERED
    self.delivered = ["DELIVERED", "counter"]           # Response => none
    self.terminate = ["TERMINATE", username]            # Response => none
    self.request   = ["REQUEST", "user", "ver"]         # Response => PROFILE
    self.profile   = ["PROFILE", username, "v", "jsfl"] # Response => none
    self.relay     = ["RELAY", username, "v"]           # Response => PROFILE
    self.get       = ["GET", "filename"]                # Response => FILE
    self.file      = ["FILE", "name", "len", "content"] # Response => none