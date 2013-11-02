# Include the Dropbox SDK
import dropbox
import sqlite3

class Dropbox:
  def __init__(self, username):
    # Get your app key and secret from the Dropbox developer website
    self.app_key = '2ycmk3mndjuvija'
    self.app_secret = 'f6v4pvhsirmr5tw'

    self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)

    # Connect to sqlite database and print success message
    self.conn = sqlite3.connect('../server/cosn.db')

    # Set local username
    self.username = username

    # Set token if exists
    self.token = self.has_token()

    # Set client and account information 
    if self.token != '': self.set_client

  def auth_url(self):
    return self.flow.start()

  def get_token(self, auth_code):
    if self.token == '':
      # This will fail if the user enters an invalid authorization code
      self.token, self.user_id = self.flow.finish(auth_code)
      self.set_client()
      self.conn.execute("INSERT INTO dropbox(username, token) VALUES(?, ?)", [self.username, self.token])
      self.conn.commit()
    return self.token

  def set_client(self):
    self.client = dropbox.client.DropboxClient(self.token) 
    self.acct = self.client.account_info()

  def has_token(self):
    cursor = self.conn.execute("SELECT * FROM dropbox WHERE username = ? LIMIT 1", [self.username])
    token = ''
    for row in cursor:
      if row[0]:
        token = row[1]
    if token: return token
    return ''

  def upload_profile(self):
    

  def upload_file(self, filename):
    f = open('working-draft.txt')
    response = client.put_file('/magnum-opus.txt', f)
    print "uploaded:", response

# # This will fail if the user enters an invalid authorization code
# access_token, user_id = flow.finish(code)

# client = dropbox.client.DropboxClient(access_token)
# print 'linked account: ', client.account_info()

# f = open('working-draft.txt')
# response = client.put_file('/magnum-opus.txt', f)
# print 'uploaded: ', response

# folder_metadata = client.metadata('/')
# print 'metadata: ', folder_metadata

# f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
# out = open('magnum-opus.txt', 'w')
# out.write(f.read())
# out.close()
# print metadata