<template>
    <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
	    <h1>User Profile</h1>

    <v-form ref="form" v-model="valid" lazy-validation>
    <h4>{{ profile.user }}</h4>
              <v-text-field
		name="uname"
		label="User Name:" 
                v-model="uname" required>
              </v-text-field>
	      <v-btn color="primary" @click="submit">Update</v-btn>
            </v-form>
	    
	    <p>
	      Not Registered?
              <v-btn text>Create account</v-btn>
	    </p>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Profile',
    data() { return {
	valid: false,
	profile : {
	    uname: '',
	    user: none,
	    dob: none,
	    medicalConditions: none,
	},
	uname: '',
    };
	   },
    methods: {
	submit() {
            if (this.$refs.form.validate()) {
		alert("submit() - FIXME - this doesn't do anything");
            }
	},
	getProfile() {
	    console.log("getProfile()....");
	    var self = this;
	    var url = this.$store.state.baseUrl + "/api/profile/";
	    var action = "get";
	    var data = {};
	    this.$store.dispatch("authRequest",{
		url: url,
		action: action,
		data: data,
		successCb: function(response) {
		    console.log("successCb - response="+JSON.stringify(response));
		    if (response.status==200) {
			if (response.data.count>0) {
			    self.profile = response.data.results[0];
			    console.log("proifle="+JSON.stringify(self.profile));
			} else {
			    console.log("no profile returned");
			    self.profile = {};
			}
		    } else {
			console.log("Unexpected status code "+response.status
				    +": "+response.statusText);
			alert("Unexpected status code "+response.status
			      +": "+response.statusText);
			self.profile={};
		    }
		},
		failCb: function(response) {
		    console.log("failCb - response="+JSON.stringify(response));
		    alert("failCb - response="+JSON.stringify(response));
		    
		}
	    });
	},
	getProfile1() {
	   var url = this.$store.state.baseUrl + "/api/profile/";
	    var self = this;
		const config = {
		    headers: { Authorization: `Token `+this.$store.state.token }
		};
		console.log("getProfile()....url="+url+", config="+JSON.stringify(config));
		axios(
		    {
			method: 'get',
			url: url,
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
			    self.profile = response.data['results'];
			    console.log("set profile to "+JSON.stringify(self.profile));
			} else {
			    console.log(response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			    alert("Incorrect Response Code: " + response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			}
		    })
	   }
    },
    mounted() {
    console.log("Events.vue.mounted()");
    this.getProfile();
    },

};
</script>

<style scoped>
</style>
