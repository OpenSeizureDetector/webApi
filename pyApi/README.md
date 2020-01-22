OpenSeizureDetector pyApi
#########################

This is a python (Django framework) implementation of a REST api
to save and retrieve data from wearer's seizure detectors for future
analysis.

The structure is as follows:

pyApi
   - wearers app - handles creating and updating information on wearers of
                   openseizuredetector watches.
   - rawdata app - handles creating, modifying and retrieving seizure detector
                   data records.
   - events app - handles creating, updating and retrieving seizure detector
                   events such as real seizures or false alarms.
				   
				   
URLs
    /authenticate - retrieve an access token for a given wearer to upload data.
	/wearers - list wearers
	
	
	
