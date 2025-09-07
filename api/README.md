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
From Ubuntu 18.04 LTS or higher

```
apt install build-essential python3-dev mysql-server mysql-client-dev
```

### Backend
```
python -m venv ~/pyEnvs/webpy
source ~/pyEnvs/webpy/bin/activate

git clone https://github.com/OpenSeizureDetector/webApi.git
cd webApi/api

pip install -r requirements.txt

ln -s static static2

```
The symbolic link to static2 is only required for developent using the django development server as described below.   It is not required for production using the nginx web server, because the static files location is specified in the server configuration file, so the django app is never passed requests to /static
 
Create a mysql database and associated user/password using
'''
sudo mysql -u root
CREATE DATABASE osd;
CREATE USER 'osd'@'localhost' identified by '<OSD PASSWORD>';
GRANT ALL ON osd.* to 'osd'@'localhost';
'''

copy webApi/api/webApi/credentials.json.template to webApi/api/webApi/credentials.json

Edit webApi/api/webApi/credentials.json to use database credentials that will give it access to your mySql database, and provide a secret key string for use with encryption.

```
./manage.py makemigrations
./manage.py migrate
```

### Front End
We do not have a working database access front end at the moment - simple activities such as user registration and validation are achieved using simple static web pages in the api/static folder.

# Deployment
## Development
Use the django development server with
```
./manage.py runserver
```
The site should be visible on http://localhost:8000
 
## Production 
Use the gunicorn interface with the nginx web server, controlled with the 'supervisor' process as follows (from https://medium.com/swlh/deploying-django-apps-for-production-on-ubuntu-server-18-04-using-gunicorn-supervisor-nginx
 
 ```
 sudo apt install supervisor nginx
 pip install gunicorn
 cd api
 ln -s webApi/wsgi.py webApi/webApi.wsgi
 ```
 Test that gunicorn can server the web api django project with:
 ```
 gunicorn --bind 0.0.0.0:8000 webApi.wsgi
 ```
 Then set up supervisor to start gunicorn and re-start it if it crashes etc.   Create /etc/supervisor/conf.d/gunicorn.conf which should look somehing like:
 ```
 [program:osd_webApi]
directory=<path>/webapi/api
command=<path_to_virtual_env>/bin/gunicorn webApi.wsgi:application --workers 3 --bind 127.0.0.1:8000 --log-level info;
stdout_logfile = <path>/logs/gunicorn/access.log
stderr_logfile = <path>/logs/gunicorn/error.log
stdout_logfile_maxbytes=5000000
stderr_logfile_maxbytes=5000000
stdout_logfile_backups=100000
stderr_logfile_backups=100000
autostart=true
autorestart=true
startsecs=10
stopasgroup=true
priority=99
```
Create the directory <path>/logs/gunicorn as used for the log files above.

Start Supervisor
``` 
sudo supervisorctl reread
sudo supervisorctl update
```
 
Configure nginx by creaing /etc/nginx/sites_available/webApi which contains
 
```
 server {
    listen 80;
    server_name <your_server_domain_name_or_IP>;
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root <path>api;
    }
    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```
 
Then enable the site with
 ```
 sudo ln -s /etc/nginx/sites-available/webApi /etc/nginx/sites-enabled
 ```
 Test nginx configuration with
 ```
 sudo nginx -t
 ```
 Then restart nginx with 
 ```
 sudo systemctl restart nginx
 ```
 
 If you change anything related to hostnames, you need to change both /etc/nginx/sites-available/webApi and also <path>webApi/api/webApi/settings.py to include the new hostname or ip address.
 You then restart the gunicorn process using supervisor with 
 ```
 supervisorctl reread
 supervisorctl update
```
 ...and then re-start the NGINX web server with
 ```
 systemctl restart nginx
 ```
 
 
 # Enable Encryption
 The API is transferring users' personal data to our server so the data transfer must be encrypted for privacy.
 
 To achieve this we use LetsEncrypt certificates by doing the following.
 
 Install certbot (Which runs under snapd)
 ```
 sudo apt install snapd
 sudo snap install core
 sudo snap refresh core
 sudo snap install --classic certbot
 sudo ln -s /snap/bin/certbot /usr/bin/certbot
 ```
 Then obtain and install a certificate for the installed host names using
 ```
 sudo certbot --nginx
 ```
 And follow the prompts to select which host name you want certificates for etc.   This should also set certbox to renew teh certificate automatically without needing regular user interaction.
 
 The certificates are saved in /etc/letsencrypt/live/<host name>
 
 You should now be able to access the server with https://osdapi.ddns.net (or whatever hostname you used).
 
 
## Enable Email
The user registration process relies on sending confirmation emails to the user.

**Note:** The initial intention was to host our own email server (e.g., using Postfix and DKIM authentication). However, this proved unreliable for production because many major email providers (like Gmail and Outlook) frequently rejected or marked these emails as spam, even with proper authentication.

**For the production system, we now use an external email provider (such as Gmail SMTP, SendGrid, or similar) to ensure reliable delivery of confirmation and notification emails.**

To configure this, set the appropriate SMTP credentials in `webApi/api/webApi/credentials.json` and ensure your Django settings load these values.


