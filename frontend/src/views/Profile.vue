<template>

<v-container fill-height>
  <v-layout align-center justify-center>
    <v-flex>
      <h1>Profile - User: {{ profile.username }} ID: {{ profile.user }}</h1>
      <v-form ref="form" v-model="valid" lazy-validation>
	<v-row>
	  <v-col>
            <v-text-field
	      name="email"
	      label="email:" 
              v-model="profile.email" required>
            </v-text-field>
	  </v-col>
	  <v-col>
	  <v-checkbox
	    v-model="profile.is_superuser"
	    label="Admin" readonly=true
	    ></v-checkbox>
	  </v-col>
	  <v-col>
	  <v-checkbox
	    v-model="profile.is_staff"
	    label="Analyst" readonly=true
	    ></v-checkbox>
	  </v-col>
	</v-row>
	<v-row>
	  <v-col>
            <v-text-field
	      name="firstname"
	      label="First Name:" 
              v-model="profile.first_name" required>
            </v-text-field>
	  </v-col>
	  <v-col>
            <v-text-field
	      name="lastname"
	      label="Last Name:" 
              v-model="profile.last_name" required>
            </v-text-field>
	  </v-col>
	</v-row>
	<v-row>
	  <v-date-picker
	    label="Date of Birth: " <!--{{ profile.dob }}-->
	    v-model="profile.dob"
	    date-format="yyyy-MM-dd"
	    >
	  </v-date-picker>
	</v-row>
	<v-row>
          <v-text-field
	    name="medicalconditions"
	    label="Medical Conditions:" 
            v-model="profile.medicalConditions" required>
          </v-text-field>
	</v-row>
	<v-row>
	  <v-checkbox
	    v-model="profile.licenceAccepted"
	    label="Lience Agreement Accepted?: "
	    ></v-checkbox>
	</v-row>
	<v-btn color="primary" @click="submit">Update</v-btn>
      </v-form>      
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
  var dateFormat = require('dateformat');
export default {
	name: 'Profile',
	data() { return {
	    valid: false,
	    profile : {
		uname: 'none',
		user: null,
		dob: null,
		medicalConditions : "",
		licenceAccepted : false,
		is_superuser : false,
		is_staff : false,
	    },
	    profileDefault : {
		uname: 'none',
		user: null,
		dob: null,
		medicalConditions : "",
		licenceAccepted : false,
		is_superuser : false,
		is_staff : false,
	    },
	};
	       },
	methods: {
	    submit() {
		if (this.$refs.form.validate()) {
		    this.saveProfile();
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
				console.log("profile="+JSON.stringify(self.profile));
			    } else {
				console.log("no profile returned");
				self.profile = self.profileDefault;
			    }
			} else {
			    console.log("Unexpected status code "+response.status
					+": "+response.statusText);
			    alert("Unexpected status code "+response.status
				  +": "+response.statusText);
			    self.profile = self.profileDefault;
			}
		    },
		    failCb: function(response) {
			console.log("failCb - response="+JSON.stringify(response));
			alert("failCb - response="+JSON.stringify(response));
			//self.profile={};
		    }
		});
	    },
	    saveProfile() {
		console.log("saveProfile()....");
		var self = this;
		var url = this.$store.state.baseUrl + "/api/profile/"+self.profile.id+"/";
		var action = "put";
		var data = self.profile;
		console.log("sending data "+JSON.stringify(data));
		this.$store.dispatch("authRequest",{
		    url: url,
		    action: action,
		    data: data,
		    successCb: function(response) {
			console.log("successCb - response="+JSON.stringify(response));
			if (response.status==200) {
			    if (response.data.count>0) {
				self.profile = response.data.results[0];
				console.log("profile="+JSON.stringify(self.profile));
			    }
			} else {
			    console.log("Unexpected status code "+response.status
					+": "+response.statusText);
			    alert("Unexpected status code "+response.status
				  +": "+response.statusText);
			}
		    },
		    failCb: function(response) {
			console.log("failCb - response="+JSON.stringify(response));
			alert("failCb - response="+JSON.stringify(response));
			//self.profile={};
		    }
		});
	    },
	},
	mounted() {
	    console.log("Events.vue.mounted()");
	    this.getProfile();
	}
	
    };
</script>
		
		<style scoped>
</style>
