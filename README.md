# webApi
This repository contains the code for a web site that will allow OpenSeizureDetector users to upload data from seizures
or false alarms.    This will allow us to build up an anonymised open data set of seizure data to use for research to develop
better detection algorithms - there is very little publicly availale seizure data so it is very difficult to tes new algorithms
to see if the improve detection reliability or reduce false alarms.

# Structure
The code uses a mysql database and there is Django python web frame work application that provides an API (see the 'webApi' folder)

There is also a javascritp based front end that will allow users to view their data and correct or anotate seizuzre or 
false alarm reports.  (See the 'frontend' folder)
