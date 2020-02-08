<template>
  <span>
    <v-app-bar app color="brown darken4" dark>
			<v-toolbar-title>{{appTitle}}</v-toolbar-title>
			<v-btn text to="/About">About</v-btn>
			<v-spacer></v-spacer>
			<v-btn v-if="!isAuthenticated" text to="/Login">Login/Register</v-btn>
			<v-btn v-if="isAuthenticated" text to="/profile">Account</v-btn>

    </v-app-bar>
    <v-navigation-drawer
      app v-model="drawer"
      class="brown lighten-2"
      dark disable-resize-watcher>
      <v-list>
	<template v-for="(item, index) in items">
	    <v-list-item>
	      {{item.title}}
	    </v-list-item>
	  <v-divider :key="`divider-${index}`"></v-divider>
	</template>
      </v-list>
    </v-navigation-drawer>
  </span>
</template>

    <script>
    export default {
	name: 'AppNavigation',
	data() {
	    return {
		appTitle: 'OpenSeizureDetector WebAPI',
		drawer: false,
		items: [
		    { title: 'drawer-btn1'},
		    { title: 'drawer-Log In'}
		]};
	},
	computed:{ 
	    isAuthenticated(){return this.$store.getters['isAuthenticated']} 
	},
    };
</script>

    <style scoped>
    </style>
