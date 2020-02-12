<template>
  <v-container>
    <v-card>
      <v-card-title>
	<h1>Events</h1>
      </v-card-title>
      <v-card-text>
	<p>Select Events by Date:</p>
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
	</v-form>
      </v-card-text>
      <v-card-actions>
	<v-btn color="primary" @click="getEvents">Get Events</v-btn>
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
		   v-on="on">New Event</v-btn>
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
	{{ item.dataTime }}
      </template>
      <template v-slot:item.eventType= {item}>
	{{ eventTypes[item.eventType].text }}
      </template>
      <template v-slot:item.action="{ item }">
	<v-icon small class="mr-2" @click="editEvent(item)">
          edit
	</v-icon>
	<v-icon small @click="deleteEvent(item)">
          delete
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
	dateStr: function(dataTime) {
	    var d;
	    if (dataTime instanceof Date) {
		console.log("dateSTr - dataTime is Date");
		d = dataTime;
	    } else {
		console.log("dateStr - converting dataTime to Date");
		d = Date(dataTime);
	    }
	    return dateFormat(d, "yyyy-mm-dd hh:MM:ss");
	}
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    created() {
	console.log("Events.vue.created()");
    },
    
    methods: {
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
				       "yyyy-mm-dd hh:MM:ss")+
			    '&end='+
			    dateFormat(this.endDateTime,
					       "yyyy-mm-dd hh:MM:ss"),
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
	updateEvent() {
	    console.log("updateEvent()");
	},
	editEvent (event) {
            this.editedIndex = this.events.indexOf(event)
            this.editedEvent = Object.assign({}, event)
            this.dialog = true
	},
	
	deleteEvent (event) {
            const index = this.events.indexOf(event)
            confirm('Are you sure you want to delete this event?') && this.events.splice(event, 1)
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
		Object.assign(this.events[this.editedIndex], this.editedEvent)
            } else {
		this.events.push(this.editedEvent)
            }
            this.close()
	},
    },

};
</script>

<style scoped>
</style>
