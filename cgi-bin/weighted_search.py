#!/usr/bin/python
# coding: utf-8

import datetime
from config import *

__doc__ = """Handles weighted searches by performing scoring on tags."""

def get_score_values_restaurants(cursor, restaurant_ids):
    """Gets the scores for tags of the list of restaurants.

    @param cursor is the MySQL cursor.
    @param restaurant_ids is a list of integer restaurant IDs.

    @return dict whose key is restaurant ID and its value
        is a dictionary whose key is "tag name" and value is 1.
    """

    rest_score = {}
    query = 'SELECT tag_name AS tag, rest_id FROM tags WHERE ' + \
        ' OR '.join(['rest_id=%s'] * len(restaurant_ids))
    dprint('{0}: Getting restaurant scores using {1}'.format(
        'get_score_values_restaurants', query))
    cursor.execute(query, restaurant_ids)
    for entry in cursor:
        tag = entry[0]
        rest_id = entry[1]
        if not rest_score.has_key(rest_id):
            rest_score[rest_id] = {}
        # The score of each tag for a restaurant is exactly one.
        # Because restaurants can only have a tag once.
        rest_score[rest_id][tag] = 1
    dprint('Restaurant score by tags: ' + str(rest_score))
    return rest_score

def get_user_score_by_tag(cursor, username):
    """Gets the user's score: the number of tag references in their visits.

    @param cursor is the MySQL cursor.
    @param username is the string user's name.

    @return dict whose key is "tag name" and its value is the integer
        number of times it was referenced in the user's Visits history.
    """

    # Get the counts of each tag based on the restaurants the user visited.
    user_score = {}
    query = 'SELECT tag_name, COUNT(tag_name) FROM tags_of_all_visits ' \
        'WHERE username=%s GROUP BY tag_name'
    dprint(query)
    cursor.execute(query, (username,))
    for entry in cursor:
        tag = entry[0]
        count = entry[1]
        # TODO: Multiply by the number of times the restaurant was visited.
        user_score[tag] = count
    dprint('User score is {0}'.format(str(user_score)))
    return user_score

def get_static_score(cursor, user_scores, particular_rest_scores,rating=1):
    """Gets score(r, u): the score of a restaurant for a user."""
    cumulative_score = 0
    dprint('Particular restaurant\'s scores: {0}'.format(
        particular_rest_scores))
    for tag, value in user_scores.iteritems():
        if tag in particular_rest_scores:
            # The score gets user_score * rest_score, but rest_score is 1.
            # Hence, we can just add the user_score to the total score.
            cumulative_score += value
            dprint('Tag, value tuple ({0}, {1}) updated score to {2}.'.
                format(tag, str(value), str(cumulative_score)))
        else:
            dprint('Tag, value tuple ({0}, {1}) did not change the score.'.
                format(tag, str(value)))
    return float(cumulative_score)

def get_query_score_on_restaurant(cursor, particular_rest_scores, query_list):
    cumulative_score = sum([0] + [1 for query in query_list \
        if query in particular_rest_scores])
    """
    cumulative_score = 0
    for query in query_list:
        if query in particular_rest_scores:
            # The score gets query_score * rest_score, but both are 1.
            cumulative_score += 1
            dprint(''.join([query, ' is a restaurant tag. Score is now ',
                str(cumulative_score)]))
        else:
            dprint(tag + " not in restaurant's list of tags.")
    """
    return cumulative_score

def get_final_score(cursor, user_scores, particular_rest_scores, query_list,
        alpha=1.4):
    """Gets score(r, u, q): The score for a restaurant, user, and query."""
    static_score = get_static_score(cursor, user_scores,
        particular_rest_scores)
    query_score = get_query_score_on_restaurant(cursor,
        particular_rest_scores, query_list)
    final_score = alpha * static_score + (1.0 - alpha) * query_score
    dprint('Final score is {0}'.format(final_score))
    if DEBUG_PRINT and 0:
        formated_score = ', '.join(
            ['({0}, {1:.3})'.format(tag, score) \
                for tag, score in final_score.iteritems()] )
        dprint('Final score is {0}'.format(formated_score))
    return final_score

def _debug_test_scoring(cursor):
    """This is a sandbox used to test any functionality."""
    # There should only be one user searching. Choose this guy.
    user_scores = get_user_score_by_tag(cursor, 'userid')
    partiular_rest_id = 8
    # Get scores for all restaurants this user has visited.
    rest_scores = get_score_values_restaurants(cursor,
        [partiular_rest_id, 12, 19])
    # Try testing our functions on exactly one restaurant.
    # Get the score for one of these restaurants.
    particular_rest_scores = rest_scores[partiular_rest_id]
    # Get the score between the user and a restaurant. For testing.
    static_score = get_static_score(cursor, user_scores,
        particular_rest_scores)
    # Make up a search query that the user would make.
    query_list = ['dinner']
    # Get the score between a restaurant and a query. For testing.
    query_score = get_query_score_on_restaurant(cursor,
        particular_rest_scores, query_list)
    # Get the score now weighted with a query string. This is the true result.
    final_score = get_final_score(cursor, user_scores,
        particular_rest_scores, query_list)
    print('Static score which is score(r, u): ' + str(static_score))
    print('Query score which is score(r, q): ' + str(query_score))
    print('Final score which is score(r, u, q): ' + str(final_score))

if __name__ == '__main__':
    conn = None
    try:
        conn = mysql.connector.connect(user=db_user, password=db_pass,
            host=db_loc, database=db_name)
        cursor = conn.cursor()
        _debug_test_scoring(cursor)
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


