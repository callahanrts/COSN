#!/usr/bin/python
import sqlite3
import pickle
import httplib2
import pprint
import mimetypes

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from apiclient import errors

class Drive:
  def __init__(self, username):    
    # Store user's username
    self.username = username

    # Initialize mimetypes object
    mimetypes.init()

    # Copy your credentials from the console
    self.CLIENT_ID = '346355476366-p65ou25kvsihb4tnpu7ctgmsrnp55psg.apps.googleusercontent.com'
    self.CLIENT_SECRET = 'zdB0Sn8zL1jRztIuR8Iq2SVQ'

    # Check https://developers.google.com/drive/scopes for all available scopes
    self.OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

    # Redirect URI for installed apps
    self.REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    # Path to the file to upload
    FILENAME = 'document.txt'

    # Connect to sqlite database and print success message
    self.conn = sqlite3.connect(u'../server/cosn.db')

  def authorize(self):
    self.has_credentials()
    if self.credentials == None:
      # Run through the OAuth flow and retrieve credentials
      self.flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE, self.REDIRECT_URI)
      self.authorize_url = self.flow.step1_get_authorize_url()

      print 'To use this app, you must first connect it to a dropbox account'
      print 'Go to the following link in your browser: ' + self.authorize_url
      code = raw_input('Enter verification code: ').strip()
      self.credentials = self.flow.step2_exchange(code)

    # Store credentials when you get them
    self.store_credentials()

    # Create an httplib2.Http object and authorize it with our credentials
    self.http = httplib2.Http()
    self.http = self.credentials.authorize(self.http)

    self.drive_service = build('drive', 'v2', http=self.http)

  def store_credentials(self):
    self.conn.execute(u"INSERT INTO drive(username, credentials) VALUES(?, ?)", [self.username, pickle.dumps(self.credentials)]) 
    self.conn.commit()

  def has_credentials(self):
    self.credentials = None
    cursor = self.conn.execute(u"SELECT * FROM drive WHERE username = ? LIMIT 1", [self.username])
    for row in cursor:
      if row[0]:
        self.credentials = pickle.loads(row[1])

  def upload_profile(self):
    title = "cosn_profile"
    description = "JSON Profile"
    filename = "../users/" + self.username + "/" + self.username + ".json"
    self.insert_file(title, description, filename)

  # Insert new file.
  # Args:
    # service: Drive API service instance.
    # title: Title of the file to insert, including the extension.
    # description: Description of the file to insert.
    # parent_id: Parent folder's ID.
    # mime_type: MIME type of the file to insert.
    # filename: Filename of the file to insert.
    # Returns:
    # Inserted file metadata if successful, None otherwise.
  def insert_file(self, title, description, filename):
    mime_type = mimetypes.guess_type(filename)
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {
      'title': title,
      'description': description,
      'mimeType': mime_type
    }

    # Set the parent folder.
    #if parent_id:
    #  body['parents'] = [{'id': parent_id}]
    try:
      print self.drive_service
      file = self.drive_service.files().insert(body=body, media_body=media_body).execute()
      # Uncomment the following line to print the File ID
      # print 'File ID: %s' % file['id']
      return file

    except errors.HttpError, error:
      print 'An error occured: %s' % error
      return None


