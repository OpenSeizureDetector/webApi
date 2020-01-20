# webApi
A RESTful web API for storing and retrieving seizure detector data for classification and analysis - primarily intended to collect 'normal' and 'seizure' labelled data so we can train machine learning algorithms to tell the difference

## Structure
 1 Based on CakePHP so that it can run on low cost web hosting providers.
 1 Uses MySQL back end to be conventional.
 1 Very simple RESTful API initially - no fancy login screens etc. in the first version.
 1 The main elements are data samples, which is a 5 second sample of data with some calculated meta data stored.
 1 Authentication is on a per-user basis, where a user is a user of the web api.
 1 The person wearing the watch is called a 'Wearer'.   A single authentication user can manage the data for multiple wearers.
 

## Functions
  1 Create Single dataSample, associated with a given wearer.
  1 Categorise a given dataset
  1 Download data for a given wearer
  
  
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
