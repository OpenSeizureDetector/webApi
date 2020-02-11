<template>
  <v-container>
    <v-card>
      <v-card-title>
	<h1>Events</h1>
      </v-card-title>
      <v-card-text>
	<p>Select Events by Date:</p>
	<v-form ref="form" v-model="valid" lazy-validation>
	  <v-datetime-picker
	    label="Start"
	    v-model="startDateTime"
	    date-format="yyyy-MM-dd"
	    time-format="HH:mm:ss">
	  </v-datetime-picker>
	  <v-datetime-picker
	    label="End"
	    v-model="endDateTime"
	    date-format="yyyy-MM-dd"
	    time-format="HH:mm:ss">
	    >
	  </v-datetime-picker>
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
      <template v-slot:item.eventType= {item}>
	{{ eventTypes[item.eventType].text }}
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
	    { value: 6 ,  text: "Other Medical Issue" }
	],
	tableHeaders : [
	    {text: "Date/Time", value: 'dataTime'},
	    {text: "Event Type", value: 'eventType'},
	    {text: "Notes", value: 'desc'}
	    ],
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
	}
    },
    
    methods: {
	getEvents() {
	    var self = this;
            if (this.$refs.form.validate()) {
		console.log("getEvents() - FIXME - this doesn't do anything");
		console.log("....url="+this.url+", token="+this.token);
		const config = {
		    headers: { Authorization: `Token `+this.token }
		};
		console.log("....config="+JSON.stringify(config));
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
	    }
    }
};
</script>

<style scoped>
</style>
