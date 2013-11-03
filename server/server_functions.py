import sqlite3
################################################################
# These functions are used by the server to interact with the 
# database and give the server commands to return to the user
################################################################
def remove_user_from_table(username, conn): 
  conn.execute(u"DELETE FROM online_users WHERE username = ?", [username])
  conn.commit()

def logout_user(username, conn): 
  remove_user_from_table(username, conn)
  return [username + u" was logged out successully"]

# Return user location or a message that explains the user is probably offline
def query_user(request, conn):
  cursor = conn.execute(u"SELECT * FROM online_users WHERE username = ? LIMIT 1", [unicode(request[1])])
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    return [u"LOCATION", row[0], row[1], row[2], row[3]]
  else:
    return [u"Error", u"User was not found--probably offline"]

# Insert a user into the online_users table
def register_user(request, conn):
  cursor = conn.execute(u"SELECT * FROM online_users WHERE username = ? LIMIT 1", [request[3]] )
  exists = False
  for row in cursor:
    if row[0]:
      exists = True 
  if exists:
    return [u"ACK", row[0], row[1], row[2], row[3], u"User already registered"]
  else:
    conn.execute(u"INSERT INTO online_users(id, ip_address, port, username) VALUES(NULL, ?, ?, ?)", [request[1], request[2], request[3]])
    conn.commit()
    return [u"ACK", request[1], request[2], request[3], u"Registered successfully"]

def down_user(username, conn):
  remove_user_from_table(username, conn)
  return [u"User was taken offline for inactivity"]

def ping_command(user_data):
 return [u"PING", user_data[4], user_data[2], user_data[3]] 