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

  
  
## Tests
  1 Unauthenticated user uploads data - fail.
  1 Authenticated user uploads data for a wearer assocaited with that user - success
  2 Authenticated user uploads data for a wearer not associated with that user - Fail
  3 Authenticated user edits data for a wearer assocaited with that user - success
  3 Authenticated user edits data for a wearer not assocaited with that user - Fail


## Installation
From Ubuntu 18.04 LTS
sudo apt install php php-cli php-json php-pdo php-mysql php-zip 
sudo apt install php-gd php-mbstring php-curl php-xml php-pear 
sudo apt install php-bcmath php-intl
git clone https://github.com/OpenSeizureDetector/webApi.git
cd webApi/app
Install the php dependencies with:
../composer.phar install

Create a mysql database and associated user/password
Execute mysql -u <user name> -p <database name> <createdb.sql

Edit webApi/app/config/app.php to use database credentials that will give
it access to your mySql database.
bin/cake server
 - should be able to see somethign useful at http://localhost:8765
 
 
 Create mysql databases:
 sudo mysql -u root
    > create database osd;
	> create database osd_test;
	> grant all on osd.* to osd@localhost identified by '<insert password>';
	> grant all on osd_test.* to osd@localhost;
	> exit
	
 Check database:
 mysql -u osd -p osd
 <type password when prompted>
	 > show tables;
	 - should give a list of tables
	 
	 > select * from users;
	 - should list all users currently defined.



Note:  Initial database has three users defined as follows:
admin / admin_pw
analyst / analyst_pw
user / user_pw

** Change their passwords before making the system live using app/bin/cake Password command **
