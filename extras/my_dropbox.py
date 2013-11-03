# Include the Dropbox SDK
import dropbox
import sqlite3
import pickle
import json
import smtplib

class Dropbox:
  def __init__(self, username):
    # Set user path and directory
    self.user_dir = "../users/"
    self.user_path = self.user_dir + username + "/" 

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
    if not self.token == '': self.set_client()

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
    print(self.acct)

  # Set token if it's stored inthe database. otherwise return a blank string
  def has_token(self):
    cursor = self.conn.execute("SELECT * FROM dropbox WHERE username = ? LIMIT 1", [self.username])
    token = ''
    for row in cursor:
      if row[0]:
        token = row[1]
    if token: return token
    return ''

  def upload_profile(self):
    f = open(self.user_path + self.username + ".json")
    self.upload(f, self.username + ".json")

  def upload_file(self, filename):
    f = open(user_dir + filename)
    self.upload(f, filename)

  def upload(self, f, filename):
    self.client.file_delete(self.username + "/" + filename)
    response = self.client.put_file(self.username + "/" + filename, f.read())
    print("uploaded: \n")

  def send_friend_request(self, email):
    self.share = self.client.share(self.username + "/")
    SUBJECT = 'COSN Friend Request'
    TEXT = 'You\'re friend, '+ self.username + ', has sent you a friend request. \n\n Follow this link to accept the shared profile ' + self.share['url']

    gmail_sender = 'cosnunr@gmail.com'
    gmail_passwd = 'cosnpassword'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % email, 'From: %s' % gmail_sender, 'Subject: %s' % SUBJECT, '', TEXT])

    try:
      server.sendmail(gmail_sender, [email], BODY)
      print ('email sent')
    except:
      print ('error sending mail')

    server.quit()

