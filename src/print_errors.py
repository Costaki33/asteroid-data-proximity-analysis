#
#
#This file will contian all the error messages and other items that will be printed to the user
#
#

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
/data/reset      DELETE  Resets the db that stores the data of the database

'''
    


print(error('curl -X GET localhost:5036'))
print(welcome_message())
