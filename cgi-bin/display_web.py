#!/usr/bin/python
# coding: utf-8

from config import *
from user_visits import *
from weighted_search import *

def wprint(text):
    """Prints text for the web.

    This function actually does nothing. Using this function signifies
    that the print call is intended for the webpage rather than for
    diagnostics.
    """

    print(text)

def pprint_phone_number(phone_str):
    """Takes a string of numbers and formats it as a phone number.

    Example: "1112223333" becomes "(111) 222-3333"
    Returns the fixed phone string on success or the original string on failure
    """
    ret = phone_str
    if len(phone_str) == 10:
        ret = ''.join(['(', phone_str[0:3], ') ', phone_str[3:6], '-',
            phone_str[6:]])
    elif len(phone_str) == 11:
        ret = ''.join([phone_str[0], '-', phone_str[1:4], '-',
            phone_str[4:7], '-', phone_str[7:]])
    return ret

def print_restaurant_for_web(cursor, id, visit=False, score=1.0):
    """Prints a restaurant on a web page.

    @param cursor The MySQL cursor instance.
    @param id The integer index of the restaurant ID in the database.
    @param visit Boolean saying whether or not to display the Visit button.
    @param score The floating point score the restaurant got in weighting.
    @returns None
    """

    rest = {}

    # Get the data for the restaurant.
    query = 'SELECT name, address, rating, phone from restaurants WHERE id=%s'
    cursor.execute(query, (id,))
    row = [row for row in cursor][0]
    rest['id'] = str(id)
    rest['name'] = row[0]
    rest['address'] = row[1]
    rest['rating'] = str(row[2])
    rest['phone'] = row[3]
    rest['restaurant'] = rest

    # Get the tags for the restaurant.
    query = 'SELECT tag_name from tags WHERE rest_id = %s'
    cursor.execute(query, (id,))
    rest['tags'] = [tag[0] for tag in cursor]
 
    # Get the review for the restaurant.
    query = 'SELECT snippet_text, rating from reviews WHERE rest_id = %s'
    cursor.execute(query, (id,))
    reviews = [review for review in cursor]
    rest['review_snippet'] = reviews[0][0]
    rest['review_rating'] = str(reviews[0][1])

    # Output the data to the web page.
    output_list = ['<div class="searchResult">\n']

    # Arbitrary div for layout purposes.
    output_list += ['<div class="srDiv1">']
    # Output the Yelp logo near the search result.
    # Showing the logo is required by contract with Yelp.
    output_list += ['<img src="', yelp_logo_path, '" class="yelp_logo">\n']

    if visit:
        # Output the weighted score of the restaurant.
        output_list += ['<span class="srWeight">Relevance: ', str(score),
            '</span> | \n']

    # Output the restaurant name.
    output_list += ['<span class="srName">Name: ', rest['name'],
        '</span> | \n']
    # Output rating.
    output_list += ['<span class="srRating">Rating: ', rest['rating'],
        '</span>\n']
    # Output visit button.
    if visit:
        output_list += ['<form action="index.php" method="post"'
            ' style="display:inline">\n'
            '\t<input type="submit" name="visit" value="Visit">\n'
            '\t<input type="hidden" name="restid" value=',
            str(id), '>\n</form>\n']
    output_list += ['</div>']

    output_list += ['<div class="srDiv2">']
    # Output tags.
    output_list += ['<span class="srTags">Tags: ']
    output_list += [', '.join(rest['tags'])]
    output_list += ['</span>\n']
    output_list += ['</div>']

    output_list += ['<div class="srDiv3">']
    # Output location.
    output_list += ['<span class="srLoc">Address: ', rest['address'],
        '</span>\n']
    # Output phone number.
    output_list += ['<span class="srPhone"> | Phone: ',
        pprint_phone_number(rest['phone']), '</span>\n']
    output_list += ['</div>']

    output_list += ['<div class="srDiv4">']
    # Output review.
    output_list += ['<span class="srRevSnip">Review (', rest['review_rating'],
        '/5.0): ', rest['review_snippet'], '</span>\n']
    output_list += ['</div>']

    # Close the restaurant's output sequence.
    output_list += ['</div>\n']
    wprint(''.join(output_list))

def print_users(cursor):
    query = 'SELECT * FROM users'
    cursor.execute(query)
    for user in cursor:
        print('User {0} has ID {1} and email {2}.'.format(
            user[1], user[0], user[2]))

def print_restaurants(cursor):
    query = 'SELECT * FROM restaurants'
    cursor.execute(query)
    for rest in cursor:
        print('Restaurant {0} has name {1}, address {2}, and phone {3}.'.
            format(rest[0], rest[1], rest[2], rest[6]))

def print_tags(cursor):
    query = 'SELECT * FROM tags'
    cursor.execute(query)
    for tag in cursor:
        print('Tag {0} has id {1} is related to restaurant id {2}.'.format(
            tag[1], tag[0], tag[2]))

def print_reviews(cursor):
    query = 'SELECT * FROM reviews'
    cursor.execute(query)
    for rev in cursor:
        print('Review {0} has rating {1} for restaurant id {2}.'.format(
            rev[0], rev[1], rev[3]))

def print_visits(cursor):
    query = 'SELECT * FROM visits'
    cursor.execute(query)
    for visit in cursor:
        print('User {0} went to restaurant {1} on {2}.'.format(
            visit[0], visit[1], visit[3]))

def print_visits_for_web(cursor, username):
    """Prints all restaurants a user visited in tabular format."""
    query = 'SELECT rest_name, date, visits_count FROM user_visits_history' \
        ' WHERE username = %s'
    dprint('{0}: Getting history with user {1} and query {2}'.format(
        'print_visits_for_web', username, query))
    cursor.execute(query, (username,))
    if cursor.rowcount > 0:
        wprint('<table class="visits_history">')
        wprint('<thead>')
        wprint('\t<tr><th>Name</th><th>Date</th><th>Count</th></tr>')
        wprint('</thead>')
        wprint('<tbody>')
        for visit in cursor:
            wprint('\t<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(
                visit[0], visit[1], visit[2]))
        wprint('</tbody>')
        wprint('</table>')
    else:
        wprint('<p>You have not visited any restaurants yet.</p>')

def print_rests_by_tag_for_web(cursor, tag, num, used=[],visit=False): 
    query = 'SELECT DISTINCT rest_id FROM tags WHERE tag_name=%s'
    cursor.execute(query, (tag, ))
    ids = [id for id in cursor]
    ids_len = len(ids)
    if ids:
        dprint('Going to print restaurants: ' + \
            ', '.join([str(id[0]) for id in ids]))
        for x in range(0, min(ids_len,num)):
            if(ids[x][0] not in used):
                print_restaurant_for_web(cursor, ids[x][0],visit)
    else:
        wprint('<p>No restaurants found.</p>')

def print_rests_by_tag_for_web_user(cursor, username, tag):
    t_cursor = cursor
    cursor = prev_rests_with_tag(cursor, username, tag)
    if cursor:
        rests = [i for i in cursor]
        rest_len = min(10,len(rests))
        rest_ids = []
        for x in range(0, rest_len):
            rest_ids.append(rests[x][0])
            print_restaurant_for_web(cursor, rests[x][0],True)
        print_rests_by_tag_for_web(cursor, tag, 10-rest_len, rest_ids,True)    
    else:
        print_rests_by_tag_for_web(t_cursor, tag, 10, visit=True)

def print_rests_by_tag_weighted(cursor, username, tag):
    query = 'SELECT DISTINCT rest_id, rating from tags ' \
        'INNER JOIN restaurants ON rest_id = id WHERE tag_name=%s'
    dprint('{0}: User "{1}" and tag "{2}" used in {3}'.format(
        'print_rests_by_tag_weighted', username, tag, query))
    cursor.execute(query, (tag, ))
    ids = [id for id in cursor]
    rest_ids = []
    ratings = {}
    if ids:
        id_len = len(ids)
        for x in range(0, id_len):
            rest_ids.append(ids[x][0])
            ratings[rest_ids[x]] = ids[x][1]

        rest_scores = get_score_values_restaurants(cursor, rest_ids)
        user_score = get_user_score_by_tag(cursor, username)
        total_scores = []
        for idx,rest in enumerate(rest_scores):
            rest_id = rest_ids[idx]
            total_scores.append((rest_id,
                get_final_score(cursor, user_score, rest_scores[rest], [tag])))
        if DEBUG_PRINT:
            formatted_score = ', '.join(
                ['({0}, {1:.5})'.format(pair[0], pair[1]) \
                    for pair in total_scores] )
            dprint('Total scores as (Restaurant ID, Score) are {0}'.
                format(str(formatted_score)))
        total_scores.sort(key=lambda tup: tup[1], reverse=True)

        # Print the 10 or less restaurants we have found.
        id_len = min(10, id_len)
        used_ids = []
        for x in range(0, id_len):
            used_ids.append(total_scores[x][0])
            print_restaurant_for_web(cursor, total_scores[x][0], True,
                total_scores[x][1])
        # Print other results so that we have ten search results total.
        print_rests_by_tag_for_web(cursor, tag, 10-id_len, used_ids, True)
    else:
        # Print 10 results without weighting.
        print_rests_by_tag_for_web(cursor, tag, 10, visit=True)


def print_for_web(cursor, name=None, addr=None, tags=[]):
    """Prints a list of restaurants for the web.
    
    Returns True on success. False otherwise.
    """

    query = 'SELECT DISTINCT id FROM restaurants WHERE '
    success = False
    if name and addr:
        query += 'name LIKE %s AND address LIKE addr'
        dprint(query)
        cursor.execute( query, (name, addr) )
        success = True
    elif name:
        query += 'name LIKE %s'
        dprint(query)
        cursor.execute( query, (name,) )
        success = True
    elif addr:
        query += 'address LIKE %s'
        dprint(query)
        cursor.execute( query, (addr,) )
        success = True
    elif tags:
        query = 'SELECT id, name FROM restaurants WHERE id IN'
        query += ' (SELECT rest_id FROM tags WHERE'
        query += ' OR'.join([' tag_name LIKE %s'] * len(tags))
        query += ')'
        dprint(query)
        cursor.execute( query, *tags )
        success = True

    if success:
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
    return success

if __name__ == '__main__':
    try:
        conn = mysql.connector.connect(user=db_user, password=db_pass,
            host=db_loc, database=db_name)
        cursor = conn.cursor(buffered=True)
        #print_restaurant_for_web(cursor, 12)
        print_rests_by_tag_weighted(cursor, 'a', 'dinner')
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

