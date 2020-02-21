<template>
<v-card>
  <v-card-title>
    <h1>Password Reset</h1>
  </v-card-title>
  <v-card-text>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
	name="uname"
	label="User Name:" 
        v-model="uname" required>
      </v-text-field>
    </v-form>
  </v-card-text>
  <v-card-actions>
    <v-btn color="primary" @click="submit">Reset Password</v-btn>
  </v-card-actions>
</v-card>
</template>

<script>
import axios from 'axios';
export default {
    name: 'RequestPasswordReset',
    data() { return {
	valid: false,
	uname: ''
    };
	   },
    methods: {
	submit() {
	    console.log("RequestPasswordReset.submit()");
	    var data = {
		"login": this.uname,
    	    };
	    console.log("requestPasswordReset.submit(): data = "+JSON.stringify(data));
	    let url = this.$store.state.baseUrl
	    console.log("....url="+url);
	    axios(
		{
		    method: 'post',
		    url: url+'/api/accounts/send-reset-password-link/',
		    data: data,
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
			alert("Request Accepted - you will receive a confirmation email in a few minutes"); 
			console.log("redirecting to login page");
			router.push({ path: '/login/' });
		    } else {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
			console.log("Wrong Response Code: "+response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
		    }
		})
		.catch((err) => {
		    console.log("catch(): err="+JSON.stringify(err));
		    //alert("error - "+JSON.stringify(err));
		});
        } 
    }	
};
  </script>

<style scoped>
</style>
