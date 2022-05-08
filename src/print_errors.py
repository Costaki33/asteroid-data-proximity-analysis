'''
This file will contian all the error messages and other items that will be printed to the user
'''

#This will print the correct curling command to the user
def error(correct_curl):
    '''
    This function will return the correct curling command for each curl command that was incorrectly inputted by
    the user.

    Input:
        correct_curl (string) it is the correct command for that specific route

    Output:
        (string) it will be the correct command for the user to use.

    '''
    return f'\n\n[Error]: Invalid curl for this route. Here is the correct command for this route.\n     {correct_curl}\nRetype the command above to get the correct results.\n\n'


#This function will print the welcome message to the user    
def welcome_message():
    '''
    This function will print the welcome message to the user, that contains all the routes that this api supports.

    Input:
        (none)

    Output:
        (string) it will be the string that will be shown to the user.

    '''
    return f'''

####Asteroid-data-proximity####

Instructions on how to use this application, to store and delete data:

/                GET     Shows all the routes that the user is able to call
/data            POST    Uploads data into database
/data/read       GET     Returns a list of all the items that were put in the database
/data/reset      DELETE  Resets the db that stores the data of the database


'''
    
#This function will print an error message telling the user that db=0 is empty
def db0_is_empty(current_route):
    """
    This function will return a message to the user telling them  that db=0 is empty.

    Input:
        current_route (str) It is the current route that was just curled.

    Output:
        (string): It will be a string that is returned to the user as an error message
    """


    return f"""

[Error]: The database that stores all of the data in the redis container is empty.
Nothing can be returned to the user until the database is filled. In order to populate the database
use the following command:
                curl -X POST localhost:5036/data
With that comamnd completed, you can redo the following command once again:
                {current_route}

"""

#This function will print an error message, telling the user that the list is empty
def list_if_empty(current_route):
    '''
    This function will print to the user that the list is empty.

    Input:
       (current_route) (string): It is the current route that is the user currently curled.

    Output: 
        (string): It will be a string that tells that the list at is empty, to prevent any errors
        from happening when running the api.
    '''
    return f'''

The list that will be returned is vacant, meaning that the current route:
                 {current_route}
Is going to return an empty list, and an error might be raised.

    '''

print(error('curl -X GET localhost:5036'))
print(welcome_message())
print(db0_is_empty('curl -X POST localhost:5036/data'))
