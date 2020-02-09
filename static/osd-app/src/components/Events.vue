<template>
    <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
	    <h1>Events</h1>

            <v-form ref="form" v-model="valid" lazy-validation>
            </v-form>
	    
          </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
export default {
    name: 'Events',
    data() { return {
	valid: false,
    };
	   },
    methods: {
	getEvents() {
            if (this.$refs.form.validate()) {
		console.log("getEvents() - FIXME - this doesn't do anything");
            }
	}
    }
};
</script>

<style scoped>
</style>
