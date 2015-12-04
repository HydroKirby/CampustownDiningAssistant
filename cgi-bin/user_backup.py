def times_visited(cursor, username):
    query = "SELECT SUM(count) as times_visited FROM visits WHERE username=%s GROUP BY rest_id ORDER BY total_visits DESC"
    cursor.execute(query,(username,))
    return cursor

def total_visits(cursor, username):
    query = "SELECT SUM(count) as total_visits FROM visits WHERE username=%s"
    cursor.execute(query,(username,))
    return cursor.fetchone()[0]

def prev_rests_with_tag(cursor, username, tag): 
    t_visits = total_visits(cursor,username)
    if(t_visits >= 3):
        # Grab the rest_ids and times the user visited them
        query = ''.join(['SELECT b.id,a.total_visits ' ,
        # Grabs the rest_ids and total times the user visited each rest_id
        # The restaurant must comprise of at least 5% of the total visits
        'FROM (SELECT rest_id, SUM(count) as total_visits ' ,
        'FROM visits WHERE username=%s ' ,
        'GROUP BY rest_id HAVING total_visits*100.0/%s >= 5) a ' ,
        # Finds all restaurants with the searched tag which have also been visited by the user
        'INNER JOIN (SELECT * from visits INNER JOIN ' ,
        '(SELECT restaurants.id FROM restaurants INNER JOIN tags ' ,
        'ON restaurants.id = tags.rest_id WHERE tag_name=%s) s ON ',
        's.id = visits.rest_id WHERE visits.username = %s) b ON ' ,
        # Sort from most visited to least visited, and get the top 5
        'a.rest_id = b.id ORDER BY a.total_visits DESC LIMIT 5'])
        cursor.execute(query, (username, t_visits, tag, username))
        return cursor
    else:
        return None
    
    
    
