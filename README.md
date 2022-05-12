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


## Deploying to Kubernetes

(instructions on how to deploy program to k8s)


### Integration Testing

(how to run integration tests)


## Interacting with the Program

(how to interact with program)
Once the user has access to the software, they now have the ability to query routes for the program to satisfy requests.

CRUD stuff:

In order to create new data into the `redis` database, the command is as follows:
```ruby
curl -X POST localhost:5006/data
```
This will add the dataset to the server, where all of the raw data is stored into database 0. A message will be returned to the user indicating that the data has been adequately stored.

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

