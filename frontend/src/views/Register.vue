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
export default {
    name: 'Register',
    data() { return {
	valid: false,
	uname: '',
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
            if (this.$refs.form.validate()) {
	// Register a new user
	   	    console.log("register("+uname+","+password+")");
	    let url = context.state.baseUrl;
	    console.log("....url="+url);
	    axios(
		{
		    method: 'post',
		    url: url+'/api/accounts/login/',
		    data: {
			login: uname,
			password: password,
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
			context.commit('setToken', response.data['token']);
			context.commit('setIsAuthenticated', true);
			console.log("redirecting to events page");
			router.push({ path: '/events/' });
		    } else {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
			context.commit('setToken', null);
			context.commit('setIsAuthenticated', false);
		    }
		})
		.catch((err) => {
		    console.log("catch(): err="+JSON.stringify(err));
		    context.commit('setToken', null);
		    context.commit('setIsAuthenticated', false);
		});
	}
			alert("FIXME - register button does not work!");
				console.log("FIXME - register button does not work!");
            }
	}
    };
</script>

<style scoped>
</style>
