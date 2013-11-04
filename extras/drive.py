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
    self.get_user()
    if self.user == None:
      # Run through the OAuth flow and retrieve credentials
      self.flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE, self.REDIRECT_URI)
      self.authorize_url = self.flow.step1_get_authorize_url()

      print 'To use this app, you must first connect it to a dropbox account'
      print 'Go to the following link in your browser: ' + self.authorize_url
      code = raw_input('Enter verification code: ').strip()
      self.credentials = self.flow.step2_exchange(code)
      self.user = [self.username, self.credentials, None]

    else:
      # Get credentials out of user opbject
      self.credentials = pickle.loads(self.user[1])

    # Create an httplib2.Http object and authorize it with our credentials
    self.http = httplib2.Http()
    self.http = self.credentials.authorize(self.http)

    self.drive_service = build('drive', 'v2', http=self.http)

    # Store credentials when you get them
    self.store_credentials()

    # Insert file to drive if we don't have a record of it
    self.upload_profile()

  def store_credentials(self):
    self.conn.execute(u"INSERT INTO drive(username, credentials, profile) VALUES(?, ?, ?)", [self.username, pickle.dumps(self.credentials), None]) 
    self.conn.commit()

  def get_user(self):
    self.user = None
    cursor = self.conn.execute(u"SELECT * FROM drive WHERE username = ? LIMIT 1", [self.username])
    for row in cursor:
      if row[0]:
        self.user = row

  # Args:
  #   service: Drive API service instance.
  #   file_id: ID of the file to insert permission for.
  #   value: User or group e-mail address, domain name or None for 'default'
  #          type.
  #   perm_type: The value 'user', 'group', 'domain' or 'default'.
  #   role: The value 'owner', 'writer' or 'reader'.
  # Returns:
  #   The inserted permission if successful, None otherwise.
  def give_permission(self, email):
    file_id = None # Get file id from drive
    new_permission = {
      'value': email,
      'type': 'user',
      'role': 'reader'
    }
    try:
      return self.drive_service.permissions().insert(fileId=file_id, body=new_permission).execute()
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
    return None


  def upload_profile(self):
    # Upload profile to google drive
    filename = "../users/" + self.username + "/" + self.username + ".json"
    
    if self.user[2] == None:
      self.profile = self.insert_file("cosn_profile", "JSON Profile", filename)
    else:
      print self.user[2]
      self.profile = self.update_file(self.user[2], "cosn_profile", "JSON Profile", filename)

    # Update user to store profile
    self.get_user()

    # Save profile for later
    self.conn.execute(u"UPDATE drive SET profile = ? WHERE username = ?", [pickle.dumps(self.profile), self.username]) 
    self.conn.commit()

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

  # Update an existing file's metadata and content.

  # Args:
  #   service: Drive API service instance.
  #   file_id: ID of the file to update.
  #   new_title: New title for the file.
  #   new_description: New description for the file.
  #   new_mime_type: New MIME type for the file.
  #   new_filename: Filename of the new content to upload.
  #   new_revision: Whether or not to create a new revision for this file.
  # Returns:
  #   Updated file metadata if successful, None otherwise.
  def update_file(self, file_id, new_title, new_description, new_filename):  
    mime_type = mimetypes.guess_type(new_filename)
    try:
      # First retrieve the file from the API.
      file = self.drive_service.files().get(fileId=file_id).execute()

      # File's new metadata.
      file['title'] = new_title
      file['description'] = new_description
      file['mimeType'] = new_mime_type

      # File's new content.
      media_body = MediaFileUpload(
        new_filename, mimetype=new_mime_type, resumable=True)

      # Send the request to the API.
      updated_file = self.drive_service.files().update(
        fileId=file_id,
        body=file,
        newRevision=True,
        media_body=media_body).execute()
      return updated_file
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      return None      


