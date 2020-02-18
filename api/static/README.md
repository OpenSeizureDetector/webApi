README - osd-app
================

This is a web based front end to the database API.   It serves two main purposes:
   1  To provide a user registration facility (that can be called from the
      android app)
   2  To provide a facility to edit events (genuine alarms, missed seizures and false alarms) to provide information on what was happening at the time.
   
   
When the user initially accesses the page they will see a login screen.
The login screen includes a button to show a new user registration screen.

When the user is authenticated they will see a home screen which lists
events associated with their account.


Structure
---------
The code is a single page web app writen using the vuejs framework.
It uses the vuex state controller for communication between components.
The Vuetify framework is used for the html front end.

I have tried to use the conventional structure for the app in the hope that
it is easier for folks that know about vue etc. to understand and maybe
contribute to, because Javascript is not my thing!

