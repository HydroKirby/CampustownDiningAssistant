#!/usr/bin/python
# coding: utf-8

import datetime
from config import *

__doc__ = """Handles DB calls involving user history.

THIS FILE IS DEPRECATED.
SEE MANAGE_DB.PY"""

def get_visited_rests_tags(cursor, user_id, rest_id):
    """Returns a list of tag IDs of a restaurant that the user visited."""
    query = 'SELECT DISTINCT tag_name FROM tags, visits WHERE ' \
        'visits.user_id = %s AND visits.rest_id = %s AND tags.rest_id = %s'
    cursor.execute(query, (user_id, rest_id, rest_id))
    for name in cursor:
        print(name)

def weighted_search(cursor, tags=[]):
    success = True
    query = 'SELECT DISTINCT id FROM restaurants, tags WHERE'
    query += ' OR'.join([' tag_name LIKE %s'] * len(tags))
    dprint(query)
    cursor.execute( query, *tags )
    # We executed the query to get the restaurant IDs.
    # Get the IDs and print them out.
    ids = [id for id in cursor]
    if ids:
        dprint('Got restaurant IDs ' + \
            ', '.join([str(id[0]) for id in ids]))
        for id in ids:
            print_restaurant_for_web(cursor, id[0])
    else:
        dprint('No restaurants found.')

def add_visit(cursor, user_id, rest_id):
    """Logs a user's visit to a restaurant.

    Returns True on success and False otherwise.
    """

    success = True
    query = 'INSERT INTO visits (user_id, rest_id) VALUES (%s, %s)'
    try:
        cursor.execute(query, (user_id, rest_id))
    except MySQLdb.Error, err:
        print(err)
    return success

def _debug_visits_function(cursor=None):
    """This function is a placeholder to do anything! Not for release."""
    #get_visited_rests_tags(cursor, 1, 15)
    #add_visit(cursor, 1, 8)
    date = datetime.datetime.now()
    date = date.strftime('%Y-%m-%d')
    print(date)

if __name__ == '__main__':
    conn = None
    try:
        conn = mysql.connector.connect(user=db_user, password=db_pass,
            host=db_loc, database=db_name)
        cursor = conn.cursor()
        _debug_visits_function(cursor)
        conn.commit()
        cursor.close()
    except KeyboardInterrupt as err:
        pass
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err) 
    finally:
        if conn:
            conn.close()
        else:
            print('Error: Failed to connect to the database.')

