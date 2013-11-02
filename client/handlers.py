
class CommandHandler(object):
  def __init__(self, servecmd, clientcmd):
    self.servecmd = servecmd

  def handle_server_command(self, command, user):
    if command == "REGISTER":
      return self.servecmd.register_user()

    elif command == "QUERY":
      return self.servecmd.query_user(user)

    elif command == "LOGOUT":
      return self.servecmd.logout_user()

  def handle_peer_commands(self, command, user, alt_data):
    # Respond to commands
    if command == "FRIEND":
      return ("friend", self.clientcmd.befriend_user(self.username))

    elif command == "REQUEST": 
      return ("profile", self.clientcmd.request_profile(user, self.user["profile"]["info"]["version"]))

    elif command == "RELAY": 
      return ("profile", self.clientcmd.request_profile_relay(alt_data, self.user["profile"]["info"]["version"]))

    elif command == "GET": 
      return ("file", self.clientcmd.request_file(alt_data))


      # Current, single window chat
  def chat_command(self, message, user): 
    if user in self.friends:
      # Open connection and get user
      self.chat_conn = socket(AF_INET, SOCK_STREAM)
      user_data = self.send_udp(self.servecmd.query_user(user))
      self.view.log_message(self.username+": "+message)

      try:
        self.chat_conn.connect((user_data[2], int(user_data[3])))
        self.chat_conn.send(pickle.dumps(self.clientcmd.chat_message(message, self.username, self.chat_counter))) 
        self.chat_counter += 1

        response = self.retrieve_data() # Get message
        self.view.log(response) 
      except:
        logging.exception("hm")
        self.view.log(self.send_udp(self.clientcmd.user_offline(user_data[4])))
    else:
      self.view.log("You must be friends with this user before chatting with them")







