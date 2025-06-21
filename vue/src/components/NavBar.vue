<template>
  <el-menu class="my-menu" v-if="!$route.meta.hide" :default-active="activeIndex" mode="horizontal" :ellipsis="false"
    @select="handleSelect" text-color="#000000" active-text-color="#000000">
    <div class="link">
      <a href="https://github.com/mayoi-Akira" target="_blank"><img src="../assets/github.png" width="37" height="37"
          class="link-img"></a>
      <a href="https://space.bilibili.com/513574247" target="_blank"><img src="../assets/bilibili.png" width="50"
          height="50" class="link-img"></a>
      <a href="https://gitee.com/mayoi_Akira" target="_blank"><img src="../assets/gittee.png" width="35" height="35"
          class="link-img"></a>
    </div>
    <el-menu-item index="2">主页</el-menu-item>
    <el-menu-item index="3">数据集上传</el-menu-item>
    <el-menu-item index="4">模型训练</el-menu-item>
    <el-menu-item index="5">预测</el-menu-item>
    <el-sub-menu index="6">
      <template #title>
        <img src="../assets/user_img.jpg" height="45" width="45" class="user_img" />
      </template>
      <el-menu-item index="6-1">个人主页</el-menu-item>
      <el-menu-item index="6-2">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NavMenu',

  // 1. data(): 用来声明响应式数据
  data() {
    return {
      activeIndex: '1',
    }
  },

  // 2. methods: 定义所有模板中会调用的函数
  methods: {
    handleSelect(key: string, keyPath: string[]) {
      console.log(key)
      // 当用户点击“注销”时（keyPath[1] === '2-2'）
      if (key == '2') {
        this.$router.push({ name: 'home' })
      }
      else if (keyPath[1] === '6-2') {
        this.$router.push({ name: 'login' })
      }
    }
  },
})
</script>

<style scoped>
.el-menu {
  /* 建议用 width:100%，父容器控制宽度 */
  height: 70px;
  width: 102.35%;
  margin-left: -20px;
  display: flex;
  justify-content: space-between;
  /* background-color: #FB7299; */
  background: linear-gradient(315deg, #FB7299, #EAE1E7);
}

::v-deep .appmenu .el-menu-item:hover,
::v-deep .appmenu .el-sub-menu__title:hover {
  color: #66bb6a;
}

.el-menu-item {
  font-size: 1.2rem;
}

.link {
  display: flex;
  align-items: center
}

.link-img {
  border: 1.5px solid #cccccc00;
  border-radius: 50rem;
}

.el-menu--horizontal>div {
  margin-top: 0.4%;
  margin-left: 4%;
}

.el-menu--horizontal>div>a {
  padding-right: 4px;
  padding-left: 4px;
}

.el-menu--horizontal>.el-menu-item:nth-child(2) {
  padding-right: 8px;
  padding-left: 8px;
  margin-left: auto;
}


.user_img {
  border-radius: 50rem;
}
</style>
