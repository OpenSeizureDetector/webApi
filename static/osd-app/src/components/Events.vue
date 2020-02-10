<template>
    <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm16 md16>
	    <h1>Events</h1>
	    url= {{url}}
	    token={{token}}
            <v-form ref="form" v-model="valid" lazy-validation>
 	      <v-btn color="primary" @click="getEvents">Get Events</v-btn>
	      <ul id="events-list">
		<li v-for="e in events">
		  {{e.dataTime}} : {{e.eventType}}
		  <v-select
		    v-model="e.eventType"
		    :items="eventTypes"
		    menu-props="auto"
		    hide-details
		    label="Select"
		    single-line
		    ></v-select>
		  <v-text-field
		    v-model="e.desc"
		    label="Description"
		    ></v-text-field>
 		  <v-btn color="primary" @click="updateEvent">Update</v-btn>
		</li>
	      </ul>
           </v-form>
	    
          </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Events',
    data() { return {
	valid: false,
	events: [],
	eventTypes : [
	    { value: 0 , text: "Alarm (unvalidated)" },
	    { value: 1 ,  text: "Warning (unvalidated)" },
	    { value: 2 ,  text: "False Alarm" },
	    { value: 3 ,  text: "False Warning" },
	    { value: 4 ,  text: "Tonic-Clonic Seizure" },
	    { value: 5 ,  text: "Other Seizure" },
	    { value: 6 ,  text: "Other Medical Issue" }
	]
    };
	   },
    computed: {
	token () {
                return this.$store.state.token;
            },
	url () {
                return this.$store.state.baseUrl;
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
			url: this.url+'/events/',
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
