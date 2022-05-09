import jobs 
import time
import json
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)
#These are all the functions that will do various jobs

#This function will return a list of dictionaries to the user for every asteroid entry
def read_data(jid):
    '''
    This function will return a list of dictionaries to the user for every asteroid entry 

    Input:
       jid (string) It is the job id that was created randomly.

    Output:
       (none)
    '''
    list_of_data = []
    for item in jobs.rd.keys():
        #json.loads turns a json string to a dictionary
        list_of_data.append(json.loads(jobs.rd.get(item)))

    #Add this item into the answers db=3. the key value will be jid and the value will be the return
    jobs.answers.set(jid, json.dumps(list_of_data))
    

#This function will return a list that contains all of the ids from the dataset
def list_ids(jid):
    """
    This function will return a list that contains all the id's in the database.

    Input:
       jid (str): It is the job id

    Output:
       (None)
    """
    id_list = ["blah"]
    
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))
        
        # Adding 'id' into the list
        id_list.append(currentdict['id'])
        
    #adding the return to the answers db
    jobs.answers.set(jid, json.dumps(id_list))


#This function will return a list of all the names that are in the dataset
def list_names(jid):
    """
    This function will return a list of all the names in the dataset

    Input:
        jid (string): It is the job id that was created

    Output:
        (none)
    """
    name_list = []

    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))

        #adding 'name' into the list
        name_list.append(currentdict['name'])

    #adding the return to the answers db
    jobs.answers.set(jid, json.dumps(name_list))


#This function will store list of all the diameter for the asteroids
def list_diameters(jid):
    """
    This function will store a list of all the diamters in the dataset

    Input:
       jid (str) it is the job id

    Output:
       None
    """
    
    diameter_list = []
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))
        
        #adding 'diameter' into the list
        diameter_list.append(currentdict['diameter'])

    #adding the return to the answers db
    jobs.answers.set(jid, json.dumps(diameter_list))


#This function will do the work
def list_moid_lds(jid):
    """
    This function will do the work

    Input:
       jid (str): It is the job id

    Output:
       (none)
    """

    moid_ld_l = []

    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))
        
        #adding 'moid_ld' into the list
        moid_ld_l.append(currentdict['moid_ld'])

    #adding the return to the answers db
    jobs.answers.set(jid, json.dumps(moid_ld_l))

@jobs.q.worker
def execute_job(jid):
    '''
    This function will be in charge of doing all the work

    '''
    #Starting to execute the job
    jobs.update_job_status(jid, 'in progress')

    #here is where you call the correct functions that will be used to complete the work
    #We are going to need the route that the user implemented, from the job dictionary
    job_dictionary = jobs.get_job_by_id(jid)

    route = job_dictionary['route']

    #depending on the route, it will call different functions that will return different results
    if(route == '/job/data/read'):
        read_data(jid)
    elif(route == '/job/ids'):
        list_ids(jid)
    elif(route == '/job/names'):
        list_names(jid)
    elif(route == '/job/diameters'):
        list_diameters(jid)
    elif(route == '/job/moid_ld'):
        list_moid_lds(jid)

    #There will be a 15 second buffer for the program to the job, during this time worker will the work
    time.sleep(15)

    #This will say that the job has been complete
    jobs.update_job_status(jid, 'complete')

execute_job()
