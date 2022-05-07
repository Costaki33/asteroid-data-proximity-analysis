import json
import csv
import redis
from typing import List
from flask import Flask, request, jsonify
import jobs
import print_errors
import logging

#Creating app, an instance of the flask variable
app = Flask(__name__)

#This is the route that will show the user all the possible routes that they can choose from
@app.route("/", methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def info() -> str:
    """
    This function will show to the user all the possible routes that they can choose from

    Args: 
        None

    Output:
        (string)
    """
    if(request.method == 'GET'):
        return print_errors.welcome_message()

    else:
        return print_errors.error('curl -X GET localhost:5036/')


#This route is to load the data into redis, db=0
@app.route('/data', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def load_asteroid_data_into_redis() -> str:
    '''
    This function will put the dataset.csv into the redis server. All of the 
    raw data will be saved on db = 0

    Args:
        None

    Returns:
        (string) it will return a message to the user telling them that the data 
        has been stored or the incorrect method was used and an error message will
        be shown to the user
    '''
    #This if for storing the data into the redis database in db=0
    if(request.method == 'POST'):
        #Deletes all the items inside db=0
        jobs.rd.flushdb()

        #This will populate the redis db=0
        data = {}
        count = 0
        data['asteroid_data'] = []
        with open("dataset.csv", 'r') as f:
            dataset = csv.DictReader(f)
            for row in dataset:
                data['asteroid_data'].append(dict(row))
                count = count + 1
                if(count == 3000):
                    break

            #Populating the redis db=0
            for item in data['asteroid_data']:
                jobs.rd.set(item['id'], json.dumps(item))

        return '\n\nThe data has been successfully been stored in redis, in db=0\n\n'
    else:
        return print_errors.error('curl -X POST localhost:5036/data')

#Deletes all of the data in db=0 
@app.route("/data/reset", methods =['GET', 'PUT', 'POST', 'DELETE'])
def rest_db_data() -> str:
    '''
    This function will delete all the data in the redis database (db=0).

    Input:
        (None)

    Output:
        (String) it will return a message to the user that the data inside the 
        redis db has been deleted
    '''
    if(request.method=="DELETE"):
        jobs.rd.flushdb()
        return '\n\nThe redis container for db=0, is empty, all the data that was inside has been deleted.\n\n'
    else:
        return print_errors.error('curl -X DELETE localhost:5036/data/reset')

#Returns the data to the user, we start using the worker.py function through the usage of jobs.py 
#@app.route("/data/read", methods = ['GET', 'POST', 'DELETE', 'PUT'])
#def read_dataset() -> List:    
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
