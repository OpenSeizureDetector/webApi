import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import router from '../router';

Vue.use(Vuex);

export default new Vuex.Store({
    //export const store = new Vuex.Store({
    state: {
	baseUrl: "https://osdapi.ddns.net",
	isAuthenticated: false,
	token: null
    },
    getters: {
	baseUrl(state) {
	    return state.baseUrl;
	},
	token(state) {
	    return state.token;
	},
	isAuthenticated(state) {
	    console.log("getters.isAuthenticated: "+state.isAuthenticated);
	    return state.isAuthenticated;
	}
    },
    mutations: {
	setToken(state, payload) {
	    state.token = payload;
	    console.log("store.mutations.setToken - token = "+state.token);
	},
	setIsAuthenticated(state, payload) {
	    state.isAuthenticated = payload;
	    console.log("setIsAuthenticated: "+state.isAuthenticated);
	}
    },
    actions: {
	// Obtain an access token using the uname and password credentials.
	login(context, { uname, password }) {
	    console.log("login("+uname+","+password+")");
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
			alert(JSON.stringify(response.data));
			context.commit('setToken', null);
			context.commit('setIsAuthenticated', false);
		    }
		})
		.catch((err) => {
		    console.log("catch(): err="+JSON.stringify(err));
		    alert(JSON.stringify(err));
		    context.commit('setToken', null);
		    context.commit('setIsAuthenticated', false);
		});
	},
	logout: function(context) {
	    console.log("logout");
	    context.commit('setToken', null);
	    context.commit('setIsAuthenticated', false);
	},
	authRequest: function(context, payload) {
	    var url = payload['url'];
	    var action = payload['action'];
	    var data = payload['data'];
	    var successCb = payload['successCb'];
	    var failCb = payload['failCb'];
	    var headers = { Authorization: `Token `+context.state.token }
	    console.log("store.authRequest: url="+url+", action="+action
			+", data="+JSON.stringify(data)
			+", headers="+JSON.stringify(headers)
		       );
	    axios(
		{
		    method: action,
		    url: url,
		    headers: headers,
		    data: data,
		    validateStatus: function(status) {
			return status<500;
		    },
		}
	    )
		.then(response => {
		    console.log("store.authRequest- response="+JSON.stringify(response));
		    successCb(response);
		})
		.catch((err) => {
		    console.log("store.authRequest.catch(): err="+JSON.stringify(err));
		    failCb(err)
		});
	},
	getUserDetails(context) {
	    console.log("getUserDetails");
	},
    },
    modules: {
    }
});


