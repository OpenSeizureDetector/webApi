# webApi (Open Seizure Detector Data Sharing system)
This repository contains the code for the web site that allows OpenSeizureDetector users to upload data from seizures
or false alarms.    This will allow us to build up an anonymised open data set of seizure data to use for research to develop
better detection algorithms - there is very little publicly availale seizure data so it is very difficult to test new algorithms
to see if the improve detection reliability or reduce false alarms.

Users wishing to access the anonymised database of user contributed data should refer to the (Open Seizure Database)[https://github.com/OpenSeizureDetector/OpenSeizureDatabase].


# Structure
The code uses a mysql database and there is Django python web frame work application that provides an API (see the 'webApi' folder), which contains some installation instructions in its README.md file.

There is also a javascript based front end that will allow users to view their data and correct or anotate seizuzre or 
false alarm reports.  (See the 'frontend' folder), but this is not yet working.
