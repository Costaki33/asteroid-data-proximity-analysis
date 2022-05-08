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
                if(count == 300):
                    break

            #Populating the redis db=0
            for item in data['asteroid_data']:
                jobs.rd.set(item['id'], json.dumps(item))

        return '\n\nThe data has been successfully been stored in redis, in db=0\n\n'
    else:
        return print_errors.error('curl -X POST localhost:5036/data')


#This route will return a list of all the items in redis db=0
@app.route("/data/read", methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def read_data():
    '''
    This function will return a list of all the dictonaries that were added to the redis db=0

    Input:
        (None)

    Output:
        (list of dicts) that contain all the information that was added to redis
    '''
    #We need to check that the db=0 is infact been populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/data/read')

    #Checking that the verb is a GET
    if(request.method == 'GET'):
        list_of_data = []
        
        for item in jobs.rd.keys():
            list_of_data.append(json.loads(jobs.rd.get(item)))

        #Return a list that will be accepted by flask
        return jsonify(list_of_data)
    else:
        return print_errors.error('curl -X GET localhost:5036/data/read')

# this route returns a list of all asteroid ids
@app.route("/id", methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def list_ids():
    """
    This function will return a list that contains all the id's in the database.

    Input:
        (None)

    Output: 
        (list) that contains all the ids of the asteroid.
    """
    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/id')

    # making sure that user is calling GET
    if(request.method == 'GET'):
        
        # empty list
        id_list = []

        # going through entire dataset to find ids
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            #adding 'id' into the list
            id_list.append(currentdict['id'])
        
        #Checking if the returning list infact does have items inside it, else it will return the list
        if(len(id_list) == 0):
            return print_errors.list_if_empty('curl -X GET localhost:5036/id')
        else:
            return jsonify(id_list)

    else:
        return print_errors.error('curl -X GET localhost:5006/id')

# this route returns a list of all asteroid names
@app.route("/name", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_names():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/name')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        # empty list
        name_list = []

        # going through entire dataset
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            # adding 'name' into the list
            name_list.append(currentdict['name'])

        # checking if list actually has items in it
        if(len(name_list) == 0):
            return print_errors.list_if_empty('curl -X GET localhost:5036/name')
        else:
            return jsonify(name_list)

    else:
        return print_errors.error('curl -X GET localhost:5006/name')

# this route returns a list of names of near earth orbit asteroids
@app.route("/neo", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_neos():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/neo')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        # empty list
        neo_list = []

        # going through entire dataset
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            # chacking if the 'neo' value is a Y
            if currentdict['neo'] is 'Y':

                # append the name of the asteroid that is neo
                neo_list.append(currentdict['name'])

        # checking if list is populated
        if(len(neo_list) == 0):
            return '\n\nThere are no asteroids near Earth orbit. Yay!\n\n'
        else:
            return jsonify(neo_list)

    else:
        return print_errors.error('curl -X GET localhost:5006/neo')

# this route returns a list of names of potentially hazardous asteroids
@app.route("/pha", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_phas():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/pha')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        # empty list
        pha_list = []

        # going through entire dataset
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            # checking if the 'pha' value is a Y
            if currentdict['pha'] is 'Y':

                # append the name of the asteroid that is pha
                pha_list.append(currentdict['name'])

        # checking if list is populated
        if(len(pha_list) == 0):
            return '\n\nThere are no potentially hazardous asteroids. Yay!\n\n'
        else:
            return jsonify(pha_list)

    else:
        return print_errors.error('curl -X GET localhost:5006/pha')

# this route returns a list of all asteroid diameterss
@app.route("/diameter", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_diameters():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/diameter')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        # empty list
        diameter_list = []

        # going through entire dataset
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            # adding 'diameter' into the list
            diameter_list.append(currentdict['diameter'])

        # checking if list actually has items in it
        if(len(diameter_list) == 0):
            return print_errors.list_if_empty('curl -X GET localhost:5036/diameter')
        else:
            return jsonify(diameter_list)

    else:
        return print_errors.error('curl -X GET localhost:5006/diameter')



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
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
