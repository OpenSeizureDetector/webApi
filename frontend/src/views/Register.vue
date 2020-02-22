<template>
<v-card>
  <v-card-title>
    <h1>Create Account to Use OpenSeizureDetector WebAPI</h1>
  </v-card-title>
  <v-card-text>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-text-field
	name="uname"
	label="User Name:" 
        v-model="uname" required>
      </v-text-field>
      <v-text-field
	name="firstname"
	label="First Name:" 
        v-model="firstname" required>
      </v-text-field>
      <v-text-field
	name="lastname"
	label="Last Name:" 
        v-model="lastname" required>
      </v-text-field>
      <v-text-field
        v-model="email"
        :rules="emailRules"
        label="E-mail"
        required
        ></v-text-field>
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
    <v-btn color="primary" @click="submit">Create Account</v-btn>
  </v-card-actions>
</v-card>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Register',
    data() { return {
	valid: false,
	uname: '',
	firstname: '',
	lastname: '',
	email: '',
        password: '',
        confirmpassword: '',
	emailRules: [
	    v => !!v || 'E-mail is required',
	    v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
        ],
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
	    console.log("Register.submit()");
            if (this.$refs.form.validate()) {
		// Register a new user
		var data = {
		    "username": this.uname,
		    "first_name": this.firstname,
		    "last_name": this.lastname,
		    "email": this.email,
		    "password": this.password,
		    "password_confirm": this.confirmpassword
		};
		console.log("register: data = "+JSON.stringify(data));
		let url = this.$store.state.baseUrl
		console.log("....url="+url);
		axios(
		    {
			method: 'post',
			url: url+'/api/accounts/register/',
			data: data,
			validateStatus: function(status) {
			    return status<500;
			},
		    }
		)
		    .then(response => {
			if (response.status == 201) {
			    console.log(response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			    alert("User created successfully - you will receive a confirmation email in a few minutes"); 
			    console.log("redirecting to login page");
			    router.push({ path: '/login/' });
			} else {
			    console.log(response.status +
					" - " + response.statusText +
					" : " +JSON.stringify(response.data));
			    var errMsg = "Problem Creating User: ";
			    for (const key in response.data) {
				errMsg = errMsg + ": "+key+" - "+response.data[key];
			    }
			    alert(errMsg+": Please Try Again");
    
			}
		    })
		    .catch((err) => {
			console.log("catch(): err="+JSON.stringify(err));
			//alert("error - "+JSON.stringify(err));
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
