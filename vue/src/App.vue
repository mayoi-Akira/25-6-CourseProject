<template>
  <div id="app">

    <el-container class="app-container w-full">
      <el-header v-if="!$route.meta.hide" class="header">
        <NavBar />
      </el-header>

      <el-main v-if="!$route.meta.hide"><router-view /></el-main>
      <router-view v-else></router-view>
    </el-container>

  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  },

  data() {
  },

  computed: {
  },
  methods: {
  }
}
</script>

<style>
html,
body,
#app {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  /* background-color: black; */
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

.common-layout {
  height: 100%;
  width: 100%;
}

.app-container {
  flex: 1;
  height: 100vh;
  width: 100vw;
  display: flex;
  /* background-color: black; */
  flex-direction: column;
  max-width: none;
}

.el-main {
  flex: 1 1 auto;
  overflow: auto;
  padding: 0;
  background-color: #EFF2F5;
}

.header {
  height: 60px;
  /* 或 10vh，建议用px */
  width: 99.8%;
}
</style>
