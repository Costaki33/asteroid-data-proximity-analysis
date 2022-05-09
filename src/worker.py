import jobs 
import time
import json
from flask import Flask, request, jsonify

#These are all the functions that will do various jobs

#This function will return a list of dictionaries to the user for every asteroid entry
def read_data(jid):
    list_of_data = []
    for item in jobs.rd.keys():
        #json.loads turns a json string to a dictionary
        list_of_data.append(json.loads(jobs.rd.get(item)))

    #Add this item into the answers db=3. the key value will be jid and the value will be the return
    jobs.answers.set(jid, json.dumps(list_of_data))
    



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
        
    #There will be a 15 second buffer for the program to the job, during this time worker will the work
    time.sleep(15)

    #This will say that the job has been complete
    jobs.update_job_status(jid, 'complete')

execute_job()
