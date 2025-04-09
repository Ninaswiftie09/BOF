<template>
  <div id="app">
    <LoginView />
  </div>
</template>

<script>
import LoginView from './components/login.vue';

export default {
  name: 'App',
  components: {
    LoginView,
  },
};
</script>

<style>
@import './assets/styles.css';
</style>



