#!/usr/bin/python
#! coding: utf-8

from manage_db import *
from display_web import *

def act_on_args_query(input_values, cursor, conn=None):
    arg_parse_success = True
    if input_values.updateshow:
        argstring = ' '.join(input_values.updateshow)
        dprint('Updating businesses by tag ' + argstring)
        # Updates businesses by querying Yelp, then displays them.
        businesses = call_yelp.query_yelp(argstring)
        if businesses:
            for bus in businesses:
                update_business(conn, cursor, bus, input_values.updateshow)
            # Display the restaurants for the web.
            dprint('Printing businesses by tag ' + argstring)
            if input_values.username:
                #print_rests_by_tag_for_web_user(cursor, input_values.username, argstring)
                print_rests_by_tag_weighted(cursor, input_values.username, argstring)
            else:
                print_rests_by_tag_for_web(cursor, argstring, 10)
        else:
            wprint('<p>No businesses found.</p>')
    elif input_values.web:
        # Display the restaurants for the web.
        print_for_web(cursor, tags=[input_values.web])
    elif input_values.visits:
        if input_values.username:
            print_visits_for_web(cursor, input_values.username)
        else:
            wprint('<p>You can only view your history of visits' \
                ' when you are logged in.</p>')
    elif input_values.output and input_values.output[0] in table_names:
        # The program was requested to print a table.
        toprint = input_values.output[0]
        if toprint == 'users':
            print_users(cursor)
        elif toprint == 'restaurants':
            print_restaurants(cursor)
        elif toprint == 'tags':
            print_tags(cursor)
        elif toprint == 'reviews':
            print_reviews(cursor)
        elif toprint == 'visits':
            print_visits(cursor)
        else:
            arg_parse_success = False
    elif input_values.introspect:
        # Make a search request to Yelp and output the response.
        businesses = call_yelp.query_yelp(input_values.introspect)
        bus = businesses[0]
        call_yelp.introspect_business(bus)
    else:
        arg_parse_success = False
    return arg_parse_success

def act_on_args_add(input_values, cursor, conn=None):
    arg_parse_success = True
    if input_values.term:
        # Make a search request to Yelp and work with the response.
        dprint('Adding a business with terms ' + input_values.term)
        businesses = call_yelp.query_yelp(input_values.term)
        for bus in businesses:
            update_business(conn, cursor, bus, [input_values.term])
    elif input_values.reg:
        reg = input_values.reg
        if len(reg) != 4:
            print('Error: Invalid number of arguments to register.')
            arg_parse_success = False
        if user_into_db(cursor, conn, reg[0], reg[1], reg[2], reg[3]):
            print('User successfully registered.')
        else:
            print('Error: Failed to register the user.')
    else:
        arg_parse_success = False
    return arg_parse_success

def act_on_args_delete(input_values, cursor, conn=None):
    arg_parse_success = True
    name = ' '.join(input_values.name)
    addr = ' '.join(input_values.addr)
    # Demolish a restaurant.
    if demolish_rest(cursor, name, addr):
        wprint('<p>Demolished the restaurant named {0} at {1}.</p>.'.format(
            name, addr))
    else:
        wprint('<p>Could not find a restaurant named {0} at {1}.</p>'.format(
            name, addr))
    return arg_parse_success

def act_on_args_visit(input_values, cursor, conn=None):
    arg_parse_success = True
    user_name = input_values.visit[0]
    rest_id = int(input_values.visit[1])
    date = None
    if len(input_values.visit) <= 2 or input_values.visit[2] == 'date':
        # The word "date" is passed as a temporary parameter
        # back when this function was tested being called in PHP.
        # It bears no semantical meaning.
        pass
    else:
        date = input_values.visit[2]
    insert_visit(cursor, user_name, rest_id, date)
    return arg_parse_success

def act_on_args(cursor, conn=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    query_parser = subparsers.add_parser('query',
        description='Query the DB for info.')
    query_parser.add_argument('-o', '--output', nargs=1, dest='output',
        type=str, help=''.join(['Output a table (',
        ', '.join(table_names), ')']))
    query_parser.add_argument('-i', '--introspect', dest='introspect',
        type=str, help='Introspect a Yelp query')
    query_parser.add_argument('-w', '--web', dest='web', type=str,
        nargs='+', help='Print search query results for the web page.')
    query_parser.add_argument('-u', '--updateshow', dest='updateshow',
        type=str, nargs='+', help='Update restaurants and show for the web.')
    query_parser.add_argument('-n', '--name', dest='username',
        type=str, help='Username')
    query_parser.add_argument('-v', '--visits', dest='visits',
        action='store_true', help='Print the history of visits for a user.')

    add_parser = subparsers.add_parser('add',
        description='Add a restaurant or user to the DB.')
    add_parser.add_argument('-t', '--term', dest='term', type=str,
        help='Search term (default: %(default)s)')
    add_parser.add_argument('-r', '--register', nargs=4, dest='reg', type=str,
        help='Register a user (name, email, pass, pass_verify)')

    delete_parser = subparsers.add_parser('delete',
        description='Delete a restaurant from the DB.')
    delete_parser.add_argument('-n', '--name', dest='name', type=str,
        nargs='+', required=True, help="Restaurant's name")
    delete_parser.add_argument('-a', '--address', dest='addr', type=str,
        nargs='+', required=True, help="Restaurant's address")
    
    visit_parser = subparsers.add_parser('visit',
        description='Visit a restaurant with some user.')
    visit_parser.add_argument('-v', '--visit', dest='visit', type=str,
        nargs=2, required=True,
        help='Visit a restaurant (Username, Restaurant ID)')

    unregister_parser = subparsers.add_parser('unregister',
        description='Unregister a user from the DB.')
    unregister_parser.add_argument('-n', '--name', dest='name', type=str,
        nargs='+', required=True, help="Username")
    unregister_parser.add_argument('-p', '--password', dest='pass', type=str,
        nargs='+', required=True, help="Password")
    
    arg_parse_success = True
    subcmd = None
    if len(argv) >= 2:
        # argv[0] is the path to this file.
        # argv[1] is the sub command.
        # Hence, we need at least two commands to run properly.
        subcmd = argv[1]
        input_values = parser.parse_args(argv[1:])

    if subcmd == 'query':
        arg_parse_success = arg_parse_success and \
            act_on_args_query(input_values, cursor, conn)
        if not arg_parse_success:
            query_parser.print_help()
            arg_parse_success = True
    elif subcmd == 'add':
        arg_parse_success = arg_parse_success and \
            act_on_args_add(input_values, cursor, conn)
        if not arg_parse_success:
            add_parser.print_help()
            arg_parse_success = True
    elif subcmd == 'delete':
        arg_parse_success = arg_parse_success and \
            act_on_args_delete(input_values, cursor, conn)
        if not arg_parse_success:
            delete_parser.print_help()
            arg_parse_success = True
    elif subcmd == 'visit':
        arg_parse_success = arg_parse_success and \
            act_on_args_visit(input_values, cursor, conn)
        if not arg_parse_success:
            visit_parser.print_help()
            arg_parse_success = True
    else:
        # No valid input arguments.
        arg_parse_success = False

    if not arg_parse_success:
        parser.print_help()

def main():
    try:
        conn = mysql.connector.connect(user=db_user, password=db_pass,
            host=db_loc, database=db_name)
        cursor = conn.cursor(buffered=True)
        act_on_args(cursor, conn)
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

if __name__ == '__main__':
    main()

