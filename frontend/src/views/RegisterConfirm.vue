<template>
<div>
<h1 v-if="isConfirmed">Registration confirmed ok - Please Login</h1>
<h1 v-if="!isConfirmed">Confirmation Failed "{{ msg }}" :  please try again....</h1>
</div>
</template>
	  
<script>
import axios from 'axios';
import router from '../router';
export default {
    name: 'RegisterConfirm',
    data() { return {
       isConfirmed: false,
       msg : "",
	  } },
    created() {
      console.log('created called.');
      var self = this;
      var postData = {
        user_id : this.$route.query.user_id,
        timestamp : this.$route.query.timestamp,
        signature : this.$route.query.signature
	}

	    axios(
		{
		    method: 'post',
		    url: this.url+'/api/accounts/verify-registration/',
		    data: postData,
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
		        self.isConfirmed = true;
		    } else {
			console.log(response.status +
				    " - " + response.statusText +
				    " : " +JSON.stringify(response.data));
		        self.isConfirmed = false;
			self.msg = response.data.detail;
				    }
		})
		.catch((err) => {
		    console.log("catch(): err="+JSON.stringify(err));
		    self.isConfirmed = false;
		});
	},

    computed:{ 
	url () {
                return this.$store.state.baseUrl;
        },
	},
    methods: {
    }
};
</script>

<style scoped>
</style>


