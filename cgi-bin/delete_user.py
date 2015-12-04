#!/usr/bin/python
# coding: utf-8

from config import *

def delete_user(cursor, username, password):
    """Deletes a user.

    @param cursor The MySQL cursor instance.
    @param username The user's name string.
    @param password The user's password.

    @return True on success; False otherwise.
    """

    success = True
    query = 'SELECT name, pass FROM users WHERE name=%s'
    dprint('{0}: Getting name and pass with {1}'.format('delete_user', query))
    cursor.execute(query, (username,))
    users = [pair for pair in cursor]
    if not len(users):
        print('Username not found.')
        success = False
    else:
        # We do not need the name now.
        #name = users[0][0]
        stored_password = users[0][1]
        if password != stored_password:
            print('Incorrect password.')
            success = False
        else:
            # Delete the user.
            query = None
            # Delete the user's visits.
    return success

