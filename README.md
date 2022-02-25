Compose metadata python application
Python application

Versions Used:
Docker version 20.10.12
Docker Compose version v2.2.3
ubuntu 20.04
python 3.8

Project structure:
.
├── docker-compose.yml
├── app
    ├── Dockerfile
    ├── requirements.txt
    └── getweatherdata.py

docker-compose.yml

services: 
  app: 
    build: app 
	environment:
      - API_KEY=b6f5221855dd7432fcbb52b170b5f172
    command: python3 getweatherdata.py

Build with docker compose
$ docker compose build
Sending build context to Docker daemon  2.662kB
Step 1/5 : FROM python:3.8
 ---> ec926d993ba8
Step 2/5 : ADD . ~/code
 ---> Using cache
 ---> a57656ed4510
Step 3/5 : WORKDIR ~/code
 ---> Using cache
 ---> 08fec795460b
Step 4/5 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> b8722658c679
Step 5/5 : CMD ["python3", "getweatherdata.py"]
 ---> Using cache
 ---> 471b80dadb5e
Successfully built 471b80dadb5e
Successfully tagged compose-python_app:latest

Deploy with docker-compose
$ docker compose up
 ⠿ Container compose-python-app-1  Created
Attaching to compose-python-app-1
compose-python-app-1  | in getweatherdata main
compose-python-app-1  | API KEY from docker-compose file: b6f5221855dd7432fcbb52b170b5f172
compose-python-app-1  | Connect openweathermap API and retrieve last 5 days data - START
compose-python-app-1  | Connect openweathermap API and retrieve last 5 days data - END
compose-python-app-1  | Write JSON data into file data.json - Start
compose-python-app-1  | Write JSON data into file data.json - End
compose-python-app-1  | Read JSON data. Flatten the data and deduplicate process - Start
compose-python-app-1  | Write Flatten data into text file: original_data.txt
compose-python-app-1  | Read JSON Data. Flatten the data and deduplicate process - End
compose-python-app-1  | Build First Dataset containing location, date and highest temperature - Start
compose-python-app-1  | getfirstdataset - Read whole 5 days deduplicated data
compose-python-app-1  | getfirstdataset - record highest temperatures by location and month
compose-python-app-1  | getfirstdataset - write first dataset into csv file
compose-python-app-1  | Build First Dataset containing location, date and highest Temperature - End
compose-python-app-1  | Build Second Dataset containing avg temp, min temp, loc of min temp, max temp - Start
compose-python-app-1  | getseconddataset - Read whole 5 days deduplicated data
compose-python-app-1  | getseconddataset - get max temp, loc of max temp - per day
compose-python-app-1  | getseconddataset - get min temp, loc of min temp - per day
compose-python-app-1  | getseconddataset - get avg temp per day
compose-python-app-1  | Build Second Dataset containing avg temp, min temp, loc of min temp, max temp - End
compose-python-app-1  | End
compose-python-app-1 exited with code 0

Expected result
Listing containers must show one container exited as below:

$ docker ps -a
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS                      PORTS     NAMES
5fb584050a20   compose-python_app   "python3 getweatherd…"   6 minutes ago    Exited (0) 4 minutes ago              compose-python-app-1
5

$ docker container cp 5fb584050a20:/~/code/original_data.txt /tmp/
$ docker container cp 5fb584050a20:/~/code/firstdataset.txt /tmp/
$ docker container cp 5fb584050a20:/~/code/seconddataset.txt /tmp/


$ docker compose down