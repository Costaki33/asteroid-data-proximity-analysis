import json
import csv
import redis
from typing import List
from flask import Flask, request, jsonify
import jobs
import print_errors
import logging

logging.basicConfig(level=logging.DEBUG)

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
@app.route("/job/data/read", methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
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
        job_dict = jobs.add_job('/job/data/read', 'list of dicts')
        jid = job_dict['id']

        #we are going to add the job_id into a new redis database, and the route as the key value
        jobs.job_list.set('/job/data/read', jid)

        #Returns a message to the user explaning the next steps that need to be done
        return print_errors.job_confi('curl -X GET localhost:5036/job/data/read', jid)

    else:
        return print_errors.error('curl -X GET localhost:5036/data/read')


#This function will return a list of all the job id
@app.route("/stored/job-ids", methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def return_all_ids():
    """
    This function will return a list of all the keys and values that are in the redis
    database, db=4

    Input:
        (none)

    Output:
        (list) return a list of all the key and values that have been stored in db=4
    """
    #Checking that db=4 is not empty
    if(len(jobs.job_list.keys()) == 0):
        return print_errors.db4_is_empty()

    if(request.method == 'GET'):
        list_of_id = []
        for item in jobs.job_list.keys():
            mini_list = []
            mini_list.append(item)
            mini_list.append(jobs.job_list.get(item))
            list_of_id.append(mini_list)

        return jsonify(list_of_id)

    else:
        return print_errors.error('curl -X GET localhost:5036/stored/job-ids')

#This route will return what is stored in the the answer database or it will return a print statemet
@app.route("/job/result/<jid>", methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def get_results(jid):
    """
    This function is going to return the result of the job id that was created

    Input:
        jid (str): It is the job id that created when the user instantiated the job

    Output:
       It will return the result back to the user.
    """
    #Checking if db=3 is empty
    if(len(jobs.answers.keys()) == 0):
        return print_errors.db3_is_empty()

    #Getting the result back to the user
    if(request.method == 'GET'):
        job_dictionary = jobs.get_job_by_id(jid)
        logging.warning('The item of job_dictionary is: ', print(job_dictionary['return_type']))
        
        #This will check if the return value has been completed
        if(job_dictionary['status'] != 'complete'):
            return print_errors.return_not_finished(jid)

        #Incase the return type is list of dicts
        if(job_dictionary['return_type'] == 'list of dicts'):
            logging.warning('It is inside the list of dicts')
            list_of_dict = json.loads(jobs.answers.get(jid))
            json.dumps(list_of_dict, sort_keys=False, indent=2)
            #        logging.warning('the type of list_of_dict is:', type(list_of_dict))
            return jsonify(list_of_dict)

        #Incase the return type is a list
        elif(job_dictionary['return_type'] == 'list'):
            logging.warning('It is inside the list if statement')
            normal = json.loads(jobs.answers.get(jid))
            json.dumps(normal, sort_keys=False, indent=2)
            return jsonify(normal)

        #Incase the return type is a string
        elif(job_dictionary['return_type'] == 'string'):
            logging.warning('It is inside the string if statement')
            
            #Returns the string message to the user
            return jobs.answers.get(jid)
            
        #Incase the return type is a dictionary
        elif(job_dictionary['return_type'] == 'graph'):
            pass

        #This would happen if the return_type was different from anything else
        else:
            return f'''

The route that was curled below.

'''

        logging.warning('It did not go into any of the if statements')
        #Incase the return type is a graph
        #elif(job_dictionary['return_type'] == 'graph'):
         #   pass
            
    else:
        return print_errors.error('curl -X GET localhost:5036/job/id')


#This route will get rid of all the items in the job_list db=4
@app.route('/joblist/delete', methods =['DELETE', 'GET', 'PUT', 'PATCH', 'POST'])
def delete_all_ids():
    """
    This function will delete all the pending job in the job list

    Input:
       (None)

    Output:
       (string): It will tell the user of that the db=4 is empty

    """

    if(request.method == 'DELETE'):
        jobs.job_list.flushdb()
        return print_errors.db4_is_empty()
    else:
        return print_errors.error('curl -X DELETE localhost:5036/joblist/delete')


#This route will get rid of all the items in the jdb db=2
@app.route('/jdb/delete', methods = ['GET', 'DELETE', 'PUT', 'PATCH', 'POST'])
def delete_all_jdb():
    """
    This function will delete all the jdb in the db=2

    Input:
       (none)

    Output:
       (string): IT will tell the iser of that db=2 is empty
    """
    if(request.method == "DELETE"):
        jobs.jdb.flushdb()
        return print_errors.db2_is_empty()
    
    else:
        return print_errors.error('curl -X DELETE localhost:5036/jdb/delete')

#This function will get rid of all the items in the redis database for db=3
@app.route("/answers/delete", methods = ['DELETE', 'GET', 'PUT', 'PATCH', 'POST'])
def delete_all_answers():
    """
    This function will delete all the answers in the answers database, db=3

    Input:
        (None)

    Output:
        (string): It iwll tell the user that all the saved answers have been deleted
    """

    if(request.method == 'DELETE'):
        jobs.answers.flushdb()
        return print_errors.db3_is_empty2()
    else:
        return print_errors.error('curl -X DELETE localhost:5036/answers/delete')


# this route returns a list of all asteroid ids
@app.route("/job/ids", methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
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
        return print_errors.db0_is_empty('curl -x GET localhost:5036/job/ids')

    # making sure that user is calling GET
    if(request.method == 'GET'):
        
       job_dict = jobs.add_job('/job/ids', 'list')
       jid = job_dict['id']

       #we are going to add the job_id into a new redis databse, and the route as the key value
       jobs.job_list.set('/job/ids', jid)

       #returns a message to the user explaning the next steps that need to be done
       return print_errors.job_confi('curl -X GET localhost:5036/job/ids', jid)
    else:
        return print_errors.error('curl -X GET localhost:5006/id')



# this route returns a list of all asteroid names
@app.route("/job/names", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_names():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/job/names')

    # making sure that user is calling GET
    if(request.method == 'GET'):
        #adds it to the queue, jdb
        job_dict = jobs.add_job('/job/names', 'list')
        jid = job_dict['id']

        #adds it to the job list
        jobs.job_list.set('/job/names', jid)

        #This prints a confirmation string to the user
        return print_errors.job_confi('curl -X GET localhost:5036/job/names', jid)
    else:
        return print_errors.error('curl -X GET localhost:5006/name')


# this route returns a list of names of near earth orbit asteroids
@app.route("/job/neo", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_neos():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/neo')

    # making sure that user is calling GET
    if(request.method == 'GET'):
        #Adds it to the queue, jdb, it will determine at the very end it will return a list or a string
        job_dict = jobs.add_job('/job/neo', 'list')
        jid = job_dict['id']

        #adds it to the job list
        jobs.job_list.set('/job/neo', jid)

        #This prints a confirmation string to the user
        return print_errors.job_confi('curl -X GET localhost:5036/job/neo', jid)

        '''
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
        '''

    else:
        return print_errors.error('curl -X GET localhost:5006/neo')


'''
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
'''

# this route returns a list of all asteroid diameterss
@app.route("/job/diameters", methods = ['GET', 'POST', 'DELETE', 'PATCH'])
def list_diameters():
    """
    This function is just going to get the job_id in order for the worker to do the work

    Input:
        (none)

    Output:
        (none)
    """

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/job/diameters')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        job_dict = jobs.add_job('/job/diameters', 'list')
        jid = job_dict['id']

        #We are going to add the job_id into a new redis database, and the route as the key value
        jobs.job_list.set('/job/diameters', jid)

        #Returns a confirmation string back to the user
        return print_errors.job_confi('curl -X GET localhost:5036/jod/diameters', jid)

    else:
        return print_errors.error('curl -X GET localhost:5006/diameter')

'''
# this route returns the name and value of the asteroid with the largest diameter
@app.route("/diameter/max", methods =['GET', 'PUT', 'POST', 'DELETE'])
def diameter_largest():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/diameter')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        # diameter list
        diameter_list = []

        # going through entire dataset
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            # adding diameters to diameter_list
            diameter_list.append(float(currentdict['diameter']))

        # using max() to get the largest diameter value
        return('\n\n' + 'The largest asteroid diameter is ' +  str(max(diameter_list)) + '\n\n')

# this route returns the name and value of the asteroid with the smallest diameter
@app.route("/diameter/min", methods =['GET', 'PUT', 'POST', 'DELETE'])
def diameter_largest():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/diameter/min')

    # making sure that user is calling GET
    if(request.method == 'GET'):

        # diameter list
        diameter_list = []

        # going through entire dataset
        for item in jobs.rd.keys():
            currentdict = json.loads(jobs.rd.get(item))

            # adding diameters to diameter_list
            diameter_list.append(float(currentdict['diameter']))

        # using max() to get the smallest diameter value
        return('\n\n' + 'The smallest asteroid diameter is ' +  str(min(diameter_list)) + '\n\n')
'''
# this route returns a list of all asteroid moid_lds
@app.route("/job/moid_ld", methods =['GET', 'PUT', 'POST', 'DELETE'])
def list_moid_lds():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/job/moid_ld')

    # making sure that user is calling GET
    if(request.method == 'GET'):
        job_dict = jobs.add_job('/job/moid_ld', 'list')
        jid = job_dict['id']

        jobs.job_list.set('/job/moid_ld', jid)

        return print_errors.job_config('curl -X GET localhost:5036/job/moid_ld', jid)
    else:
        return print_errors.error('curl -X GET localhost:5036/job/moid_ld')
'''
# this route returns the list of moid_lds in ascending order (least to greatest)
@app.route("/job/moid_ld/ascending", methods =['GET', 'PUT', 'POST', 'DELETE'])
def ascending_moid_lds():

    # checking that db 0 is populated
    if(len(jobs.rd.keys()) == 0):
        return print_errors.db0_is_empty('curl -x GET localhost:5036/job/moid_ld/ascending')

    # making sure that user is calling GET
    if(request.method == 'GET'):
        job_dict = jobs.add_job('/job/moid_ld/ascending', 'list')
        jid = job_dict['id']

        jobs.job_list.set('/job/moid_ld/ascending', jid)

        return print_errors.job_config('curl -X GET localhost:5036/job/moid_ld/ascending', jid)
    else:
        return print_errors.error('curl -X GET localhost:5036/job/moid_ld/ascending')
'''
#Deletes all of the data in db=0 
@app.route("/data/reset", methods =['GET', 'PUT', 'POST', 'DELETE'])
def rest_db_data() -> str:
    """
    This function will delete all the data in the redis database (db=0).

    Input:
        (None)

    Output:
        (String) it will return a message to the user that the data inside the 
        redis db has been deleted
    """
    if(request.method=="DELETE"):
        jobs.rd.flushdb()
        return '\n\nThe redis container for db=0, is empty, all the data that was inside has been deleted.\n\n'
    else:
        return print_errors.error('curl -X DELETE localhost:5036/data/reset')

#Returns the data to the user, we start using the worker.py function through the usage of jobs.py 

    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
