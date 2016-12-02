from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import errorcode
import uuid
import time
import json

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['GOOGLE_LOGIN_REDIRECT_SCHEME'] = "https"
if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.debug = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
## Author: Mike Taylor

DBCONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'findme',
    'raise_on_warnings': True
}

apptoken = 'cf02308c614e080009c7fb0c4b19ff8a'

###
# oAuth2 Authentication Login
##
@app.route('/')
def index():
    return "logged in"
    #return flask.redirect(flask.url_for('login'))

'''
    import flask
    import httplib2
    from oauth2client import client
    from apiclient import discovery
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v2', http_auth)
        files = drive_service.files().list().execute()
        return json.dumps(files)


@app.route('/oauth2callback')
def oauth2callback():
    import flask
    import httplib2
    from oauth2client import client
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/drive.metadata.readonly',
        redirect_uri=flask.url_for('oauth2callback', _external=True),
        include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))
'''

###
# Users
##
@app.route('/user/', methods=["GET"])
@app.route('/users/', methods=["GET"]) # List of users
@app.route('/users/<int:user_id>')
def userprofile(user_id=None):
    """
    Returns:
        user_profile
    Args:
        POST   /user?action=signup      - v1 user registration
        POST   /user?action=profile     - v1 user update
        PATCH  /users/<user_id>         - v2 user update
    """
    error = None
    try:
        action = request.args.get('action', '')
        user_id = request.args.get('user_id', '')
        if request.method == "POST" | request.method == "GET":
            if action != '':
                if action == "signup":
                    return render_template('output.html', data=user_signup())
                elif action == "profile":
                    return render_template('output.html', data=user_update())
            else:
                if user_id != None:
                    data = user_update()
                else: data = status_message('fail', "no user_id")
            return render_template('output.html', data=data)
        else:
            return request.method + " requested"
    except KeyError as identifier:
        error = "FormError: " + identifier.message
        return render_template('error.html', error=error)

##
#  Search
##
@app.route('/search')
def search():
    """
    Returns:
        user_profile list
    Args:
        POST   /search?action=general       - v1 general user search
        POST   /search?action=advanced      - v1 advanced user search
        GET    /users                       - v2 user list

    Returns:
        directory list
    Args:
        POST   /search?action=directory     - v1 general group search
        GET    /directories                 - v2 group list
    """
    error = None
    try:
        action = request.args.get('action', 'search')
        user_id = request.args.get('user_id', '')
        if request.method == "POST" | request.method == "GET":
            if action != '':
                if action == "general":
                    return render_template('output.html', data=getdata())
                elif action == "advanced":
                    return render_template('output.html', data=getdata())
                elif action == "directory":
                    return render_template('output.html', data=getdata())
            else:
                if user_id != None:
                    data = user_update()
                else: data = status_message('fail', "no user_id")
            return render_template('output.html', data=data)
        else:
            return request.method + " requested"
    except KeyError as identifier:
        error = "FormError: " + identifier.message
        return render_template('error.html', error=error)


###
#  Contacts
##
@app.route('/contacts')
@app.route('/users/<int:user_id>/contacts/')
@app.route('/users/<int:user_id>/contacts/<int:contact_id>')
@app.route('/users/<int:user_id>/contacts/<int:contact_id>/block')
@app.route('/users/<int:user_id>/contacts/<int:contact_id>/unblock')
def contacts(user_id=None, contact_id=None):
    """
    Returns:
        contact list
    Args:
        POST   /contacts/?action=get        - v1 admin general contact search
        GET    /users/<user_id>/contacts    - v2 admin user contact list
            TODO: resolve this route with client
        GET    /users/<user_id>             - v2 admin user edit (SEE: Users above)

    Returns:
        status message
    Args:
        POST   /contacts/?action=invite     - v1 user invitation
        POST   /users/<user_id>/contacts    - v2 admin user contact list
            TODO: add 'invite' ?

        POST   /contacts/?action=remove     - v1 user contact delete
        DELETE /users/<user_id>/contacts/<contact_id>  - v2 user contact delete

        POST   /contacts?action=block       - v1 block user contact
        POST   /users/<user_id>/contacts/<contact_id>/block  - v2 block user contact

        POST   /contacts?action=unblock     - v1 unblock user contact
        POST   /users/<user_id>/contacts/<contact_id>/unblock  - v2 unblock user contact
    """
    retarray = {}
    return render_template('list.html', data=retarray)

##
#  Groups
##
@app.route('/group')
@app.route('/groups')
@app.route('/groups/<int:group_id>')
@app.route('/groups/<int:group_id>/members')
@app.route('/groups/<int:group_id>/members/<int:user_id>')
def groups(group_id=None, user_id=None):
    """
    Returns:
        group list
    Args:
        POST   /search?action=group         - v1 general group search
        POST   /groups/?action=get          - v1 admin general contact search
        GET    /groups/?action=getmembers&group_id=<group_id>  - v1 group member list
        GET    /groups/<group_id>/members   - v2 group member list

    Returns:
        status message
    Args:
        GET    /groups/?action=invite&group_id=<group_id>  - v1 group invite
        GET    /groups/?action=join&group_id=<group_id>    - v1 group join
        POST   /groups/[group_id]/members                  - v2 group invite / join
            TODO: add 'invite'/'join' and user_id ***

        POST   /groups/?action=leave&group_id=<group_id>&user_id=<user_id>  - v1 leave group
        DELETE /groups/[group_id]/members/[user_id]        - v2 leave group

        POST  /groups/?action=removemember&group_id=<group_id>&user_id=<user_id>
            - v1 remove group member
        DELETE /groups/<group_id>/members/<user_id>        - v2 remove group member

    Returns:
        group
    Args:
        POST   /groups/?action=create       - v1 group create
        POST   /groups/                     - v2 group create
            TODO: resolve this URL

        POST   /groups/?action=update       - v1 update group
        PATCH  /groups/<group_id>           - v2 update group
            TODO: resolve this URL

        POST   /groups/?action=changeowner&group_id=<group_id>&owner_id=<user_id> - v1 change owner
        PATCH  /groups/<group_id>
            TODO: add owner_id ?

    """
    retarray = {}
    return render_template('list.html', data=retarray)

##
#  Directories
##
@app.route('/directories')
@app.route('/directories/')
@app.route('/directories/<directory_id>/members')
def directories(directory_id=None, user_id=None):
    """
    Returns:
        directory list
    Args:
        POST   /directories/?action=get          - v1 admin general contact search
        GET    /directories                      - v2 directory list

    Returns:
        directory member list
    Args:
        GET   /directories/?action=getmembers&directory_id=<directory_id> - v1 directory member list
        GET   /directories/<directory_id>/members  - v2 directory member list

    Returns:
        status message
    Args:
        POST /directories/?action=join&directory_id=<directory_id>  - v1 join directory
        POST /directories/?action=verify&directory_id=<directory_id> - v1 join directory -deprecated
        POST /directories/[directory_id]/members                     - v2 join directory
            TODO: add 'invite'/'join' and user_id

        POST /directories/?action=leave&directory_id=<directory_id>&user_id=<member_id>
            - v1 leave group
        DELETE /directories/<directory_id>/members/<member_id>        - v2 leave group
            TODO: switch user_id and member_id ?

    """
    retarray = {}
    return render_template('list.html', data=retarray)

##
#  Notifications (Invitations and Updates)
##
@app.route('/notifications')
@app.route('/notifications/')
@app.route('/notifications/<msg_id>')
@app.route('/invitations')
@app.route('/invitations/<msg_id>')
@app.route('/updates')
@app.route('/updates/<msg_id>')
def notifications(msg_id=None):
    """
    Returns:
        invitation list
    Args:
        POST   /notifications/?action=invitations  - v1 invitation list
        GET    /invitations                        - v2 invitation list

    Returns;
        invitation
    Args:
        POST   /notifications/?action=read&id=<invitation_id>  - v1 read invitation
        GET    /invitations/<invitation_id>        - v2 read invitation

    Returns:
        status message
    Args:
        POST   /notifications/?action=accept&invitation_id=<invitation_id>
            - v1 accept invitation
        POST   /notifications/?action=reject&invitation_id=<invitation_id>
            - v1 reject invitation
        PATCH /invitations/<invitation_id>         - v2 accept / reject notification
            TODO: add action?

    Returns:
        updates list
    Args:
        POST   /notifications/?action=updates      - v1 updates list
        GET    /updates                            - v2 updates list

    """
    retarray = {}
    return render_template('list.html', data=retarray)

##
#  Settings
##
@app.route('/settings')
@app.route('/settings/')
def settings(directory_id=None, user_id=None):
    """
    Returns:
        settings model
    Args:
        POST   /settings/?action=get&user_id=<user_id>     - v1 get settings
        POST   /settings/                                  - v2 get settings

        POST   /settings/?action=update&user_id=<user_id>  - v1 update settings
        POST   /settings/?action=changeemail&user_id=<user_id>
            - v1 update settings -deprecated
        PATCH /settings                                    - v2 update settings
    """
    retarray = {}
    return render_template('list.html', data=retarray)

##
#  404 NOT FOUND
##
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

##
# User Defined Handler Functions
##


##
# Login page handler Functions
##
def valid_login(username, password):
    username = username
    password = password
    return True

def log_the_user_in(username):
    expiration = time.time() + 60 * 60 * 24
    username = username
    retarray = {
        'auth_token': apptoken,
        'expires': expiration
    }
    return retarray

def user_signup():
    retarray = {
        'app_action': 'user_signup',
        'id': request.args.get('id', 'dafault_id'),
        'user_id': request.args.get('user_id', 'default_user_id'),
        'email': request.args.get('email', 'default_email'),
        'first_name': request.args.get('first_name', 'default_first_name'),
        'last_name': request.args.get('last_name', 'default_last_name'),
        'password': request.args.get('password', 'default_password'),
        'organization': request.args.get('organization', 'default orgainization'),
        'designation': request.args.get('designation', 'default deignation'),
        'location_latitude': request.args.get('location_latitude', 'location_latitude'),
        'location_longitude': request.args.get('location_longitude', 'location_longitude'),
        'location': [{
            'lat': request.args.get('location_latitude', 'location_latitude'),
            'lon': request.args.get('location_longitude', 'location_longitude')
        }],
        'profile_picture': request.args.get('profile_picture', ''),
        'contacts': request.args.get('contacts', '')
    }
    return retarray

def user_update():
    return status_message("success", "user_id: 1 updated")

def status_message(status=None, message=None):
    return {'status': status | "no status", 'message': message | "no message"}

##
# MySQL Connector and query function
##
def getdata(query):
    msg = ''
    try:
        cnx = mysql.connector.connect(**DBCONFIG)
        cursor = cnx.cursor(buffered=True)
        if query == '':
            query = "DESCRIBE DATABASE"
        cursor.execute(query)
        for (i, j) in cursor:
            msg += "{} {}".format(i, j)
        cursor.close()
        cnx.close()
        msg += "The Database is Connected"
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msg += "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            msg += "Database does not exist"
        else:
            msg += "DB Error: " + err.msg
    else:
        cnx.close()
        msg += "Connection closed."
    return msg

