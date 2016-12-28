import json
import datetime
import decimal

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
##
# MySQL Connector and query function
##
DBCONFIG={
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'dbuser',
    'password': 'MySQL123!',
    'database': 'findme'
}

def getdata(sql="SHOW TABLES", fmt='json'):
    from mysql.connector import connection, errorcode, Error
    msg = ''
    try:
        cnx = connection.MySQLConnection(**DBCONFIG)
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
    except Error as err:
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
