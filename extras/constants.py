
class Command(object):
  def __init__(self, host, port, username):
    # Client-Server Command Strings
    self.register = [u"REGISTER", host, port, username]  # Response => ACK
    self.query    = [u"QUERY", u"1"]                      # Response => LOCATION
    self.logout   = [u"LOGOUT", username]                # Response => none  
    self.down     = [u"DOWN", username]                  # Response => none 

    # P2P Command Strings
    self.ping      = [u"PING", u"user", u"ip", u"port"]     # Response => PONG
    self.pong      = [u"PONG", u"user", u"ip", u"port"]     # Response => none
    self.friend    = [u"FRIEND", u""]                     # Response => CONFIRM
    self.confirm   = [u"CONFIRM", username]              # Response => none
    self.busy      = [u"BUSY", username]                 # Response => none
    self.chat      = [u"CHAT", u'msg', u"user", u"ctr"]     # Response => DELIVERED
    self.delivered = [u"DELIVERED", u"counter"]           # Response => none
    self.terminate = [u"TERMINATE", username]            # Response => none
    self.request   = [u"REQUEST", u"user", u"ver"]         # Response => PROFILE
    self.profile   = [u"PROFILE", username, u"v", u"jsfl"] # Response => none
    self.relay     = [u"RELAY", username, u"v"]           # Response => PROFILE
    self.get       = [u"GET", u"filename"]                # Response => FILE
    self.file      = [u"FILE", u"name", u"len", u"content"] # Response => none