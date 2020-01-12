<template>
<div id="app">
  <Navigation />
  <Main />
</div>
</template>

<script>
import Navigation from './components/Navigation'
import Main from './components/Main'

export default {
  name: 'app',
  components: { Navigation, Main }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}
</style>
