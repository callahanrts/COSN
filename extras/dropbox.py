class Dropbox:
	DROPBOX_APP_KEY = '<YOUR APP KEY>'
  DROPBOX_APP_SECRET = '<YOUR APP SECRET>'
	
  ##############################
  # Authenticating a user
  ##############################
  @app.route('/')
  def home():
    if not 'access_token' in session:
        return redirect(url_for('dropbox_auth_start'))
    return 'Authenticated.'

  @app.route('/dropbox-auth-start')
  def dropbox_auth_start():
    return redirect(get_auth_flow().start())

  @app.route('/dropbox-auth-finish')
  def dropbox_auth_finish():
    try:
      access_token, user_id, url_state = get_auth_flow().finish(request.args)
    except:
      abort(400)
    else:
      session['access_token'] = access_token
    return redirect(url_for('home'))

  def get_auth_flow():
    redirect_uri = url_for('dropbox_auth_finish', _external=True)
    return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, redirect_uri,
                             session, 'dropbox-auth-csrf-token')

  #############################################
  # Creating a datastore and your first table    
  #############################################
  def data_store():
  	access_token = session['access_token']
    client = DropboxClient(access_token)
    manager = DatastoreManager(client)
    datastore = manager.open_default_datastore()

  def data_table():
  	tasks_table = datastore.get_table('tasks')


  ##############
  # DB actions
  ##############
  def do_insert():
    tasks_table.insert(taskname='Buy milk', completed=False)
    datastore.transaction(do_insert, max_tries=4)

  def do_update():
    first_task.set('completed', True)
    datastore.transaction(do_update, max_tries=4)

  def do_delete():
    first_task.delete()
    datastore.transaction(do_delete, max_tries=4)

  def query():
    tasks = tasks_table.query(completed=False)
    for task in tasks:
      print task.get('taskname')