/*axios.interceptors.response.use(response => response, error => {
    if(error.response.status === 401) {
	console.log("Interceptor caught 401");
    }
    return error;
});
*/

// vuejs
// appState values:
//  0 : not logged in
//  1 : display wearers
//  2 : list data
//  3 : add wearer
//  4 : edit wearer
//
var app = new Vue({
    el: '#vueApp',
    data: {
	APPSTATE_NOT_LOGGED_IN: 0,
	APPSTATE_DISPLAY_WEARERS: 1,
	APPSTATE_LIST_DATA: 2,
	APPSTATE_ADD_WEARER: 3,
	APPSTATE_EDIT_WEARER: 4,
	appState: 0,
	isLoggedIn: 0,
	token: '',
	message: 'Hello Vue from vueApp.js!',
	ajaxMsg: 'ajax messages appear here',
	wearers: [],
	uname: 'user',
	passwd: 'user_pw',
	confirm_passwd:'confirm password',
	email: 'email',
    },
    methods: {
	validateStatus: function (status) {
	    return status < 500;
	},
	loginBtnOnClick: function() {
	    this.message = "Button Clicked - uname="+
		this.uname+", passwd="+this.passwd;
	    axios(
		{
		    method: 'post',
		    url:'/accounts/login/',
		    data: {
			login: this.uname,
			password: this.passwd,
		    },
		    validateStatus: this.validateStatus,
		}
	    )
		.then(response => {
		    //console.log(JSON.stringify(response));
		    this.ajaxMsg = response.status +
			" - " + response.statusText +
			" : " +JSON.stringify(response.data);
		    this.message = response.statusText + " : "
			+ response.data['detail'];
		    if (response.status == 200) {
			this.isLoggedIn = 1;
			this.token = response.data['token'];
			this.appState = this.APPSTATE_LIST_WEARERS;
		    } else {
			this.isLoggedIn = 0;
			this.appState = this.APPSTATE_NOT_LOGGED_IN;
		    }
		    //this.getWearers();		    
		})
		.catch(function (error) {
		    console.log(error);
		    this.message = error;
		    this.appState = this.APPSTATE_NOT_LOGGED_IN;
		});

	},
	registerBtnOnClick: function() {
	    this.message = "Button Clicked - uname="+
		this.uname+", passwd="+this.passwd;
	    axios({
		method: 'POST',
		url: '/accounts/register/',
		data: {
		    username: this.uname,
		    password: this.passwd,
		    email:this.email,
		    password_confirm: this.confirm_passwd,
		},
		validateStatus: this.validateStatus,
	    })
		.then(response => {
		    //console.log(JSON.stringify(response));
		    this.ajaxMsg = response.status +
			" - " + response.statusText +
			" : " +JSON.stringify(response.data);
		    this.isLoggedIn = 1;
		    //this.appState = this.APPSTATE_LIST_WEARERS;
		    //this.getWearers();		    
		})
		.catch(function (error) {
		    console.log(error);
		    this.wearers = [];
		    this.message = error;
		    this.appState = this.APPSTATE_NOT_LOGGED_IN;
		    console.log("error!");
		});
	},
	logoutBtnOnClick: function() {
	    this.message = "Logout Button Clicked";
	    headersObj = {
		"Authorization": "Token " + this.token,
	    };
	    console.log(JSON.stringify(headersObj));
	    axios(
		{
		    method: 'POST',
		    url:'/accounts/logout/',
		    headers: headersObj,
		    data: {
			revoke_token: true,
		    },
		    validateStatus: this.validateStatus,
		}
	    )
		.then(response => {
		    //console.log(JSON.stringify(response));
		    this.ajaxMsg = response.status +
			" - " + response.statusText +
			" : " +JSON.stringify(response);
		    this.message = response.statusText + " : "
			+ response.data['detail'];
		    if (response.status == 200) {
			this.isLoggedIn = 0;
			this.appState = this.APPSTATE_LIST_WEARERS;
		    } else {
			this.isLoggedIn = 0;
			this.appState = this.APPSTATE_NOT_LOGGED_IN;
		    }
		    //this.getWearers();		    
		})
		.catch(function (error) {
		    console.log(error);
		    this.message = error;
		    this.appState = this.APPSTATE_NOT_LOGGED_IN;
		});
	},
	getWearers: function() {
	    // Retrieve a list of the wearers associated with the current
	    // logged in user.
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
		    console.log(JSON.stringify(response));
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
