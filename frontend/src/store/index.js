import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import router from '../router';

Vue.use(Vuex);

export default new Vuex.Store({
//export const store = new Vuex.Store({
    state: {
	baseUrl: "https://api.osd.dynu.net",
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
			context.commit('setToken', null);
			context.commit('setIsAuthenticated', false);
		    }
		})
		.catch((err) => {
		    console.log("catch(): err="+JSON.stringify(err));
		    context.commit('setToken', null);
		    context.commit('setIsAuthenticated', false);
		});
	},
	logout: function(context) {
	    console.log("logout");
	    context.commit('setToken', null);
	    context.commit('setIsAuthenticated', false);
	},
	getUserDetails(context) {
	    console.log("getUserDetails");
	},
    },
    modules: {
    }
}
			     );
