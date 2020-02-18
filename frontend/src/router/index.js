import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store';
//import Home from '../views/Home.vue';
import Events from '../views/Events.vue';
import About from '../views/About.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import PageNotFound from '../views/PageNotFound.vue';
import Profile from '../components/Profile.vue';

Vue.use(VueRouter);

const routes = [
    {
	path: '/',
	alias: ['/home/', '/static/dist/', '/events/'],
	name: 'home',
	component: Events,
	meta: { 'auth': true }
    },
    {
	path: '/login/',
	name: 'login',
	component: Login,
	meta: { 'auth': false }
    },
    {
	path: '/register/',
	name: 'register',
	component: Register,
	meta: { 'auth': false }
    },
    {
	path: '/profile/',
	name: 'profile',
	component: Profile,
	meta: { 'auth': true }
    },
    {
	path: '/about/',
	name: 'about',
	component: About,
	meta: { 'auth': false }
    },
    {
	path: '*',
	name: 'pagenotfound',
	component: PageNotFound,
	meta: { 'auth': false }
    }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
    //console.log("router.beforeEach - to="+JSON.stringify(to));
    if (to.meta.auth) {
	console.log("router.beforeach - to.meta.auth is true...");
	if (! store.getters['isAuthenticated']) {
	    console.log("router.beforeEach - redirecting to login screen");
	    next({ name: 'login' });
	} else {
	    console.log("router.beforeEach - we are authenticated so continuing to page");
	    next(); 
	}
    } else {
	console.log("router.beforeEach - meta.auth is false - continuing to page");
	next();
    }
});

export default router;
