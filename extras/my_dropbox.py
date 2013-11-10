import sys
sys.path.append(u'../requests')

# Include the Dropbox SDK
import dropbox
import sqlite3
import pickle
import json
import smtplib
import os
from threading import *
from io        import open
from shutil    import * 
import requests

class Dropbox(object):
  def __init__(self, username, profile, location, content, view):
    self.profile   = profile                        # Set user profile
    self.location  = location                       # Set user location
    self.content   = content                        # Set user content
    self.view      = view                           # Set view for logging 
    self.user_path = u"../users/" + username + u"/" # Set user path and directory

    # Get your app key and secret from the Dropbox developer website
    self.app_key = u'2ycmk3mndjuvija'
    self.app_secret = u'f6v4pvhsirmr5tw'

    self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)

    self.conn = sqlite3.connect(u'../server/cosn.db')   # Connect to sqlite database
    self.username = username                            # Set local username
    self.token = self.has_token()                       # Set token if exists
    if self.token != u'': 
      self.set_client() # Set client and account information 
      # Do updating uploads in a separate thread because it takes too damn long
      t = Thread(target = self.initial_uploads)
      t.start()
    else:
      self.auth_url()

  def initial_uploads(self):
    self.upload_file("profile.json")                    # Upload user profile
    self.upload_file("content.json")                    # Upload user content

    # Set location variables
    self.location["links"]["content"] = self.client.media(self.username + u"/content.json")
    self.location["links"]["public"]  = self.client.media(self.username + u"/profile.json")
    self.save_user_file("location.json", self.location) # Save location to file
    self.upload_file("location.json")                   # Upload location

  def auth_url(self):
    self.view.log("Copy the following url into your browser to link dropbox")
    self.view.log("Then copy the code into the link dropbox input")
    self.view.log(self.flow.start())

  def get_token(self, auth_code):
    if self.token == u'':
      try: 
        # This will fail if the user enters an invalid authorization code
        self.token, self.user_id = self.flow.finish(auth_code)
        self.set_client()
        query = u"INSERT INTO dropbox(username, token) VALUES(?, ?)"
        self.conn.execute(query, [self.username, self.token])
        self.conn.commit()
      except: 
        return False
    return True

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

  def save_user_media(self, filename, content):
    f = open(filename, "wb")
    f.write(content)
    f.close()

  def download_and_save(self, filename, url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
      with open(filename, 'wb') as f:
        for chunk in r.iter_content():
          f.write(chunk)

  def download_file(self, loc_url):
    response = requests.get(url=loc_url)
    return json.loads(response.content)

  def accept_friend(self, url, conn):
    friend = self.download_file(url)
    self.add_friend(friend, url, conn if conn != None else self.conn)
    return (friend["address"]["IP"], friend["address"]["port"])

  def add_friend(self, friend, url, conn): 
    query = u"SELECT * FROM friend WHERE username = ? AND friend = ? LIMIT 1"
    cursor = conn.execute(query, [self.username, friend["address"]["ID"]])
    for row in cursor:
      if row[0]:
        return
    query = u"INSERT INTO friend(username, friend, location_url) VALUES(?, ?, ?)"
    conn.execute(query, [self.username, friend["address"]["ID"], url])
    conn.commit()

  def share_url(self):
    self.media = self.client.media(self.username + u"/location.json")
    return self.media["url"]

  def get_location(self, friend):
    query = u"SELECT location_url FROM friend WHERE username = ? AND friend = ? LIMIT 1"
    cursor = self.conn.execute(query, [self.username, friend])
    user = cursor.fetchone()
    if user != None: return self.download_file(user[0])
    return None

  def get_profile(self, friend):
    loc = self.get_location(friend)
    if loc != None: 
      return (self.download_file(loc["links"]["public"]["url"]), 
              self.download_file(loc["links"]["content"]["url"]))
    return None

  def download_content(self, path, content):
    filepath = path + "/content/" 
    if not os.path.exists(filepath): os.makedirs(filepath)
    for item in content:
      media_file = filepath + item["id"] + self.extension(item["type"])
      if os.path.isfile(media_file): continue
      if item["type"] == "text": 
        self.save_user_media(media_file, item["info"])
      elif item["type"] == "video":
        self.save_user_media(media_file, item["info"] + '\n' + item["url"])
      else:
        self.download_and_save(media_file, item["url"])

  def extension(self, file_type):
    if file_type == "text": 
      return ".txt"
    elif file_type == "image": 
      return ".jpg"
    elif file_type == "video":
      return ".txt"
    elif file_type == "audio":
      return ".mp3"

  def get_friend_files(self, friend):
    profile, content = self.get_profile(friend)
    if profile == None: return False
    filepath = self.user_path + "friends/" + friend + "/"
    if not os.path.exists(filepath): os.makedirs(filepath)
    self.save_user_file("friends/" + friend + "/profile.json", profile)
    self.download_content(filepath, content)

  def send_friend_request(self, email):
    SUBJECT = u'COSN Friend Request'
    TEXT = """You\'re friend, '+ self.username + u', has sent you a friend request. \n\n 
              Follow this link to accept the shared profile""" + self.share_url()

    gmail_sender = u'cosnunr@gmail.com'
    gmail_passwd = u'JJ9VxgGjuwKeJ7L'

    server = smtplib.SMTP(u'smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = u'\r\n'.join([u'To: %s' % email, 
                         u'From: %s' % gmail_sender, u'Subject: %s' % SUBJECT, u'', TEXT])

    try:
      server.sendmail(gmail_sender, [email], BODY)
      print u'email sent'
    except:
      print u'error sending mail'

    server.quit()

