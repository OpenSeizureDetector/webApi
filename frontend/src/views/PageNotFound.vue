<template>
  <div class="PageNotFound">
    <h1>Page Not Found</h1>
    <p> URL: {{ url }}</p>
  </div>
</template>
<script>
import router from '../router';
export default {
    name: 'Login',
    data() { return {
	url: window.location.pathname,
	urlText: "test text"
    }
	   }
}

</script>
