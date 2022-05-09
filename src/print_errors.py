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
/data/reset      DELETE  Resets the db that stores the data of the database

Instructions on how to get the API to return things back to the user

/data/read       GET     Returns a list of all the items that were put in the database

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


def job_confi(correct_curl, jid):
    '''
    This function will return a string to te user telling them that the job has been added to the
    the queue, and that it will be worked on in the background.

    Input:
        correct_curl (str): That is the curl command inputted by the user
        jid (str): It is the job id that was randomly generated.

    Output:
        (string): IT will return a confirmation message to the user, letting them know that
        the job was been put in the queue.

    '''
    return f'''

The job has been succesfully been added to the queue for the folling curl:
                                {correct_curl}
The job id for the following job is:
                                {jid}
The jid will be very inportant, in order to get the result of your curl commadn dont lose it.
If you seem to forget the job id then to the command below to show all the saved job ids
                                curl -X GET localhost:5036/job/ids

'''


#This function will return a message to the user telling the user that db=4 is empty
def db4_is_empty():
    """
    This function will tell the user that the db=4 is empty, meaning that no job has been
    instantiated

    Input:
        (none)

    Output:
        (string): Telling the user that the db=4 is empty, that a job needs to be instantiated.
    """

    return f"""

The database that contains all the job ids is empty, there must be a job instantiated
in order to user this route. Try this route again when a job has been instantiated.

"""


#This function will tell the user that db=3  is empty
def db3_is_empty():
    """
    This function will tell the user that db=3 is empty

    Input:
       (none)

    Output:
       (string) that tells the user that db=3 is empty.
    """

    return f'''

The database that contains all the results for the job instantiations is empty. Instantiate a job
first in order to get a valid answer. Then try the following command once again.
                      curl -X GET localhost:5036/job/result/<jid>

'''


#This function will tell the user that db=3  is empty
def db3_is_empty2():
    """
    This function will tell the user that db=3 is empty

    Input:
       (none)

    Output:
       (string) that tells the user that db=3 is empty after it  was successfully deleted
    """

    return f'''

The database that contains all the results for the job instantiations is now empty, after everythig was deleted. 
Instantiate a job first in order to get a valid answer. Then try the following command once again.
                      curl -X GET localhost:5036/job/result/<jid>

'''

#This function will tell the user that db=4 is empty, so there is no pending jobs that have been added
def db4_is_empty():
    """
    This function will tell the user that db=4 is empty

    Input:
       (None)

    Output:
        (String) that tells the user that db=4 is empty
    """

    return f'''

The database that contains all the jobs that have been done by the api is empty. If you want to 
instantiate some jobs, then call the different routes so they can be added to this database.

'''

#This function will tell the user that db=2 is empty
def db2_is_empty():
    """
    This function will tell the user that db=2 is now empty

    Input:
       (none)

    Output:
       (string): It will be a string telling the user that db=2 is empty
    """

    return f'''

The database that contained all the job keys and job dictionaries has be emptied out. If you want to 
instantiate some jobs. then call different routes so they can be added to this database.

'''

def return_not_finished(jid):
    """
    This function will tell the user that the return value has not been complete yet.

    Input:
        jid (string): It is the jid that was created

    Output:
       (string): It will return a string to the user telling them that they need to wait.
    """
    return f'''
    
The return value for the curl below has not been complete.
                   curl -X localhost:5036/job/result/{jid}
Give the program a few seconds then retry the command from above once again.

'''
