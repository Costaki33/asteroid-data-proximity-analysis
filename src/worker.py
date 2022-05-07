from jobs import q, update_job_status
import time

@q.worker
def execute_job(jid):
    '''
    This function will be in charge of 

    '''
    #Starting to execute the job
    update_job_status(jid, 'in progress')
    #There will be a 15 second buffer for the program to the job
    time.sleep(15)
    #This will say that the job has been complete
    update_job_status(jid, 'complete')

execute_job()
