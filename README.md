# Asteroid Proximity Analysis Data Query System (APADQS)
### By Constantinos Skevofilax, Stefanie Catalan, and Abdon Verdejo-Parada
#
This project was developed to provide users with a proper medium to investigate the different positional and identifiction data of asteroids that are Near-Earth Orbit provided by NASA's data concerning local asteroids. 
More specifically, identification of these moving bodies is key for NASA researchers, as they can become a potential hazard to Earth, be used by probes for further investigation, and allows general further understanding of asteroids in space. 
With this program, users can query data that can further advance their research into the field of Near-Earth asteroids in a easy-to-use manner through the APADQS. 


## Getting Started

The inital setup for being able to use the APADQS, you need to setup the repository. Run the following command: 
``` bash
[funky@mnky ~]$ git clone git@github.com:Costaki33/asteroid-data-proximity-analysis.git
``` 
You have now successfully pulled the repository that has the setup for you to run the APADQS! 

Now you need to download the dataset the APADQS uses. See the original source at the provided [link](https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset?resource=download) to fruther explore the full dataset.
As per downloading the dataset, on your local machine, run the following command: 
``` bash
[funky@mnky ~]$ wget https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset?resource=download
```
The dataset will be downloaded and loaded into your now local repository.

### Understanding the Dataset
 
This asteroid dataset describes the following identification information for each asteroid: 

- H: Absolute magnitude parameter
- a: Semi-major axis au Unit
- albedo: Geometric albedo 
- class: Class type of asteroid
- diameter: Object diameter (from equivalent sphere) km Unit
- diameter_sigma: 1-sigma uncertainty in object diameter km Unit
- e: Eccentricity
- epoch: Epoch of osculation in modified Julian day form
- equinox: Equinox of reference frame
- full_name: Full name of the asteroid
- i: Inclination; angle with respect to x-y ecliptic plane
- id: Identification number for asteroid
- moid_id: Earth Minimum Orbit Intersection Distance au Unit
- n: Mean motion (1-sigma uncertainty) Deg/d
- name: Object IAU name
- neo: Near-Earth Object (NEO) flag
- orbit_id: Orbit solution ID
- pdes: Object primary designation
- pha: Potentially Hazardous Asteroid (PHA) flag
- prefix: Comet designated prefix
- q: Perihelion distance au Unit
- sigma_a: Semi-major axis (1-sigma uncertainty) AU
- sigma_e: Eccentricity (1-sigma uncertainty)
- sigma_i: Inclination (1-sigma uncertainty) Deg
- sigma_per: Sidereal orbital period (1-sigma uncertainty) D 
- sigma_q: Perihelion distance (1-sigma uncertainty) AU
- sigma_tp: Time of perihelion passage (1-sigma uncertainty) D
- spkid: Object primary SPK-ID
- tp: Time of perihelion passage TDB Unit

## Deploying to Kubernetes (k8's)

For the program to be able to be access by the outside world, you need to k8's. Using the provided commands, you can set up the environment necessary to interact with the APADQS using HTTP curl methods:
``` bash
[funky@mnky ~]$ kubectl apply -f app-prod-db-pvc.yml
[funky@mnky ~]$ kubectl apply -f app-prod-db-deployment.yml
[funky@mnky ~]$ kubectl apply -f app-prod-db-service.yml
[funky@mnky ~]$ kubectl apply -f app-prod-api-service.yml
```
After setting up the above, use the following command to get the cluster IP address needed to talk between the k8's nodes in case of a pod failing. 
``` bash
[funky@mnky ~]$ kubectl get services
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/abdon01-prod-service         ClusterIP   10.102.115.97    <none>        6379/TCP   27m 
```
Note this IP address, it will be important in the following step.

Run the following command: 
``` bash
[funky@mnky ~]$ kubectl apply -f app-prod-api-deployment.yml
```
Use a text editor like VIM and edit ``app-prod-api-deployment.yml`` so that the cluster IP address you noted above is now put into the following place: 
``spec: containers: env: (your_ip)``

Finally, run the following: 
```bash
[funky@mnky ~]$ kubectl apply -f app-prod-wrk-deployment.yml
```
Now, everything is set up for you to use the APADQS!


## Integration Testing

To check that the APADQS is working properly and returning successful return values, we need to make sure that our API, database, and Worker are all working properly. As such, we utilizd an integration testing method to test the 
functions in our API, database, and Worker are all working properly and outputting successful results. As such, we utilized pytest to test our different functions in our applications to see if our expected successful return value is equal to what is actually returned. 

To make sure everything is working correctly, run the following command: 
``` bash
[funky@mnky ~]$ cd /test
[funky@mnky ~]$ python3 test_flask.py
```
If done correctly, the following will output: 
```bash
============================================================================================================================= test session starts =============================================================================================================================
platform linux -- Python 3.6.8, pytest-7.0.0, pluggy-1.0.0
rootdir: /home/costaki/asteroid-data-proximity-analysis/test
collected 3 items

test_flask.py ...                                                                                                                                                                                                                                                       [100%]

============================================================================================================================== 3 passed in 2.32s ==============================================================================================================================
```
If all 3 tests pass, our system is working properly and now can be utilized to its full potential!


## Interacting with the Program

Now having the APADQS environment properly set up, running, and passed our integration testing measures, you can now use the system!

To get a feel for the APADQS's capabilities and available commands, run the following command ``curl -X GET localhost:5031/``, it will provide instructions on how to use the different HTTP curl routes the APADQS uses: 
```bash
[funky@mnky ~] curl -X GET localhost:5031/

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


```

In order to create new data into the `redis` database that stores your requested value, the command is as follows:

```bash
[funky@mnky ~]curl -X POST localhost:5031/data
```
This will add the dataset to the server, where all of the raw data is stored into database 0. A message will be returned to the user indicating that the data has been adequately stored:

```bash
The data has been successfully been stored in redis, in db=0
```


To read the existing data in the database, perform the command:
```ruby
curl -X GET localhost:5006/job/data/read
```
This returns a list of dictionaries of asteroid information in the dataset for the user to sift through.

If the user wishes to update existing data:
```ruby
curl -X POST localhost:5006/data
```
The `POST` option indicates that the user is requesting to add data in the database. A message indicating the success of the operation will be returned as an output.

In order to delete data from the database, perform:
```ruby
curl -X DELETE localhost:5006/data/reset
```
A message to the user will display that the operation was successful.

job stuff:

Once the database is populated, curl commands can be made so the program can perform the respective, queried routes.

Calling routes for the functions creates a new job for the program:
```ruby
curl -X GET localhost:5006/job/<route>
```
The program will create a `job id` to the corresponding route that was called, which is stored in the `job-ids` in the database.
In order to see the contents of the list that stores this information:
```ruby
curl -X GET localhost:5006/stored/job-ids
```

This will show the route requested and its respective job id. The user can copy the job id and perform the following to recieve the requested output
```ruby
curl -X GET localhost:5006/job/result/<job_id>
```

# Files 


