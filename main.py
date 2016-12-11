from flask import Flask, request, render_template, logging
import mysql.connector
from mysql.connector import errorcode
import uuid
import datetime
import decimal
import json
import httplib2
'''
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = build('compute', 'v1', credentials=credentials)
'''
PROJECT = 'ingrid-application'
ZONE = 'us-central1'
#apptoken = 'AIzaSyBRrOaEbGsZsX1u-zZZwtv938C3KIHJZ3A'

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'AIzaSyBRrOaEbGsZsX1u-zZZwtv938C3KIHJZ3A'
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
                    return render_template('output.html', data=user_signup())
                elif action == "profile":
                    uid = user_id or request.args.get('user_id', '')
                    return render_template('output.html', data=user_update(user_id))
        elif request.method == "PATCH":
            return user_update(user_id)
        else:
            uid = user_id or request.args.get('user_id', '')
            if uid is None or uid is '':
                data = get_all_users()
            else:
                data = get_user(uid)
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
                    return render_template('output.html', data=getdata('')),\
                        200, {'Content-Type': 'application/json; charset=utf-8'}
                elif action == "advanced":
                    return render_template('output.html', data=getdata('')),\
                        200, {'Content-Type': 'application/json; charset=utf-8'}
                elif action == "directory":
                    return render_template('output.html', data=getdata('')),\
                        200, {'Content-Type': 'application/json; charset=utf-8'}
            else:
                if user_id != None:
                    data = user_update(user_id)
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
                    return render_template('output.html', data=contacts_invite(contact_id))
                elif action == "remove":
                    if user_id == None:
                        user_id = request.args.get('user_id', '')
                        contact_id = request.args.get('contact_id', '')
                    return render_template('output.html',\
                        data=delete_user_contact(user_id, contact_id))
                elif action == "block":
                    if user_id is None:
                        user_id = request.args.get('user_id', '')
                    return render_template('output.html', data=user_update(user_id))
                elif action == "unblock":
                    if user_id is None:
                        user_id = request.args.get('user_id', '')
                    return render_template('output.html', data=user_update(user_id))
        elif request.method == "PATCH":
            return user_update(user_id)
        elif request.method == "DELETE":
            return delete_user_contact(user_id, contact_id)
        else:
            if user_id is None:
                user_id = request.args.get('user_id', '')
            if user_id != None:
                data = get_user_contacts(user_id)
            else:
                data = get_all_user_contacts()
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
                    return render_template('output.html', data=group_create())
                elif action == "update":
                    if user_id == None:
                        user_id = request.args.get('user_id', '')
                        contact_id = request.args.get('contact_id', '')
                    return render_template('output.html',\
                        data=update_group(group_id, user_id))
                elif action == "changeowner":
                    if group_id is None:
                        user_id = request.args.get('user_id', '')
                    return render_template('output.html', data=change_group_owner(user_id))
        elif request.method == "PATCH":
            return user_update(user_id)
        elif request.method == "DELETE":
            return delete_user_contact(user_id, contact_id)
        else:
            if user_id is None:
                user_id = request.args.get('user_id', '')
            if user_id != None:
                data = get_user_contacts(user_id)
            else:
                data = get_all_groups()
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
# Login page handler Functions
##
def valid_login(username, password):
    username = username
    password = password
    return True

def log_the_user_in(username):
    expiration = datetime.time() + 60 * 60 * 24
    username = username
    retarray = {
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

###
# User query functions
##
Q_users = "SELECT * FROM findme.tbl_users"
Q_limit = " LIMIT 10"

def user_update(user_id):
    return status_message("success", "user_id: " + user_id + " updated.")

def status_message(status=None, message=None):
    return {'status': status, 'message': message}

def get_all_users():
    return getdata(Q_users)

def get_user(uid=None):
    if uid is None:
        return status_message("fail", "user_id not passed")
    else:
        return getdata(Q_users + " WHERE `id`='" + str(uid) + "'")

###
# User Contacts query functions
##
Q_contacts = "SELECT * FROM findme.tbl_contacts"

def get_all_user_contacts():
    return getdata(Q_contacts)

def get_user_contacts(uid):
    return getdata(Q_contacts + " WHERE `user_id`='" + str(uid) + "'")

def contacts_invite(uid):
    return

def contacts_block(uid, cid):
    Q_block_user_contact = "UPDATE findme.tbl_contacts SET (`status`) VALUES (0)"\
        + Q_WHERE_user_contact(uid, cid)
    stat = getdata(Q_block_user_contact)
    return stat

def contacts_unblock(uid, cid):
    Q_unblock_user_contact = "UPDATE findme.tbl_contacts SET (`status`) VALUES (1)"\
        + Q_WHERE_user_contact(uid, cid)
    stat = getdata(Q_unblock_user_contact)
    return

def delete_user_contact(uid, cid):
    Q_delete_user_contact = "DELETE from findme.tbl_contacts"\
        + Q_WHERE_user_contact(uid, cid)
    stat = getdata(Q_delete_user_contact, format='')
    return stat

def Q_WHERE_user_contact(uid, cid):
    return " WHERE `user_id`='" + uid + "' `contact_id`='" + cid + "'"

###
# Groups query functions
##
Q_groups = "SELECT * FROM findme.tbl_groups"

def get_all_groups():
    return getdata(Q_groups)

def group_create():
    return

def update_group(gid, mid):
    return

def change_group_owner(uid):
    return
##
# MySQL Connector and query function
##
DBCONFIG = {
    'host': '127.0.0.1',
    'user': 'dbuser',
    'password': 'MySQL123!',
    'database': 'findme',
    'raise_on_warnings': False
}

def getdata(sql="SHOW TABLES", format='json'):
    msg = ''
    try:
        cnx = mysql.connector.connect(**DBCONFIG)
        cursor = cnx.cursor(buffered=True)
        if sql is None:
            sql = "SHOW TABLES"
        print sql
        cursor.execute(sql)
        query_result = [dict(line) \
            for line in [zip([column[0] \
                for column in cursor.description], row) \
                    for row in cursor.fetchall() \
            ] \
        ]
        '''
        numrows = cursor.rowcount
        for x in xrange(0, numrows):
            result = cursor.fetchone()
            d = [ dict(line) for line in [zip([ column[0] for column in cursor.description], result)
            msg += json.dump(result, d)
            if x != numrows:
                msg += ","
        '''
        cursor.close()
        if format == 'json':
            return jsondumps(query_result)
        else:
            return query_result
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msg += "\nYour Database username or password is not correct."
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            msg += "\nDatabase '" + DBCONFIG['database'] + "' does not exist."
        else:
            msg += "\n General DB Error: " + err.msg
    else:
        cnx.close()
    return msg

###
# set specific json.dumps behavior and filter
##
def jsondumps(myobj):
    return json.dumps(myobj, indent=4, skipkeys=True, ensure_ascii=False, sort_keys=True,\
        separators=(',', ':'), default=jsonfilter)

def jsonfilter(myobj):
    if type(myobj) is dict:
        return dict(myobj)
    if type(myobj) is datetime.date or type(myobj) is datetime.datetime:
        return myobj.isoformat()
    if type(myobj) is decimal.Decimal:
        return float(myobj)
