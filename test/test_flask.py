import pytest, requests as rqs
import requests
import json
import os
import time
import re


'''

This script is a unit testing environment where we can test that all the functions are working correctly 

'''

host = 'localhost'
port_num = '5031'
curl = f'http://{host}:{port_num}'

def test_data_download():

    route = f'{curl}/data'
    result_response = requests.post(route)
    assert response.ok == True
    assert response.content == b'''

--- Asteroid Proximity Data Query Program ---

Welcome to the Asteroid Proximity Data Query System! With this application, you can query different datasets about asteroids that are close to Earth. 
-> Below are instructions on how to store and delete data:

COMMAND:         HTTP METHOD:
-------------------------------------------------------------------------------------
/                GET     [This route shows all the available commands you can utilize]
/data            POST    [Uploads the data into local database]
/data/reset      DELETE  [Resets the db variable that stores the data that is currently in the database]
/joblist/delete  DELETE  [Resets the db variable that stores all the jobs that were curled by the user]
/jdb/delete      DELETE  [Resets the db variable that stores all the job keys and job dictionaries]
/answers/delete  DELETE  [Resets the db variable that stores all the return values after the worker has completed the job]

-> Further instructions on how instantiate jobs to the API

COMMAND:               HTTP METHOD:
-------------------------------------------------------------------------------------
/job/data/read           GET     [This route returns a list of dictionaries to that represent all the asteroids in the dataset]
/job/ids                 GET     [This route returns a list that contains all the ids in the dataset]
/job/names               GET     [This route a list that contains all the names of the asteroids in the dataset]
/job/neo                 GET     [This route returns a list or string that contains all the 'neo' in the dataset]
/job/pha                 GET     [This route returns a list of string that contains all the 'pha' in the dataset]
/job/diameters           GET     [This route returns a list of all the diameter measurements in the dataset]
/job/diameters/max       GET     [This route returns a string that tells the user the largest diameter in the dataset]
/job/diameters/min       GET     [This route returns a string that tell the user the smalles diameter in the dataset]
/job/moid_ld             GET     [This route returns a list of all the moid_ld in the dataset]
/job/moid_ld/ascending   GET     [This route returns a list of all the moid_ld from smallest value to largest]
/job/ids/<specific_id>   GET     [This route returns a dictionary pertaining to the id that the user inputs]

-> Further instructions on how to get the API application get the result back to the user

COMMAND:              HTTP METHOD
--------------------------------------------------------------------------------------
/job/result/<jid>        GET     [This route returns the appropate result back to the user when a job id is inputted]


'''




if __name__ == "__main__":
    pytest.main()




