import json
import os
import uuid
from flask import Flask, request
import redis
from hotqueue import HotQueue

#Gathering the redis_ip for the container
redis_ip = os.environ.get('REDIS_IP')

#Global variable that will store all of the data in redis in db=0
rd = redis.Redis(host=redis_ip, port='6379', db=0)

#Global variable for the queue data strucutre that will store the command from the flask
q = HotQueue('queue', host=redis_ip, port='6379', db=1)

#Global variable that will store all the id values generated when a command is curled
jdb = redis.Redis(host=redis_ip, port='6379', db=2, decode_responses=True)

#This function will generate a random jid that will be generated when a job was requested on the flask
def _generate_jid() -> str:
    """
    This function will generate a random identifier for each job that is curled.

    Input:
        (None)

    Output: 
       (string) it will the randomly generated id
    """
    return str(uuid.uuid4())

#This function will genrate a key value for the inputted jid 
def _generate_job_key(jid) -> str:
    """
    This function will generate a key value when the inputting an id number

    Input:
        (jid) (string) it is the randomly generates id for a specific job

    Output:
        (string) it is string that will the key value of the id. An example of what it retruns would
                 like 'jobs.jasdhf9ef9230300'
    """
    return 'job.{}'.format(jid)


def _instantiate_job(jid, status, start, end):
    """
    This function will create a dictionary entry for each job. A job dictionary will have the following 
    key value pairs. 1.- id: jid (str), 2.- status: status (str), 3.- start: start (str),
    4.- end: end (str).

    Inputs: 
         jid (str): It is the job Id that was created 
         status (str): It will have the following status (in progress or complete)
         start (str): It eill

    """
