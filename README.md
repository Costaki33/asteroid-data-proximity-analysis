# Asteroid Data Proximity Analysis

(explain project motivation and what the program is about / why its important)


## Deploying to Kubernetes

(instructions on how to deploy program to k8s)


### Integration Testing

(how to run integration tests)


## Interacting with the Program

(how to interact with program)
Once the user has access to the software, they now have the ability to query routes for the program to satisfy requests.

(C: create new data in database)
In order to create new data into the `redis` database, the command is as follows:
```curl -X POST localhost:5006/data```
This will add the dataset to the server, where all of the raw data is stored into database 0. A message will be returned to the user indicating that the data has been adequately stored.

(R: read data in database)
To read the existing data in the database, perform the command:
```curl -X GET localhost:5006/job/data/read```
This returns a list of dictionaries of asteroid information in the dataset for the user to sift through.

(U: update data)
If the user wishes to update existing data:
```curl -X POST localhost:5006/data```
The `POST` option indicates that the user is requesting to add data in the database. A message indicating the success of the operation will be returned as an output.

(D: delete data)
In order to delete data from the database, perform:
```curl -X DELETE localhost:5006/data/reset```
A message to the user will display that the operation was successful.

(curl operations)
Once the database is populated, curl commands can be made so the program can perform the respective, queried routes.

Calling routes for the functions creates a new job for the program:
```curl -X GET localhost:5006/job/<route>```
The program will create a `job id` to the corresponding route that was called, which is stored in the `job-ids` in the database.
In order to see the contents of the list that stores this information:
```curl -X GET localhost:5006/stored/job-ids`

This will show the route requested and its respective job id. The user can copy the job id and perform the following to recieve the requested output
```curl -X GET localhost:5006/job/result/<job_id>```

