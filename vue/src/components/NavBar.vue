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
      <a href="https://www.luogu.com.cn/user/1626844" target="_blank"><img src="../assets/luogu.png" width="50"
          height="50" class="link-img"></a>
      <a href="https://codeforces.com/profile/mayoi_Akira" target="_blank"><img src="../assets/codeforces.png"
          width="37" height="45" class="link-img"></a>
      <a href="https://ac.nowcoder.com/acm/contest/profile/588125209" target="_blank"><img src="../assets/nowcoder.png"
          width="90" height="40" class="link-img"></a>
    </div>
    <el-menu-item index="2"><img src="../assets/home.png" width="20" height="20">&nbsp;主页</el-menu-item>
    <el-menu-item index="3">数据集管理</el-menu-item>
    <el-menu-item index="4">模型训练</el-menu-item>
    <el-menu-item index="5">预测</el-menu-item>
    <el-sub-menu index="6">
      <template #title>
        <img src="../assets/user_img.jpg" height="45" width="45" class="user_img" />
      </template>
      <el-menu-item index="6-1"><img src="../assets/user_img.jpg" height="20" width="20" class="user_img" />
        &nbsp;&nbsp;{{ user.name }}</el-menu-item>
      <el-menu-item index="6-1">个人主页</el-menu-item>
      <el-menu-item index="6-2">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NavMenu',
  inject: ['user'],
  data() {
    return {
      activeIndex: '1',
      back_end: "http://127.0.0.1:5000",
      // back_end: "https://frp-boy.com:12771",
    }
  },
  methods: {
    handleSelect(key: string, keyPath: string[]) {
      console.log(key)
      if (key == '2')
        this.$router.push({ name: 'home' })
      else if (key === '3')
        this.$router.push({ name: 'dataset' })
      else if (key == '4')
        this.$router.push({ name: 'model' })
      else if (key == '5')
        this.$router.push({ name: 'predict' })
      else if (keyPath[1] === '6-2') {
        this.cancel()
        this.$router.replace({ name: 'login' })
      }
    },
    async fetchData() {
      try {
        const response = await fetch(`${this.back_end}/name`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ op: 'get' }),
        })
        if (response.ok) {
          const data = await response.json()
          if (data.id == 0 && this.$route.name != 'login') {
            this.$message.error("未登录")
            this.$router.replace({ name: 'login' })
            return
          }
          this.user.name = data.name
          this.user.role = data.role
        } else {
          throw new Error(`${response.status}`)
        }
      } catch (err) {
        this.$message.error(`网络错误 ${err}`)
        this.$router.replace({ name: 'login' })
      }

    },
    async cancel() {
      try {
        const response = await fetch(`${this.back_end}/name`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ op: 'cancel' }),
        })
        if (response.ok) {
          return
        } else {
          throw new Error(`${response.status}`)
        }
      } catch (err) {
        this.$message.error(`网络错误 ${err}`)

      }
    }
  },
  mounted() {
    this.fetchData()
    // console.log(this.role)
  },
  // watch: {
  //   '$route.fullPath'() {
  //     this.fetchData()
  //   }
  // }


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
