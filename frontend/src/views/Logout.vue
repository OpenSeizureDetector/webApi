<template>
<div id="logout_text">
<h1 v-if="isAuthenticated">Still Logged in - why???</h1>
<h1 v-if="!isAuthenticated">Logged Out Successfully</h1>
</div>
</template>
	  
<script>
import router from '../router';
export default {
    name: 'Logout',
    data() {
	   },
    created() {
      console.log('created called.');
      this.$store.dispatch('logout', {
		});
    },
    computed:{ 
    	       isAuthenticated(){
	       console.log("Logout.computed.isAuthenticated()");
	       return this.$store.getters['isAuthenticated']
	       } 
	},
    methods: {
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
