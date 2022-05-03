AlgTest - OpenSeizureDetector Algorithm Testing
===============================================

This folder contains the test framework to assess potential new seizure
detection algorithms by running real data collected using the Data Sharing
system through the proposed algorithm and comparing it to the original
OpenSeizureDetector algorithm results.

Each Algorithm should be implemented as a sub-class of sdAlg.SdAlg
As a minimum it should provide a single function processDp(dpStr) which
accepts a JSON string representing a single datapoint.
It should return a JSON string which contains as a minimum an alarmState
integer element, whose values are:
	0 : OK
	1 : WARNING
	2 : ALARM
Other elements may be included in the return value.