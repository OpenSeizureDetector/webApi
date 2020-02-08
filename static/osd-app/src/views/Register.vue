<template>
    <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex xs24 sm16 md8>
	    <h1>Create Account to Use OpenSeizureDetector WebAPI</h1>

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
              <v-text-field
		name="confirmpassword"
		label="Confrm Password"
		id="confirmpassword"
                type="password"
		required
		v-model="confirmpassword" :rules="passwordRules">
              </v-text-field>
	      <v-btn color="primary" @click="submit">Create Account</v-btn>
            </v-form>
	    
            </v-flex>
        </v-layout>
    </v-container>
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
		//this.$store.dispatch('login', {
                //    uname: this.uname,
                //    password: this.password
		//});
		console.log("FIXME - register button does not work!");
            }
	}
    }
};
</script>

<style scoped>
</style>
