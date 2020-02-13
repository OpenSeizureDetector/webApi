<template>
  <v-container>
    <v-card>
      <v-card-title>
	<h1>Events - Select Events by Date</h1>
      </v-card-title>
      <v-card-text>
	<v-form ref="form" v-model="valid" lazy-validation>
	  <v-row>
	    <v-col>
	      <v-datetime-picker
		label="Start"
		v-model="startDateTime"
		date-format="yyyy-MM-dd"
		time-format="HH:mm:ss">
	      </v-datetime-picker>
	    </v-col>
	    <v-col>
	      <v-datetime-picker
		label="End"
		v-model="endDateTime"
		date-format="yyyy-MM-dd"
		time-format="HH:mm:ss">
		>
	      </v-datetime-picker>
	    </v-col>
	  </v-row>
	<v-btn color="primary" @click="getEvents">Get Events</v-btn>
	</v-form>
      </v-card-text>
      <v-card-actions>
      </v-card-actions>
    </v-card>
    
    <v-data-table
      :headers="tableHeaders"
      :items="events"
      :items-per-page="20"
      class="elevation-1"
      >
      <template v-slot:top>
	<v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2"
		   v-on="on">Add New Event</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">Create / Edit Event</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
		    <v-datetime-picker
		      label="Event Date/Time"
		      v-model="editedEvent.dataTime"
		      date-format="yyyy-MM-dd"
		      time-format="HH:mm:ss">
		      >
		    </v-datetime-picker>

                  </v-col>
                  <v-col cols="12" sm="6" md="4">
		    <v-select
		      v-model="editedEvent.eventType"
		      :items="eventTypes"
		      menu-props="auto"
		      hide-details
		      label="Event Type"
		      single-line
		      ></v-select>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedEvent.desc" label="Description"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
      <template v-slot:item.dataTime = {item}>
	<!--{{ dateStr(item.dataTime) }}-->
	{{ dateStr(item.dataTime) }}
      </template>
      <template v-slot:item.eventType= {item}>
	<span  v-bind:style="{ backgroundColor: 
		      (item.eventType < 2 ? 'LightYellow' : 'transparent' ),
		      color:(item.eventType>3 ?'red' : 'black'),
		      'font-weight':(item.eventType>3 ? 'bold' : 'normal')
		      }" 
		      >
	  {{ eventTypes[item.eventType].text }}
	  </span>
      </template>
      <template v-slot:item.action="{ item }">
	<v-icon small class="mr-2" @click="editEvent(item)">
          mdi-pencil
</v-icon>
	<v-icon small @click="deleteEvent(item)">
          mdi-delete
	</v-icon>
      </template>

    </v-data-table>
  </v-container>
</template>

<script>
import axios from 'axios';
var dateFormat = require('dateformat');
export default {
    name: 'Events',
    data() { return {
	dialog: false,
	valid: false,
	dateFormatStr : "yyyy-mm-dd hh:MM:ss",
	startDateTime: "2019-01-01 00:00:00",
	endDateTime: "2021-01-01 00:00:00",
	events: [],
	eventTypes : [
	    { value: 0 , text: "Alarm (unvalidated)" },
	    { value: 1 ,  text: "Warning (unvalidated)" },
	    { value: 2 ,  text: "False Alarm" },
	    { value: 3 ,  text: "False Warning" },
	    { value: 4 ,  text: "Tonic-Clonic Seizure" },
	    { value: 5 ,  text: "Other Seizure" },
	    { value: 6 ,  text: "Other Medical Issue" },
	    { value: 7 ,  text: "Other Event" }
	],
	tableHeaders : [
	    {text: "Date/Time", value: 'dataTime'},
	    {text: "Event Type", value: 'eventType'},
	    {text: "Notes", value: 'desc'},
	    {text: "Actions", value: 'action'}
	],
	editedIndex : -1,
	editedEvent : {
	    id : null,
	    dataTime : new Date(),
	    eventType : 7,
	    desc : "",
	    },
	defaultEvent : {
	    dataTime : new Date(),
	    eventType : 7,
	    desc : "Please enter description",
	    },
    };
	   },
    computed: {
	token () {
                return this.$store.state.token;
            },
	url () {
                return this.$store.state.baseUrl;
        },
	eventTypeText(eventType) {
	    return this.eventTypes[eventType];
	},
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    created() {
	console.log("Events.vue.created()");
	//this.getEvents();
    },
    mounted() {
	console.log("Events.vue.mounted()");
	this.getEvents();
    },
    
    methods: {
	dateStr: function(dataTime) {
	    var d;
	    if (dataTime instanceof Date) {
		//console.log("dateSTr - dataTime is already a Date object");
		d = dataTime;
	    } else {
		//console.log("dateStr - converting dataTime to Date object");
		d = Date.parse(dataTime);
	    }
	    var dStr = dateFormat(d, this.dateFormatStr); 
	    //console.log("Converting "+dataTime+" to "+dStr);
	    return dStr;
	},
	getEvents() {
	    var self = this;
            if (this.$refs.form.validate()) {
		const config = {
		    headers: { Authorization: `Token `+this.token }
		};
		console.log("getEvents()....config="+JSON.stringify(config));
		axios(
		    {
			method: 'get',
			url: this.url+'/events/?start='+
			    dateFormat(this.startDateTime,
				       self.dateFormatStr)+
			    '&end='+
			    dateFormat(this.endDateTime,
					       self.dateFormatStr),
			headers: { Authorization: `Token `+this.token },
			data: {
			},
			validateStatus: function(status) {
			    return status<500;
			},
		    }
		)
		    .then(response => {
			if (response.status == 200) {
			    console.log(response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			    self.events = response.data['results'];
			    console.log("set events to "+JSON.stringify(self.events));
			} else {
			    console.log(response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			}
		    })
		    //.catch((err) => {
		//	console.log("catch(): err="+JSON.stringify(err));
		 //   })
	    }
        },
	uploadToServer(eventObj) {
	    // Upload the given event to the database.  If the ID is
	    // included in the object, it uses PUT to update an existing
	    // entry.  If ID is not specified it uses POST to create another one
	    var self = this;
	    var methodStr;
	    var urlStr;
	    const config = {
		headers: { Authorization: `Token `+this.token }
	    };
	    console.log("uploadToServer()....event="+JSON.stringify(eventObj));
	    if (eventObj['id'] != null) {
		console.log("we have an existing record id, so updating it");
		methodStr = "PUT";
		urlStr = this.url+'/events/'+eventObj['id']+'/';
	    } else {
		console.log("no record id present - creating it");
		methodStr = "POST";
		urlStr = this.url+'/events/';
	    }

	    console.log(".........methodStr="+methodStr+" urlStr="+urlStr);
	    axios(
		{
		    method: methodStr,
		    url: urlStr,
		    headers: { Authorization: `Token `+this.token },
		    data: eventObj,
		    validateStatus: function(status) {
			return status<500;
			},
		}
	    )
		.then(response => {
		    if (response.status == 200 ||
		       response.status == 201 ) {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
		    } else {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
		    
			alert("Failed to upload record: " +
			      response.status +
			      " - " + response.statusText +
			      " : " +JSON.stringify(response.data));
		    }
		})
        },
	deleteOnServer(eventId) {
	    // deletes event number eventId on the server.
	    var self = this;
	    var methodStr;
	    var urlStr;
	    const config = {
		headers: { Authorization: `Token `+this.token }
	    };
	    methodStr = "DELETE";
	    urlStr = this.url+'/events/'+eventId+'/';
	    console.log(".........methodStr="+methodStr+" urlStr="+urlStr);
	    axios(
		{
		    method: methodStr,
		    url: urlStr,
		    headers: { Authorization: `Token `+this.token },
		    data: {},
		    validateStatus: function(status) {
			return status<500;
			},
		}
	    )
		.then(response => {
		    if (response.status == 204) {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
		    } else {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
		    
			alert("Failed to delete record: " +
			      response.status +
			      " - " + response.statusText +
			      " : " +JSON.stringify(response.data));
		    }
		})
        },
	editEvent (event) {
            this.editedIndex = this.events.indexOf(event)
            this.editedEvent = Object.assign({}, event)
	    console.log("Type of dataTime = "+typeof this.editedEvent['dataTime']);
	    if (this.editedEvent['dataTime'] instanceof Date) {
		console.log("editEvent: converting Date object to String");
		this.editedEvent['dataTime'] = dateFormat(this.editedEvent['dataTime'], this.dateFormatStr); 
		//this.editedEvent['dataTime']=Date.parse(this.editedEvent['dataTime']);
	    } else {
		console.log("editEvent - dataTime is already a String object - reformatting");
		var d = Date.parse(this.editedEvent['dataTime']);
		this.editedEvent['dataTime'] = dateFormat(d, this.dateFormatStr); 
		console.log("dataTime="+this.editedEvent['dataTime']);
		}
            this.dialog = true
	},
	
	deleteEvent (event) {
            const index = this.events.indexOf(event);
	    var eventId = event['id'];
            if (confirm('Are you sure you want to delete this event?')) {
		this.events.splice(index, 1);
		this.deleteOnServer(eventId);
	    }
	},
	
	close () {
            this.dialog = false
            setTimeout(() => {
		this.editedEvent = Object.assign({}, this.defaultEvent)
		this.editedIndex = -1
            }, 300)
	},

	save () {
            if (this.editedIndex > -1) {
		Object.assign(this.events[this.editedIndex], this.editedEvent);
            } else {
		this.events.push(this.editedEvent)
            }
	    this.uploadToServer(this.editedEvent);
            this.close()
	},
    },

};
</script>

<style scoped>
</style>
