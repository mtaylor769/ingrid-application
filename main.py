from flask import Flask, request, render_template, logging, jsonify
import uuid
import apiclient
import ingridapp
#from google.appengine.api import urlfetch
#urlfetch.set_default_fetch_deadline(200)
'''
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = build('compute', 'v1', credentials=credentials)
'''

PROJECT = 'ingrid-application'
ZONE = 'us-central1'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SECRET_KEY'] = 'AIzaSyBRrOaEbGsZsX1u-zZZwtv938C3KIHJZ3A'

app.config['GOOGLE_LOGIN_REDIRECT_SCHEME'] = "https"
app.config['GOOGLE_APPLICATION_CREDENTIALS'] = "./ingrid-application-f7e95ac782cc.json"

if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.debug = True
log = app.logger
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
## Author: Mike Taylor

###
# Oauth2 authentication through Google
##
@app.route('/')
def index():
    import flask
    import httplib2
    from oauth2client import client
    from apiclient import discovery
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
        #return flask.redirect('https://www.getpostman.com/oauth2/callback')
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
        #return flask.redirect('https://www.getpostman.com/oauth2/callback')
    else:
        http_auth = credentials.authorize(httplib2.Http())
        apiservice = discovery.build('appengine', 'v1', http_auth)
        #print apiservice
        return flask.redirect(flask.url_for('users'))
        #return "Services: " + jsondumps(apiservice)


@app.route('/oauth2callback')
def oauth2callback():
    import flask
    import httplib2
    from oauth2client import client
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope=[
            #'https://www.googleapis.com/auth/drive.appdata',
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/plus.login'
        ],
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))

def auth(url_for):
    import flask
    flask.session['request_uri'] = request.referrer or url_for
    return flask.redirect(flask.url_for('index'))

###
# Users
##
@app.route('/user', methods=["POST"])
@app.route('/users/')
@app.route('/users/<int:user_id>')
def users(user_id=None):
    """
    Returns:
        users list
    Args:
        GET /users/

    Returns:
        user_profile
    Args:
        POST   /user?action=signup      - v1 user registration
        POST   /user?action=profile     - v1 update user profile
        GET    /user?user_id=<user_id>  - v1 get user profile
        GET    /users/<user_id>         - v2 get user profile
        PATCH  /users/<user_id>         - v2 update user profile
    """
    auth('users')
    error = None
    try:
        if request.method == "POST":
            action = request.args.get('action', '')
            if action != '':
                if action == "signup":
                    return render_template('output.html', data=ingridapp.user_signup(request))
                elif action == "profile":
                    uid = request.args.get('user_id', '')
                    if uid is None or uid is '':
                        uid = user_id
                    return render_template('output.html', data=ingridapp.user_update(uid))
        elif request.method == "PATCH":
            return ingridapp.user_update(user_id)
        else:
            uid = user_id or request.args.get('user_id', '')
            if uid is None or uid is '':
                data = ingridapp.get_all_users()
            else:
                data = ingridapp.get_user(uid)
        return render_template('output.html', data=data)
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
    auth('search')
    error = None
    try:
        action = request.args.get('action', 'search')
        user_id = request.args.get('user_id', '')
        if request.method == "POST" | request.method == "GET":
            if action != '':
                if action == "general":
                    return render_template('output.html', data=ingridapp.getdata('')),\
                        200, {'Content-Type': 'application/json; charset=utf-8'}
                elif action == "advanced":
                    return render_template('output.html', data=ingridapp.getdata('')),\
                        200, {'Content-Type': 'application/json; charset=utf-8'}
                elif action == "directory":
                    return render_template('output.html', data=ingridapp.getdata('')),\
                        200, {'Content-Type': 'application/json; charset=utf-8'}
            else:
                if user_id != None:
                    data = ingridapp.user_update(user_id)
                else: data = ingridapp.status_message('fail', "no user_id")
            return render_template('output.html', data=data)
        else:
            return request.method + " requested"
    except KeyError as identifier:
        error = "FormError: " + identifier.message
        return render_template('error.html', error=error)


###
#  Contacts
##
@app.route('/contacts/')
@app.route('/contacts/<int:user_id>')
@app.route('/users/<int:user_id>/contacts/')
@app.route('/users/<int:user_id>/contacts/<int:contact_id>')
@app.route('/users/<int:user_id>/contacts/<int:contact_id>/block')
@app.route('/users/<int:user_id>/contacts/<int:contact_id>/unblock')
def contacts(user_id=None, contact_id=None):
    """
    Returns:
        contact list
    Args:
        GET    /contacts/?action=get        - v1 admin general contact search
        GET    /users/<user_id>/contacts    - v2 admin user contact list
            TODO: resolve this route with client
        GET    /contacts/?action=getcontacts  - v1 single user/contact
        GET    /users/<user_id>             - v2 single user/contact

    Returns:
        status message
    Args:
        POST   /contacts/?action=invite     - v1 send user invitation
        POST   /users/<user_id>/contacts    - v2 send user invitation
            TODO: add 'invite' ?

        POST   /contacts/?action=remove     - v1 user contact delete
        DELETE /users/<user_id>/contacts/<contact_id>  - v2 user contact delete

        POST   /contacts?action=block       - v1 block user contact
        POST   /users/<user_id>/contacts/<contact_id>/block  - v2 block user contact

        POST   /contacts?action=unblock     - v1 unblock user contact
        POST   /users/<user_id>/contacts/<contact_id>/unblock  - v2 unblock user contact
    """
    auth('contacts')
    error = None
    try:
        if request.method == "POST":
            action = request.args.get('action', '')
            if action != '':
                if action == "invite":
                    return render_template('output.html', data=ingridapp.contacts_invite(contact_id))
                elif action == "remove":
                    if user_id == None:
                        user_id = request.args.get('user_id', '')
                        contact_id = request.args.get('contact_id', '')
                    return render_template('output.html',\
                        data=ingridapp.delete_user_contact(user_id, contact_id))
                elif action == "block":
                    if user_id is None:
                        user_id = request.args.get('user_id', '')
                    return render_template('output.html', data=ingridapp.user_update(user_id))
                elif action == "unblock":
                    if user_id is None:
                        user_id = request.args.get('user_id', '')
                    return render_template('output.html', data=ingridapp.user_update(user_id))
        elif request.method == "PATCH":
            return ingridapp.user_update(user_id)
        elif request.method == "DELETE":
            return ingridapp.delete_user_contact(user_id, contact_id)
        else:
            if user_id is None:
                user_id = request.args.get('user_id', '')
            if user_id != None:
                data = ingridapp.get_user_contacts(user_id)
            else:
                data = ingridapp.get_all_user_contacts()
        return render_template('output.html', data=data)
    except KeyError as identifier:
        error = "FormError: " + identifier.message
        return render_template('error.html', error=error)

##
#  Groups
##
@app.route('/group')
@app.route('/groups/')
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
    auth('groups')
    error = None
    try:
        if request.method == "POST":
            action = request.args.get('action', '')
            if action != '':
                if action == "create":
                    return render_template('output.html', data=ingridapp.group_create())
                elif action == "update":
                    if user_id == None:
                        user_id = request.args.get('user_id', '')
                        contact_id = request.args.get('contact_id', '')
                    return render_template('output.html',\
                        data=ingridapp.update_group(group_id, user_id))
                elif action == "changeowner":
                    if group_id is None:
                        user_id = request.args.get('user_id', '')
                    return render_template('output.html',\
                        data=ingridapp.change_group_owner(user_id))
        elif request.method == "PATCH":
            return ingridapp.user_update(user_id)
        elif request.method == "DELETE":
            return ingridapp.delete_user_contact(user_id, contact_id)
        else:
            if user_id is None:
                user_id = request.args.get('user_id', '')
            if user_id != None:
                data = ingridapp.get_user_contacts(user_id)
            else:
                data = ingridapp.get_all_groups()
        return render_template('output.html', data=data)
    except KeyError as identifier:
        error = "FormError: " + identifier.message
        return render_template('error.html', error=error)


##
#  Directories
##
@app.route('/directories')
@app.route('/directories/')
@app.route('/directories/<directory_id>/members')
def directories(directory_id=None,):
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
    auth('settings')
    retarray = {}
    return render_template('list.html', data=retarray)

##
#  404 NOT FOUND
##
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
