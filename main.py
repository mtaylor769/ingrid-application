from flask import Flask, request
import mysql.connector
from mysql.connector import errorcode
import time

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['GOOGLE_LOGIN_REDIRECT_SCHEME'] = "https"
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
#import json

DBCONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'findme',
    'raise_on_warnings': True
}

apptoken = 'cf02308c614e080009c7fb0c4b19ff8a'

##
# Authentication
##
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    error = None
    if request.method == 'POST':
        if request.form('action') & request.form['action'] != '':
            if valid_login(request.form['username'], request.form['password']):
                return log_the_user_in(request.form['username'])
            else:
                error = 'Invalid username/password'
    else:
        error = request.form['username']
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return "end hello()"
    #return render_template('login.html', error=error)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

##
# User Defined Handler Functions
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

