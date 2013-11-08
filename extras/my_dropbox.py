# Include the Dropbox SDK
import dropbox
import sqlite3
import pickle
import json
import smtplib
import urllib2
from threading import *
from io        import open
from shutil    import * 

class Dropbox(object):
  def __init__(self, username, profile, location, content):
    self.profile   = profile                        # Set user profile
    self.location  = location                       # Set user location
    self.content   = content                        # Set user content 
    self.user_path = u"../users/" + username + u"/" # Set user path and directory

    # Get your app key and secret from the Dropbox developer website
    self.app_key = u'2ycmk3mndjuvija'
    self.app_secret = u'f6v4pvhsirmr5tw'

    self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)

    self.conn = sqlite3.connect(u'../server/cosn.db')   # Connect to sqlite database and print success message
    self.username = username                            # Set local username
    self.token = self.has_token()                       # Set token if exists
    if not self.token == u'': self.set_client()         # Set client and account information 

    # Do updating uploads in a separate thread because it takes too damn long
    t = Thread(target = self.initial_uploads)
    t.start()

  def initial_uploads(self):
    self.upload_file("profile.json")                    # Upload user profile
    self.upload_file("content.json")                    # Upload user content

    # Set location variables
    self.location["links"]["content"] = self.client.media(self.username + u"/content.json")
    self.location["links"]["public"]  = self.client.media(self.username + u"/profile.json")
    self.save_user_file("location.json", self.location) # Save location to file
    self.upload_file("location.json")                   # Upload location

  def auth_url(self):
    return self.flow.start()

  def get_token(self, auth_code):
    if self.token == u'':
      # This will fail if the user enters an invalid authorization code
      self.token, self.user_id = self.flow.finish(auth_code)
      self.set_client()
      self.conn.execute(u"INSERT INTO dropbox(username, token) VALUES(?, ?)", [self.username, self.token])
      self.conn.commit()
    return self.token

  def set_client(self):
    self.client = dropbox.client.DropboxClient(self.token) 
    self.acct = self.client.account_info()

  # Set token if it's stored inthe database. otherwise return a blank string
  def has_token(self):
    cursor = self.conn.execute(u"SELECT * FROM dropbox WHERE username = ? LIMIT 1", [self.username])
    token = u''
    for row in cursor:
      if row[0]:
        token = row[1]
    if token: return token
    return u''

  def upload_file(self, filename):
    f = open(self.user_path + filename)
    self.upload(f, filename)

  def upload(self, f, filename):
    try:
      self.client.file_delete(self.username + u"/" + filename)
    except:
      dont_care = True
    response = self.client.put_file(self.username + u"/" + filename, f.read())

  def save_user_file(self, filename, json_obj):
    filepath = self.user_path + filename
    with open(filepath, 'wb') as outfile:
      json.dump(json_obj, outfile, indent=2, sort_keys=True)


  def download_file(self, loc_url):
    response = urllib2.urlopen(loc_url)
    return json.load(response)

  def username_from_url(self, url):
    print self.download_file(url)

  def send_friend_request(self, email):
    self.media = self.client.media(self.username + u"/profile.json")
    SUBJECT = u'COSN Friend Request'
    TEXT = u'You\'re friend, '+ self.username + u', has sent you a friend request. \n\n Follow this link to accept the shared profile ' + self.media[u'url']

    gmail_sender = u'cosnunr@gmail.com'
    gmail_passwd = u'cosnpassword'

    server = smtplib.SMTP(u'smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = u'\r\n'.join([u'To: %s' % email, u'From: %s' % gmail_sender, u'Subject: %s' % SUBJECT, u'', TEXT])

    try:
      server.sendmail(gmail_sender, [email], BODY)
      print u'email sent'
    except:
      print u'error sending mail'

    server.quit()

