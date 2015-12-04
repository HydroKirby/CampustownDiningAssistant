#!/usr/bin/python
#! coding: utf-8

from config import *
from sys import argv
from os.path import dirname, join as path_join
from user_visits import *
import datetime
import argparse
import call_yelp
try:
    import mysql.connector
    from mysql.connector import errorcode
except ImportError as err:
    print('Connector/Python module from Oracle is not installed.')
    print('Download and install it from https://dev.mysql.com/')
    raise err
from display_web import *

__doc__ = """Handles all data I/O for the Yelp Restaurants database.

Authors: Larry Resnik and Richard Shen
Year: 2015
"""

DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Champaign, IL'

table_names = ['users', 'restaurants', 'reviews', 'tags', 'visits']

def get_default_db_path():
    return path_join(dirname(argv[0]), db_name)

def get_img_path(img_url):
    """Takes the URL to a Yelp restaurant thumbnail and gets its relative path.

    Ex: http://s3-media4.fl.yelpcdn.com/bphoto/Ot-ccD6LDopqcqeI04kIBg/ms.jpg
        becomes Ot-ccD6LDopqcqeI04kIBg/ms.jpg
    """
    return img_url[img_url[:img_url.rfind('/') - 1].rfind('/') + 1:]

def user_into_db(cursor, conn, name, email, password, password_verify):
    """Inputs a user into the database."""
    success = True
    dprint('Inputting user into DB')
    response = cursor.execute(
        "INSERT INTO users (name, email, pass) VALUES (%s,%s,%s)",
        (name, email, password))
    success = success and bool(response)
    return success

def update_business(conn, cursor, bus, terms=[]):
    """Adds a restaurant or updates one that already exists."""
    rest_name = bus['name']
    if bus['location']['address']:
        address = bus['location']['address'][0]
    else:
        address = ''
    dprint('{0}: Counting restaurants with name "{1}" and address "{2}"'.
        format('update_business', rest_name, address))
    cursor.execute('SELECT COUNT(id) FROM restaurants '
        'WHERE address="%s" AND name="%s"', (address, rest_name))
    count = [i for i in cursor][0][0]
    if count <= 0:
        # There are no restaurants in the DB like this. Add it.
        rest_id = business_into_db(cursor, bus, terms)
    elif count == 1:
        # Get the existing restaurant's id.
        dprint('Getting a restaurant ID')
        query = r'SELECT id FROM restaurants ' \
            r'WHERE address=%s AND name=%s'
        cursor.execute( query, (address, rest_name) )
        id = [i for i in cursor][0][0]

        # Update the existing restaurant.
        dprint('Updating restaurant {0}'.format(id))
        query = r"UPDATE restaurants SET name=%s, " \
            r"address=%s, rating=%s, review_count=%s, closed=%s, " \
            r"phone=%s WHERE id=%s"
        cursor.execute(query, (
            rest_name, address, bus["rating"],
            bus["review_count"], bus["is_closed"], bus["phone"], id))
        update_tags_bus(cursor, bus, id)
        add_tags_list(cursor, terms, id)
        update_reviews(cursor, bus, id)
    else:
        # The query matched multiple restaurants! This is an error.
        raise Exception('Error: Multiple restaurants updatable from 1 query.')

def business_into_db(cursor, bus, terms):
    """Adds a restaurant into the DB and returns its ID."""
    dprint('Inserting a restaurant')
    closed = bool(bus['is_closed'])
    query = "INSERT INTO restaurants " \
        "(name, address, rating, review_count, closed, phone) " \
        r"VALUES (%s,%s,%s,%s,%s,%s)"
    if bus["location"]["address"]:
        address = bus["location"]["address"][0]
    else:
        address = ''
    cursor.execute(query, (
        bus["name"], address, bus["rating"],
        bus["review_count"], closed, bus["phone"]))
    id = cursor.lastrowid
    tags_into_db_bus(cursor, bus, id)
    add_tags_list(cursor, terms, id)
    review_into_db(cursor, bus, id)
    return id

def update_tags_bus(cursor, bus, id):
    """Removes tags of a restaurant's id, then adds the passed bus' tags."""
    dprint('Deleting tags from Yelp query')
    cursor.execute("DELETE FROM tags WHERE rest_id=%s", (id,))
    tags_into_db_bus(cursor, bus, id)

def tags_into_db_bus(cursor, bus, id):
    """Inserts tags into the DB from the Yelp DB."""
    dprint('Inserting tags from Yelp query')
    for category in bus["categories"]:
        cursor.execute("INSERT INTO tags "
            "(tag_name,rest_id) VALUES (%s,%s) ON DUPLICATE KEY UPDATE tag_name=%s", (category[1],id, category[1]))

def add_tags_list(cursor, terms, id):
    """Adds the passed list's tags for a restaurant."""
    dprint('Inserting tags from search terms')
    for category in terms:
        cursor.execute("INSERT INTO tags "
            "(tag_name,rest_id) VALUES (%s,%s) ON DUPLICATE KEY UPDATE tag_Name=%s", (category,id,category))

def update_reviews(cursor, bus, rest_id):
    dprint('Findng review for an existing restaurant')
    query = 'SELECT review_id FROM reviews WHERE rest_id=%s'
    cursor.execute(query, (rest_id, ))
    if cursor.rowcount <= 0:
        review_into_db(cursor, bus, rest_id)
    else:
        review_id = [i for i in cursor][0][0]
        dprint('Updating review {0}'.format(review_id))
        snippet_text = bus['snippet_text']
        query = 'UPDATE reviews SET ' \
            'rating=%s, yelp_user_id=%s, rest_id=%s, snippet_text=%s WHERE ' \
            'review_id=%s'
        cursor.execute( query, (
            bus['rating'], None, rest_id, snippet_text, review_id) )
        

def review_into_db(cursor, bus, rest_id):
    snippet_text = bus['snippet_text']
    dprint('Inserting a review')
    query = 'INSERT INTO reviews ' \
        '(rating, yelp_user_id, rest_id, snippet_text) ' \
        'VALUES (%s, %s, %s, %s)'
    cursor.execute( query, (
        bus['rating'], None, rest_id, snippet_text) )

def delete_rows(cursor, table, column, value):
    cursor.execute("DELETE FROM %s WHERE %s=%s", (
        table, column, value))

def insert_visit(cursor, username, rest_id, date):
    query = 'SELECT date from visits WHERE username = %s AND rest_id = %s' \
            ' AND date = %s'
    if not date:
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d')
    dprint(query % (username, rest_id, date))
    cursor.execute(query, (username, rest_id, date))
    if (cursor.rowcount <= 0):
        query = 'INSERT INTO visits (username, rest_id, date, count)' \
                'VALUES (%s, %s, %s, 1)'
    else:
        query = 'UPDATE visits SET count=count+1 WHERE username=%s ' \
                'AND rest_id=%s AND date=%s'
    dprint(query)
    cursor.execute(query, (username, rest_id, date))

def demolish_rest(cursor, name, address):
    """Removes a restaurant and all related data from the DB.
    
    Returns True on success. False otherwise.
    """

    success = True
    query = 'SELECT id FROM restaurants WHERE name=%s AND address=%s'
    cursor.execute( query, (name, address) )
    if (cursor.rowcount > 0):
        id = [id for id in cursor][0][0]
        dprint('Deleting restaurant with ID {0}'.format(id))

        query = 'DELETE FROM restaurants WHERE id=%s'
        cursor.execute( query, (id, ) )
        query = 'DELETE FROM tags WHERE rest_id=%s'
        cursor.execute( query, (id, ) )
        query = 'DELETE FROM reviews WHERE rest_id=%s'
        cursor.execute( query, (id, ) )
        query = 'DELETE FROM visits WHERE rest_id=%s'
        cursor.execute( query, (id, ) )
        dprint('Deleted from restaurants, tags, reviews, and visits.')
    else:
        print('Error: No restaurant matching this criteria.')
        success = False
    return success

