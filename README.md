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

### Help Message
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

**Note:**
When you have selected a command you would like to run, you be provided with a Job ID (jid). You need this jid to result list you want to observe 

```bash


[INFO]: The requested job has been succesfully been added to the job queue for the follwing curl command:

                                curl -X GET localhost:5031/job/data/read

The job id (jid) for the following job is:

                                9ab5da39-b95e-41ba-bb79-df027f01b44a

NOTE: The jid is very important. In order to view the results of your curl command, dont lose it.

If you forget the jid, use the following command below to show all the saved job ids:

                                curl -X GET localhost:5031/stored/job-ids
[funky@mnky ~] curl -X GET localhost:5031/job/result/9ab5da39-b95e-41ba-bb79-df027f01b44a
```
You must do this for every job you query. There is a list of stored job-ids you can reference if you query multiple jobs. 

### Creating new data 
In order to create new data into the ``redis`` database that stores your requested value, the command is as follows:

```bash
[funky@mnky ~]curl -X POST localhost:5031/data
```
This will add the dataset to the server, where all of the raw data is stored into database 0. A message will be returned to the user indicating that the data has been adequately stored:

```bash
The data has been successfully been stored in redis, in db=0
```

### Reading the existing data in the database 
To read the existing data in the database, perform the command:
```bash
[funky@mnky ~]curl -X GET localhost:5031/job/data/read
```
This returns a list of dictionaries of asteroid information in the dataset for the user to sift through:
```bash
  {
    "H": "12.4",
    "a": "3.00501298539988",
    "ad": "3.27932327705013",
    "albedo": "0.205",
    "class": "MBA",
    "diameter": "11.146",
    "diameter_sigma": "0.263",
    "e": ".09128422838204392",
    "epoch": "2459000.5",
    "epoch_cal": "20200531.0000000",
    "epoch_mjd": "59000",
    "equinox": "J2000",
    "full_name": "  6937 Valadon (1010 T-2)",
    "i": "9.514736870524372",
    "id": "a0006937",
    "ma": "178.1723511111374",
    "moid": "1.7423",
    "moid_ld": "678.050891",
    "n": ".1892058431368658",
    "name": "Valadon",
    "neo": "N",
    "om": "203.276045030872",
    "orbit_id": "JPL 35",
    "pdes": "6937",
    "per": "1902.689652874974",
    "per_y": "5.20928036379185",
    "pha": "N",
    "prefix": "",
    "q": "2.73070269374963",
    "rms": ".47698",
    "sigma_a": "1.5942E-8",
    "sigma_ad": "1.7397E-8",
    "sigma_e": "4.4594E-8",
    "sigma_i": "5.1189E-6",
    "sigma_ma": "2.5341E-5",
    "sigma_n": "1.5056E-9",
    "sigma_om": "2.5346E-5",
    "sigma_per": "1.5141E-5",
    "sigma_q": "1.3247E-7",
    "sigma_tp": ".00013271",
    "sigma_w": "3.5453E-5",
    "spkid": "2006937",
    "tp": "2458058.814753090089",
    "tp_cal": "20171101.3147531",
    "w": "324.4727821109635"
  },
  {
    "H": "12.3",
    "a": "2.468093230171911",
    "ad": "2.983793222788395",
    "albedo": "0.610",
    "class": "MBA",
    "diameter": "6.084",
    "diameter_sigma": "0.291",
    "e": ".2089467230460184",
    "epoch": "2459000.5",
    "epoch_cal": "20200531.0000000",
    "epoch_mjd": "59000",
    "equinox": "J2000",
    "full_name": "  3958 Komendantov (1953 TC)",
    "i": "4.82425120797704",
    "id": "a0003958",
    "ma": "47.72722845399516",
    "moid": ".962024",
    "moid_ld": "374.39088008",
    "n": ".2541919148520257",
    "name": "Komendantov",
    "neo": "N",
    "om": "11.62673870639676",
    "orbit_id": "JPL 31",
    "pdes": "3958",
    "per": "1416.252756149104",
    "per_y": "3.87748872320083",
    "pha": "N",
    "prefix": "",
    "q": "1.952393237555428",
    "rms": ".40468",
    "sigma_a": "8.6625E-9",
    "sigma_ad": "1.0472E-8",
    "sigma_e": "3.8273E-8",
    "sigma_i": "4.8224E-6",
    "sigma_ma": "8.963E-6",
    "sigma_n": "1.3382E-9",
    "sigma_om": "3.4709E-5",
    "sigma_per": "7.4561E-6",
    "sigma_q": "9.4095E-8",
    "sigma_tp": "3.543E-5",
    "sigma_w": "3.647E-5",
    "spkid": "2003958",
    "tp": "2458812.739392107421",
    "tp_cal": "20191125.2393921",
    "w": "29.25649653950637"
  }
]
```

### Updating the existing data
If the user wishes to update existing data:
```bash
[funky@mnky ~]curl -X POST localhost:5031/data
```
The `POST` option indicates that the user is requesting to add data in the database. A message indicating the success of the operation will be returned as an output:

### Deleting the existing data
In order to delete data from the database, perform:
```bash
[funky@mnky ~]curl -X DELETE localhost:5031/data/reset
```
A message to the user will display that the operation was successful

Once the database is populated, curl commands can be made so the program can perform the respective, queried routes.

### Curl commands 
Calling routes for the functions creates a new job for the program:
```bash
[funky@mnky ~]curl -X GET localhost:5031/job/<route>
```
The program will create a `job id` to the corresponding route that was called, which is stored in the `job-ids` in the database.
In order to see the contents of the list that stores this information:
```bash
[funky@mnky ~]curl -X GET localhost:5031/stored/job-ids
```

This will show the route requested and its respective job id. The user can copy the job id and perform the following to recieve the requested output
```bash
[funky@mnky ~]curl -X GET localhost:5031/job/result/<job_id>
```
Refer back to the example above as visual example of the [above](###Help-Message) mentioned commands
## Files 

### /docker
- *Dockerfile.api*   
This is the Dockerfile that builds the image and all dependencies to run the Flask API
- *Dockerfile.wrk*   
This is the Dockerfile that builds the image and all dependencies for workers. 

### /kubernetes 
- *app-prod-api-deployment.yml*
This pulls asteroid API container from Dockerhub and deploys it.
- *app-prod-api-service.yml*
This provides an IP for the user to curl for their routes.
- *app-prod-db-deployment.yml*
This pulls the Redis image from DockerHub and deploys the database.
- *app-prod-db-pvc.yml*
This provides a Redis IP so that the deployments can access the dataset's database.
- *app-prod-db-service.yml*
This makes a request for storage to the k8's admin for the database.
- *app-prod-wrk-deployment.yml*
This pulls worker container from DockerHub and deploys it so that the workers can be working on the queue in the background. 

### /src  
- *app.py*  
This is the main file for the API, with all the available routes the user can use. 
- *worker.py*   
This file contains the worker script, which utilizes functions from jobs.py to preform queued jobs. 
- *jobs.py*   
This file contains all job related functions, such as save, update, and so on. These functions are called in ``app.py`` as a part of the various routes called by the user. 





## Citations
Hossain, M. S. (2022, May 11). Asteroid dataset. Kaggle. Retrieved May 12, 2022, from https://www.kaggle.com/datasets/sakhawat18/asteroid-dataset?resource=download 

