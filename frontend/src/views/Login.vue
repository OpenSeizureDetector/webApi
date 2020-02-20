<template>
  <v-card>
    <v-card-title>
      <h1>Login</h1>
    </v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
	  prepend-icon="mdi-account-circle"
	  name="uname"
	  label="User Name:" 
          v-model="uname" required>
        </v-text-field>
        <v-text-field
	  prepend-icon="mdi-lock"
	  name="password"
	  label="Password"
          type="password"
	  required
	  v-model="password" :rules="passwordRules">
        </v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="success" @click="onRegister">Register
      </v-btn>
      
      <v-btn color="info"
	     @click="onLogin">Login</v-btn>
	     <br/>
	     <a href="/request-password-reset">Reset Password</a>
    </v-card-actions>
  </v-card>
</template>
	  
<script>
import router from '../router';
export default {
    name: 'Login',
    data() { return {
	valid: false,
	uname: '',
        password: '',
        passwordRules: [
            v => !!v || 'Password is required',
            v =>
                v.length >= 3 ||
                'Password must be greater than 3 characters'
        ]
    };
	   },
    methods: {
	onLogin() {
            if (this.$refs.form.validate()) {
		this.$store.dispatch('login', {
                    uname: this.uname,
                    password: this.password
		});
            }
	},
	onRegister() {
	    router.push({ path: '/register' });
	}

    }
};
</script>

<style scoped>
</style>


<!--
<template>
    <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
	    <h1>Login to OpenSeizureDetector WebAPI</h1>

            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
		name="uname"
		label="User Name:" 
                v-model="uname" required>
              </v-text-field>
              <v-text-field
		name="password"
		label="Password"
		id="password"
                type="password"
		required
		v-model="password" :rules="passwordRules">
              </v-text-field>
	      <v-btn color="primary" @click="submit">Login</v-btn>
            </v-form>
	    
	    <p>
	      Not Registered?
              <v-btn text to="/register">Create account</v-btn>
	    </p>
            </v-flex>
        </v-layout>
    </v-container>
</template>
-->
