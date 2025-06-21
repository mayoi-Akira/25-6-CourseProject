<!-- src/App.vue -->
<template>
  <div id="app">
    <!-- 使用选项式 API 注册的 NavBar 组件 -->
    <div class="common-layout">
      <el-container class="app-container w-full">
        <el-header v-if="!$route.meta.hide" class="header">
          <NavBar />
        </el-header>
        <el-main v-if="!$route.meta.hide"><router-view /></el-main>
        <router-view v-else></router-view>
      </el-container>
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',

  // 1. 在 components 中注册子组件
  components: {
    NavBar
  },

  // （可选）2. 如果未来需要全局状态、计算属性或方法，都写在这里
  data() {
    return {
      // 比如可以在这里声明一些响应式数据
      // message: 'Hello Vue!'
    }
  },
  computed: {
    // 比如根据路由 meta 控制布局显示
    // hideLayout() {
    //   return this.$route.meta.hideLayout
    // }
  },
  methods: {
    // 如果需要在根组件中处理事件，也写在这里
    // someMethod() { … }
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
}

.header {
  height: 60px;
  /* 或 10vh，建议用px */
  width: 100%;
}
</style>
