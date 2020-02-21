<template>
<v-card>
  <v-card-title>
    <h1>Reset Password</h1>
  </v-card-title>
  <v-card-text>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
	name="password"
	label="Password"
        type="password"
	required
	v-model="password" :rules="passwordRules">
      </v-text-field>
      <v-text-field
	name="confirmpassword"
	label="Confrm Password"
        type="password"
	required
	v-model="confirmpassword" :rules="passwordRules">
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
import router from '../router';
export default {
    name: 'ResetPassword',
    data() { return {
	valid: false,
        password: '',
        confirmpassword: '',
        passwordRules: [
            v => !!v || 'Password is required',
            v =>
                v.length >= 6 ||
                'Password must be greater than 6 characters'
        ]
    };
	   },
    methods: {
	submit() {
	    console.log("ResetPassword.submit()");
            if (this.$refs.form.validate()) {
		// Register a new user
		var data = {
		    user_id : this.$route.query.user_id,
		    timestamp : this.$route.query.timestamp,
		    signature : this.$route.query.signature,
    		    password: this.password,
		};
		console.log("resetPassword: data = "+JSON.stringify(data));
		let url = this.$store.state.baseUrl
		console.log("....url="+url);
		axios(
		    {
			method: 'post',
			url: url+'/api/accounts/reset-password/',
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
			    alert("Password Reset successfully - please Login"); 
			    console.log("redirecting to login page");
			    router.push({ path: '/login/' });
			} else {
			    console.log(response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			    alert("Unexpected Response: "+response.status +
				  " - " + response.statusText +
				  " : " +JSON.stringify(response.data));
			}
		    })
		    .catch((err) => {
			console.log("catch(): err="+JSON.stringify(err));
		    });
	    } else {
		console.log("Register.submit() - validation failed");
		alert("Form Validation Failed - Please check form");
	    }
        } 
    }	
};
</script>

<style scoped>
</style>
