# webApi
A RESTful web API for storing and retrieving seizure detector data for classification and analysis - primarily intended to collect 'normal' and 'seizure' labelled data so we can train machine learning algorithms to tell the difference

## Structure
 1 Based on the Django Rest Framework, because I had a sense-of-humour-failure trying to use cakePHP - this limits which commercial proiders we can use to
 host it.
 1 Uses MySQL back end to be conventional.
 1 Very simple RESTful API initially, but utilise an open source library
 to do user registration.
 1 The main elements are datapoints, which is a 5 second sample of data with some calculated meta data stored.
 1 Each wearer of an OpenSeizureDetector watch needs a different user account
 for the API.

## Functions
| URL                                             | Function                                                                                                 | view                                                                                                                                                                                                     |
| ---                                             | --------                                                                                                 | -                                                                                                                                                                                                        |
| /datapoints/ - POST                             | to create a datapoint                                                         |                                                    |
| /datapoints/<id> - GET                          | to retrieve a datapoint, PUT to update it, DELETE to delete it.                                         
| /datapoints/<startDateTime>,<endDateTime> - GET | to retrieve datapoints within specified date/time range - returns datapoints for the authenticated user.  Includes any events in the time range. | /datapoints/<userId>,<startDateTime>,<endDateTime> - GET | to retrieve datapoints within specified date/time range - for the specified user - must be autenticated as an admin or analyst user to do this. | |
| /profile/<userId> - GET | Retrieve user profile information |
| /profile/<userId> - PUT | Update user profile information |
| /event - POST | Create an event - mark a date/time for a specific user as an event with optional notes. |
| /event/<id> - PUT | update an event |
| /event/<id> - DELETE | delete an event
| /eventCategories - GET | Retrieve list of valid event categories |

Retrieve all events for a given user:
GET /events/?user=14
Retrieve events for a given user over a given time frame
GET /events/?user=14&start=2019-11-04 07:44:00&duration=5
GET /events/?user=14&end=2019-11-04 07:49:00&duration=5
GET /events/?user=14&start=2019-11-04 07:44:00&end=2019-11-04 07:49:00
  
## Tests
  1 Unauthenticated user uploads data - fail.
  1 Authenticated user uploads data for a wearer assocaited with that user - success
  2 Authenticated user uploads data for a wearer not associated with that user - Fail
  3 Authenticated user edits data for a wearer assocaited with that user - success
  3 Authenticated user edits data for a wearer not assocaited with that user - Fail


## Installation
From Ubuntu 18.04 LTS

### Backend
mkvirtualenv --python=/usr/bin/python3 webpy
workon webpy
pip install django django-rest-framework
pip install mysqlclient
pip install django-rest-registration
pip install django-filter
pip install numpy
pip install django-cors-headers
git clone https://github.com/OpenSeizureDetector/webApi.git
cd webApi

Create a mysql database and associated user/password

copy webApi/webApi/credentials.json.template to webApi/webApi/credentials.json
Edit webApi/webApi/credentials.json to use database credentials that will give
it access to your mySql database.

./manage.py makemigrations
./manage.py migrate


### Front End
sudo apt install npm
npm install -g @vue/cli
