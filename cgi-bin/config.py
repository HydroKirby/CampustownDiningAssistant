try:
    import mysql.connector
    from mysql.connector import errorcode
except ImportError as err:
    print('Connector/Python module from Oracle is not installed.')
    print('Download and install it from https://dev.mysql.com/')
    raise err

__doc__ = """Holds configuration variables for the main program."""

DEBUG_PRINT = 0
db_user = 'campusdi_rests'
db_pass = 'rests'
db_name = 'campusdi_rests'
db_loc = 'localhost'
yelp_logo_path = 'img/yelp_logo_40x20.png'

def dprint(text):
    """Print debug text."""
    if DEBUG_PRINT:
        print('<br> ' + text)

