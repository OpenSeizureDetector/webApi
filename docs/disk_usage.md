# Dealing with a Full Disk

We have had issues where a user has mis-configured their system and it has uploaded several thousand events, and filled up the disk on the server.

The procedure to address this is:

  * Update the off-line version of the database using the makeOsdDb.py script in the OpenSeizureDatabase curator_tools folder.
  * Check the maximum values of the event and datapoint ids:  select max(id) from events_event;   select max(id) from datapoints_datapoint;
  * Delete the contents of the events_event table:   truncate events_event;
  * Delete the contents of the datapoints_datapoint table:  truncate datapoints_datapoint;
  * Re-set the next event ID:  alter table events_event auto_increment=67705;   (or whatever the next ID value to be used is)
  * Re-set the next datapoint ID:  alter table datapoints_datapoint auto_increment=67705;   (or whatever the next ID value to be used is)

This should reduce the disk usage significantly and the system will generate events and datapoints with unique IDs based on the last ids before we shrank the database.
