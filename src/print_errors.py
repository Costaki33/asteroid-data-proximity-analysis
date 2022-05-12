'''

    This file will contian all the error messages and other items that will be printed to the user

'''

# This function will print the correct curling command to the user
def error(correct_curl):

    '''
    
    This function will return the correct curling command for each curl command that was incorrectly inputted by
    the user.

    Input:
        correct_curl (string): This string is the correct command for that specific route the user is calling

    Output:
        Error message (string): This output string message will be the correct command for the user to use

    '''

    return f'\n\n[ERROR]: Invalid curl command for this route. Here is the correct command for this route:\n{correct_curl}\nRetype your command above to get the results you seek.\n\n'


# This function prints the welcome message to the user
def welcome_message():
    
    '''
    
    This function will print a welcome message to the user, which contains all the routes that this API program supports

    Input:
        (none)

    Output:
        Welcome mesage (string): This output string message will be a string that will be shown to the user with instructions 

    '''

    return f'''

--- Asteroid Proximity Data Query Program ---

Welcome to the Asteroid Proximity Data Query System! With this application, you can query different datasets about asteroids that are close to Earth. 
-> Below are instructions on how to store and delete data:

COMMAND:         HTTP METHOD:
-------------------------------------------------------------------------------------
/                GET     [This route shows all the available commands you can utilize]
/data            POST    [Uploads the data into local database]
/data/reset      DELETE  [Resets the db container that stores the data that is currently in the database]

-> Further instructions on how to get the API application to return data back to you, the user:


COMMAND:         HTTP METHOD:
-------------------------------------------------------------------------------------
/data/read       GET     [This route returns a list of all the items that were put into the local database]


'''
    

# This function prints out an error message, notifying the user that db = 0 is empty
def db0_is_empty(current_route):
    
    '''
    
    This function return an error message to the user, notifying them that db = 0 is empty

    Input:
        current_route (str): This string is the current route that was just curled by the user

    Output:
        Error message (string): This output error message is a string that is returned to the user

    '''


    return f'''

[ERROR]: The database that stores all of the data in the Redis container is empty.
Because of this, nothing can be returned to the user until the database has been filled. In order to populate the database,
use the following command:
                curl -X POST localhost:5031/data
Following that completed & successful command, you can redo the following command:
                {current_route}

'''


# This function prints an error message, notifying the user that the list is empty
def list_if_empty(current_route):
    
    '''
    
    This function will print to the user that the list is empty.

    Input:
       (current_route) (string): The current route that is the user currently curling

    Output:
        Error message (string): A string that tells the user that the pulled list is empty, with the intention of preventing any errors
        from occuring when running the API 
    
    '''
    return f'''

[ERROR]: The requested list that will be returned is vacant, meaning that the current route:
                 {current_route}
Will return an empty list, leading to a possible error being raised.

'''

# This function returns a informational message that the user their requested service has been added to the job queue and is working the background
def job_confi(correct_curl, jid):
    
    '''
    
    This function returns a string notifying the user that their job request has been added to the
    the Job queue, and it is being worked on in the background

    Input:
        correct_curl (str): This string is the curl command inputted by the user
        jid (str): It is the job id that was randomly generated for the user to call their specific job request

    Output:
        Informational mesage(string): A string message confirming that their job was been added to the queue

    '''
    return f'''

[INFO]: The requested job has been succesfully been added to the job queue for the follwing curl command:

                                {correct_curl}

The job id (jid) for the following job is:

                                {jid}

NOTE: The jid is very important. In order to view the results of your curl command, dont lose it.

If you forget the jid, use the following command below to show all the saved job ids:

                                curl -X GET localhost:5031/stored/job-ids

'''


# This function returns a message to the user, notifying them that db = 4 is empty
def db4_is_empty():

    '''
    
    This function notifys the user that db = 4 is empty, meaning that no job has been
    instantiated

    Input:
        (none)

    Output:
        Error message (string): Tells the user that the db = 4 is empty. The job needs to be instantiated
    
    '''

    return f'''

[ERROR]: The database that contains all the job ids is empty. There must be a job instantiated
in order to use this route. Try using this route again when a job has been instantiated.
Run the following command to instantiate your job:

                      curl -X GET localhost:5031/job/result/<jid>


'''


# This function returns a message to the user, notifying the user that db = 3 is empty
def db3_is_empty():
    
    '''
    
    This function notifys the user that db = 3 is empty, meaning that no job has been
    instantiated

    Input:
       (none)

    Output:
       ERROR message (string): Tells the user that db = 3 is empty. The job needs to be insatantiated
    
    '''

    return f'''

[ERROR]: The database that contains all the job ids is empty. There must be a job instantiated
in order to use this route and have a return value. Try using this route again when a job has been instantiated.
Run the following command to instantiate your job:

                      curl -X GET localhost:5031/job/result/<jid>

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
