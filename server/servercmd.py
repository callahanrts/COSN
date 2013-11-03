#################################################
# These are commands for the client to construct 
# and send to the server
#################################################
class ServerCommands(object):
  def __init__(self, constants):
    self.constants = constants

  def register_user(self): 
    return self.constants.register

  def query_user(self, username): 
    self.constants.query[1] = username
    return self.constants.query

  def logout_user(self): 
    return self.constants.logout

  def down_user(self, username):
    down[MESSAGE] = username
    return down