<template>
    <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
	    <h1>User Profile</h1>

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
		v-model="password"  :rules="passwordRules">
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
export default {
    name: 'Profile',
    data() { return {
	valid: false,
	uname: '',
        password: '',
        passwordRules: [
            v => !!v || 'Password is required',
            v =>
                v.length >= 6 ||
                'Password must be greater than 6 characters'
        ],
    };
	   },
    methods: {
	submit() {
            if (this.$refs.form.validate()) {
		console.log("submit() - FIXME - this doesn't do anything");
            }
	}
    }
};
</script>

<style scoped>
</style>
