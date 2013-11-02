# Include the Dropbox SDK
import dropbox

class Dropbox:
  def __init__(self):
    # Get your app key and secret from the Dropbox developer website
    self.app_key = '2ycmk3mndjuvija'
    self.app_secret = 'f6v4pvhsirmr5tw'

    self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(self.app_key, self.app_secret)


  def auth_url(self):
    return self.flow.start()



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