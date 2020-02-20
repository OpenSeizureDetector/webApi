import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store';
//import Home from '../views/Home.vue';
import Events from '../views/Events.vue';
import About from '../views/About.vue';
import Login from '../views/Login.vue';
import Logout from '../views/Logout.vue';
import Register from '../views/Register.vue';
import RegisterConfirm from '../views/RegisterConfirm.vue';
import RequestPasswordReset from '../views/RequestPasswordReset.vue';
import ResetPassword from '../views/ResetPassword.vue';
//import RequestChangeEmail from '../views/RequestChangeEmail.vue';
//import ChangeEmailConfirm from '../views/ChangeEmailConfirm.vue';
import PageNotFound from '../views/PageNotFound.vue';
import Profile from '../views/Profile.vue';

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
	path: '/logout/',
	name: 'logout',
	component: Logout,
	meta: { 'auth': true }
    },
    {
	path: '/register/',
	name: 'register',
	component: Register,
	meta: { 'auth': false }
    },
    {
	path: '/confirm/',
	name: 'registerconfirm',
	component: RegisterConfirm,
	meta: { 'auth': false }
    },
    {
	path: '/request-password-reset/',
	name: 'request-password-reset',
	component: RequestPasswordReset,
	meta: { 'auth': false }
    },
    {
	path: '/reset-password/',
	name: 'reset-password',
	component: ResetPassword,
	meta: { 'auth': false }
    },
/*    {
	path: '/request-change-email/',
	name: 'request-change-email',
	component: RequestChangeEmail,
	meta: { 'auth': true }
    },
    {
	path: '/change-email-confirm/',
	name: 'change-email-confirm',
	component: ChangeEmailConfirm,
	meta: { 'auth': false }
    },
*/
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
