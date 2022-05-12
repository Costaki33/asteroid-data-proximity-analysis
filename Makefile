NAME="costaki33"
APP="asteroid-data"
VER="0.1"
RPORT="6431"
FPORT="5031"
UID="876632"
GID="816966"

#Make that will show all the make functionalities incase an invalid
list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : \
		2>/dev/null | awk -v \
	RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
	| sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

#Shows the runninng contianers and images
list:
	- docker ps -a | grep ${NAME}
	- docker images | grep ${NAME}

#This will build the image of the API image
build-api:
	docker build -t ${NAME}/${APP}-api:${VER} \
	-f docker/Dockerfile.api .

#This will build the image of the redis DB image, by pulling the redis:6 image from DockerHub
build-db:
	docker pull redis:6

#This will build the image of the worker image
build-wrk:
	docker build -t ${NAME}/${APP}-wrk:${VER} \
	-f docker/Dockerfile.wrk .

#This will run the redis container and will save the data in a file
run-db: build-db
	docker run --name ${NAME}-db \
	-p ${RPORT}:6379 -d \
	-u ${UID}:${GID} \
	-v ${PWD}/data/:/data \
	redis:6 \
	--save 1 1

#This will run the API container with a port running in the background
#It also finds the IP address of the flask container
run-api: build-api
	RIP=$$(docker inspect ${NAME}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') &&\
        docker run --name ${NAME}-api \
		-p ${FPORT}:5000 \
		-d \
		-e REDIS_IP=$${RIP} \
		${NAME}/${APP}-api:${VER}

#This will run the worker container in the background
run-wrk: build-wrk
	RIP=$$(docker inspect ${NAME}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-wrk \
	-e REDIS_IP=$${RIP} \
	-d \
        ${NAME}/${APP}-wrk:${VER}


#Clean all the db containers, by stopping and removing all the running db containers
clean-db:
	- docker stop ${NAME}-db && docker rm -f ${NAME}-db

#Clean all the api contianers, by stopping and removing all the running api containers
clean-api:
	- docker stop ${NAME}-api && docker rm -f ${NAME}-api

#Clean all the worker containers, by stopping and removing all the running worker containers
clean-wrk:
	- docker stop ${NAME}-wrk && docker rm -f ${NAME}-wrk



#The cycle for developing the API container
#Steps:
#1.- Delete any running continaer with the old source code
#2.- Re-build the image with docker build
#3.- Start up a new container with docker run
cycle-api: clean-api build-api run-api list

cycle-wrk: clean-wrk build-wrk run-wrk

cycle-wrk-api: clean-api clean-wrk run-wrk run-api list

build-all: build-db build-api build-wrk

run-all: run-db run-api run-wrk

clean-all: clean-db clean-api clean-wrk

all: build-all run-all clean-all

test-api:
	curl -X GET localhost:5031/
	#curl -X POST localhost:5031/data
	#curl -X GET localhost:5031/job/diameters
	#curl -X GET localhost:5031/job/names
	#curl -X GET localhost:5031/stored/job-ids
	#curl -X GET localhost:5031/id/<specific_id>
	#curl -X GET localhost:5031/job/diameter/gaussian_distribution


