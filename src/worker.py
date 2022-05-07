from jobs 
import time

@q.worker
def execute_job(jid):
    '''
    This function will be in charge of 

    '''
    #Starting to execute the job
    update_job_status(jid, 'in progress')

    #here is where you call the correct functions that will be used to complete the work

    #There will be a 15 second buffer for the program to the job, during this time worker will the work
    time.sleep(15)
    #This will say that the job has been complete
    update_job_status(jid, 'complete')

execute_job()
