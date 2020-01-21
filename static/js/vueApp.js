axios.interceptors.response.use(response => response, error => {
    if(error.response.status === 401) {
	console.log("Interceptor caught 401");
    }
    return error;
});

// vuejs
var app = new Vue({
    el: '#vueApp',
    data: {
	isLoggedIn: 0,
	message: 'Hello Vue from vueApp.js!',
	ajaxMsg: 'ajax messages appear here',
	wearers: [],
	uname: 'null',
	passwd: 'null'
    },
    methods: {
	loginBtnOnClick: function() {
	    this.message = "Button Clicked - uname="+
		this.uname+", passwd="+this.passwd;
	    axios.get('api/users/authenticate.json',
		      {
			  headers: {
			      'X-Requested-With': 'XMLHttpRequest',
			      'Content-Type': 'application/json'
			  },
			  auth: {
			      username: this.uname,
			      password: this.passwd
			  },
		      }
		     )
		.then(response => {
		    this.ajaxMsg = response.status +
			" - " + response.statusText +
			" : " +response.data;
		    //this.wearers = response.data['wearers'];
		    this.isLoggedIn = 1;
		    this.getWearers();
		    
		})
		.catch(function (error) {
		    //console.log(error);
		    this.message = error;
		    this.ajaxMsg = error;
		    //this.ajaxMsg = response.status +
			//" - " + response.statusText +
			//" : " +response.data;
		    this.isLoggedIn = 0;
		})
		.finally(function () {
		    // always executed
		});
	},
	logoutBtnOnClick: function() {
	    this.message = "Logout Button Clicked";
	    this.uname = "";
	    this.passwd = "";
	    this.isLoggedIn = 0;
	},
	getWearers: function() {
	    this.message = "Button Clicked - uname="+
		this.uname+", passwd="+this.passwd;
	    axios.get('api/wearers.json',
		      {
			  headers: {
			      'X-Requested-With': 'XMLHttpRequest',
			      'Content-Type': 'application/json'
			  },
			  auth: {
			      username: this.uname,
			      password: this.passwd
			  },
		      }
		     )
		.then(response => {
		    this.ajaxMsg = response.status +
			" - " + response.statusText +
			" : " +response.data;
		    this.wearers = response.data['wearers'];
		    this.isLoggedIn = 1;
		    
		})
		.catch(function (error) {
		    console.log(error);
		    this.wearers = [];
		    this.message = error;
		})
		.finally(function () {
		    // always executed
		});
	},
	addWearerBtnOnClick: function() {
	    this.message = "AddWearerButton Clicked";
	},
	
    }
});
