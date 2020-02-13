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
		//this.$store.dispatch('login', {
                //    uname: this.uname,
                //    password: this.password
		//});
		alert("FIXME - register button does not work!");
		console.log("FIXME - register button does not work!");
            }
	}
    }
};
</script>

<style scoped>
</style>
