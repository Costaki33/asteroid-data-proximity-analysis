import jobs 
import time
import json
from flask import Flask, request, jsonify
import logging
import matplotlib.pyplot as plt

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
        #Gets rid of all names that have nothing inside
        if(currentdict['diameter'] == ''):
            continue
        

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


#Function that will return a list of names of earth orbit asteroids
def list_neos(jid):
    """
    This function returns a list of names of asteroids that are near the earth

    Input:
        jid (str) it is the job id for that specific job

    Output:
        nothing, it will store the answer in a redis variable
    """
    #empty list
    neo_list = []

    #going through entire dataset
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))

        #checking if the 'neo' value is a Y
        if currentdict['neo'] == 'Y':
            #Gets rid of all names that have nothing inside
            if(currentdict['name'] == ''):
                continue
            
            neo_list.append(currentdict['name'])


    #Checking if the list is empty, if it is empty then it is better to not store that in redis
    #We are going to store a string value instead that will be displayed to the user
    if len(neo_list) == 0:
        return_string = '\n\nThere are no asteroids near Earth orbit. Yay!\n\n'
        jobs.update_return_value(jid, 'string')
        jobs.answers.set(jid, return_string)
    
    #This will be storing the list in the redis varaible
    else:
        jobs.answers.set(jid, json.dumps(neo_list))


#This function will return a list of names of potentially hazardous asteroids
def list_phas(jid):
    """
    This function will return a list of names of potentially hazardous asteroids

    Input:
        jid (str): It is the job id that was created

    Output:
        None: It will return nothing, it will just store the answer in a redis variable
    """

    #empty list
    pha_list = []

    #going through entire dataset
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))

        #checking if the 'pha' value is 'Y'
        if currentdict['pha'] == 'Y':
            #Gets rid of all names that have nothing inside
            if(currentdict['name'] == ''):
                continue
            #append the name if hte asteroid that is pha
            pha_list.append(currentdict['name'])

        #checking if the list is empty, if it is then a string message will be stored instead of an empty list
        if len(pha_list) == 0:
            return_string = '\n\nThere are no potentially hazardous asteroids. Yay!\n\n'
            jobs.update_return_value(jid, 'string')
            jobs.answers.set(jid, return_string)

        #This will be storing the listin the redis variable
        else:
            jobs.answers.set(jid, json.dumps(pha_list))


#This function will return the largest diameter in the dataset
def diameter_largest(jid):
    """
    This function will print the largest diameter of asteroid for the user

    Input:
        jid (str): It is the job id that was created

    Output:
       (none): It will output nothing
    """
    
    #diameter list
    diameter_list =[]

    #going through entire dataset
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))
        
        #Incase it is empty
        if(currentdict['diameter'] == ''):
            continue
        
        #adding diameters to diameter_list
        diameter_list.append(float(currentdict['diameter']))

    return_str = '\n\n' + 'The largest asteroid diameter is: ' + str(max(diameter_list)) + '\n\n'
    jobs.answers.set(jid, return_str)

#This function will return the smallest diameter of the asteroid
def diameter_smallest(jid):
    """
    This function will return a string to hte user telling the user the smallest diamter for asteroid

    Input:
       (jid) (string) it is the job id that was created 

    Output:
        (none): Nothing will be outputted 
    """
    #diameter list
    diameter_list = []

    #going through the entire dataset
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))
        
        #Incase it is empty
        if(currentdict['diameter'] == ''):
            continue

        #adding diameters to diamter_list
        diameter_list.append(float(currentdict['diameter']))
    
    return_str = '\n\n' + 'The smallest asteroid diameter is: ' + str(min(diameter_list)) + "\n\n"
    jobs.answers.set(jid, return_str)


#This function will return a list of the moid_lds is ascending order
def ascending_moid_lds(jid):
    """
    This function will return a list of a moid_lds that is in ascending order

    Input:
       (jid) (string): It is the job id that was created

    Output:
        None: nothing will be returned, the answer will be stored in a redis variable
    """

    #empty_list
    empty= []

    #going through the entire dataset
    for item in jobs.rd.keys():
        #Turns the dictionaries form strings to actual python dictionary objects
        currentdict = json.loads(jobs.rd.get(item))
    
        #Incase it is empty
        if(currentdict['diameter'] == ''):
            continue

        #adding moid_lds into the empty_list, and turning the value from string to floats
        empty.append(float(currentdict['moid_ld']))

    #We need to sort them from least to greatest
    sortedlist = sorted(empty)
    
    #We need to return each element in the list back to strings, made empty empty again
    empty = []

    #Turning every item back to string
    for item in sortedlist:
        empty.append(str(item))

    #store that list in a redis variable
    jobs.answers.set(jid, json.dumps(empty))

# this function will return a histogram of all moid_lds
def moid_graph(jid):

    # moid list
    moid_list = []

    #going through the entire dataset
    for item in jobs.rd.keys():
        #Turns the dictionaries form strings to actual python dictionary objects
        currentdict = json.loads(jobs.rd.get(item))

        #Incase it is empty
        if(currentdict['diameter'] == ''):
            continue

        #adding moid_lds into the empty_list, and turning the value from string to floats
        empty.append(float(currentdict['moid_ld']))

    # creating histogram from moid_list
    plt.hist(moid_list, bins = 10)
    plt.savefig('/moid_graph.png')

    with open('/moid_graph.png', 'rb') as f:
        img = f.read()

    jobs.answers.hset(jid, 'image', img)
    jobs.hset(jid, )
    jobs.answers.set(jid, img)

#This function will do the work for gathering the correct dictionary information
def specific_id_info(jid, query_string):
    """
    This function is going to return the correct dictionary to the user when the id was insputted

    Input:
        (jid) (string): It is a string that represents the job id 
        (query_string) (string): It is a string of all the parameters that was passed in by the user

    Ouput:
        (none): It outputs nothing it just stores the answer in a redis variable
    """
    split_query_parameters = query_string

    #These are all dictionary values, item is a dictionary
    for item in jobs.rd.keys():
        currentdict = json.loads(jobs.rd.get(item))
        
        if(currentdict['id'] == split_query_parameters):
            jobs.answers.set(jid, json.dumps(currentdict))
            break    

@jobs.q.worker
def execute_job(jid):
    '''
    This function will be in charge of doing all the work

    '''
    logging.warning('You are here in the execute_job')

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
    elif(route == '/job/neo'):
        list_neos(jid)
    elif(route == '/job/pha'):
        list_phas(jid)
    elif(route == '/job/diameters/max'):
        diameter_largest(jid)
    elif(route == '/job/diameters/min'):
        diameter_smallest(jid)
    elif(route == '/job/moid_ld/ascending'):
        ascending_moid_lds(jid)
    elif(route == '/job/moid_ld/graph'):
        moid_graph(jid)
    elif(route == '/job/ids/<specific_id>'):
        #query should be a string
        query = job_dictionary['query']
        specific_id_info(jid, query)

    #There will be a 15 second buffer for the program to the job, during this time worker will the work
    time.sleep(15)

    #This will say that the job has been complete
    jobs.update_job_status(jid, 'complete')

execute_job()
