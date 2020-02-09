<template>
<v-container fill-height>
  <v-layout align-center justify-center>
    <v-flex xs12 sm8 md4>
      <h1>Home Page</h1>
      <events></events>
    </v-flex>
  </v-layout>
</v-container>

</template>

<script>
import Events from '@/components/Events.vue'

console.log("Home.vue");

export default {
  name: 'home',
  components: {
      Events,
  }
}
</script>
