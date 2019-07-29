import json
import datetime
import decimal
import os

###
# User query functions
##
Q_users = "SELECT * FROM findme.tbl_users"
Q_limit = " LIMIT 10"

def user_signup(request):
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
    stat = getdata(Q_delete_user_contact, fmt='')
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

###
# Search query functions
##
def general_search(uid, kword):
    keyword = addslashes(kword)

    sql = "SELECT id, first_name, last_name, organization, profile_picture FROM tbl_users"
    # TODO: ADD JOIN FOR PROFILE PICTURE & MUTUAL CONTACTS
    sql += " where (((first_name like '%"+keyword+"%' or last_name like '%"+keyword+"%')\
        and find_by_name='1') or organization like '%"+keyword+"%' or user_id like\
        '%"+keyword+"%' or ((concat_ws(' ',first_name,last_name) like '%"+keyword+"%')\
        and find_by_name='1')"

    keywords = keyword.split(',')
    if keywords.length > 0:
        for keyword in keywords:
            sql += " or ((first_name like '%"+keyword+"%' or last_name like '%"+keyword+"%')\
                and find_by_name='1') or organization like '%"+keyword+"%'\
                or ((user_id like '%"+keyword+"%')\
                and find_by_userid='1')\
                or ((concat_ws(' ',first_name,last_name) like '%"+keyword+"%')\
                and find_by_name='1')"
    sql += ') and id!='+str(uid)+' and user_status="1"'
    stat = getdata(sql, fmt='')
    return stat

def advanced_search(uid, request):
    firstname = addslashes(request.args.get('firstname'))
    lastname = addslashes(request.args.get('lastname'))
    organization = addslashes(request.args.get('company'))
    location = addslashes(request.args.get('location'))
    nomi_id = addslashes(request.args.get('nomi_id'))

    sql = "SELECT id, first_name, last_name, organization, profile_picture FROM tbl_users where"
    # TODO: ADD JOIN FOR & MUTUAL CONTACT connection status
    query = ''

    if firstname != '':
        query += " ((first_name='"+firstname+"' or first_name like '%"+firstname+"%')\
            and find_by_name='1')"

    if lastname != '':
        if query == "":
            query += " or"
        query += " ((first_name='"+lastname+"' or first_name like '%"+lastname+"%')\
            and or find_by_name='1')"

    if organization != '':
        if query == "":
            query += " or"
        query += " (organization='"+organization+"' or organization like '%"+organization+"%')"

    if location != '':
        if query == "":
            query += " or"
        query += " (location='"+location+"' or location like '%"+location+"%')"

    if nomi_id != '':
        if query == "":
            query += " or"
        query += " ((user_id='"+nomi_id+"' or user_id like '%"+nomi_id+"%')\
                and find_by_userid='1')"

    query += ' and id!='+str(uid)+' and user_status="1"'
    stat = getdata(sql+query, fmt='')
    return stat

def group_search(uid, request):
    pin = addslashes(request.args.get('pin'))
    user_id = str(uid)

    sql = "SELECT grp.id,group_name,group_picture,owner,member_invite_contact,\
        password,phone,email,count(mem.id) as members FROM tbl_groups grp\
        INNER JOIN tbl_group_members mem on grp.id=mem.group_id and mem.status='1'\
        where grp.pin='"+pin+"'"
    stat = getdata(sql)
    return stat

def directory_search(uid, request):
    name = addslashes(request.args.get('name'))
    domain = addslashes(request.args.get('domain'))
    user_id = str(uid)

    sql = "SELECT id,directory_name,domain FROM tbl_directories\
        where directory_name like '%"+name+"%'"
    stat = getdata(sql)
    return stat
def mutual():
    usersql = "SELECT (case when (user_id = '$user') THEN contact_id ELSE user_id END)\
        as friend from tbl_contacts where (user_id='$user' or contact_id='$user') and status='1'"
    userres = getdata(usersql)
    contactsql = "SELECT (case when (user_id = '$contact') THEN contact_id ELSE user_id END)\
        as friend from tbl_contacts where (user_id='$contact' or contact_id='$contact') and\
        status='1'"
    contactres = getdata(contactsql, fmt='raw')
    return userres + contactres

def trylogin(username, password):
    loginsql = "SELECT * FROM tbl_users where username='"+username+"' and password='"+password+"'"
    loginres = getdata(loginsql)
    print loginres
##
# MySQL Connector and query function
##
DB_CNXN = os.getenv("CLOUDSQL_CONNECTION_NAME")
DB_SOCK = os.path.join("/cloudsql", DB_CNXN)
DB_USER = os.getenv("CLOUDSQL_USER")
DB_PASS = os.getenv("CLOUDSQL_PASSWORD")
DB_IPV4 = os.getenv("CLOUDSQL_SERVER_IP4V")
DB_PORT = os.getenv("CLOUDSQL_SERVER_PORT")
DB_DBNM = os.getenv("CLOUDSQL_DATABASE")
SV_SOFT = os.getenv('SERVER_SOFTWARE', '')


CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

DBCONFIG = {
    'host': DB_IPV4,
    #'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASS,
    'database': DB_DBNM,
    #'unix_socket': DB_SOCK
}

def getdata(sql="SHOW TABLES", fmt='json'):
    msg = ''
    import MySQLdb
    try:
        cnx = connect_to_cloudsql()
        cursor = cnx.cursor()
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
        if fmt == 'json':
            return jsondumps(query_result)
        else:
            return query_result
    except MySQLdb.DatabaseError as err:
        return err
    else:
        cnx.close()
    return msg

###
# Utility functions
##

###
# String functions
##
def addslashes(s):
    '''
    return a string_escape decoded, stripped (trimmed) string
    equivalent to "addslashes(trim($_POST['<fieldname>'));" in PHP
    '''
    return s.decode('string_escape').strip()

###
# JSON: set specific json.dumps behavior and filter
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

###
# GCP recommended connector for Unix Socket preferred,
##

def connect_to_cloudsql():
    import MySQLdb
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host="wmcp-mysql", port=3306, db="findme", user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db
