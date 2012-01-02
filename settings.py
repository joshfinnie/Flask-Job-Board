"""
You can store your app's configuration settings here.

Generate good secret keys:  http://flask.pocoo.org/docs/quickstart/#sessions
    >>> import os
    >>> os.urandom(24)
    '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
"""

SECRET_KEY = "this_is_my_secret_key_that_I_should_change_with_os.urandom"

MONGODB_DATABASE = 'app2312735'
MONGODB_SERVER	= 'staff.mongohq.com'
MONGODB_PORT = '10092'
MONGODB_USER = 'heroku'
MONGODB_PASSWORD = 'ded467f4021d3ca1c394707cbb2a8760'