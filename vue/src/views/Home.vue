<script lang="ts">
import myClock from '../components/myClock.vue'
export default {
  name: 'Home',
  inject: ['user'],
  components: { myClock },
  data() {
    return {
      poem: {
        first: "问君能有几多愁",
        second: "恰似一江春水向东流",
      },
      time: Date.now()
    }
  },
  methods: {

  },

}
</script>

<template>
  <div class="welcome">
    <div style="width:auto; height:auto; margin-top: 2%;">
      <i>欢迎 {{ user.name }} ~</i>
    </div>
    <div class="time-container">
      <el-icon style="margin-top: 5%;margin-right: 2%;">
        <Clock />
      </el-icon>
      <myClock />
    </div>
    <div class="poem">
      <p class="poem-1">
        {{ this.poem.first }}
      </p>
      <p class="poem-2">
        {{ this.poem.second }}
      </p>
    </div>
    <el-button class="my-el-button" size="large">
      <el-icon>
        <Refresh />
      </el-icon></el-button>
  </div>

  <div class="videos">
    <div class="video-recon">
      <h3>视频推荐：</h3>
    </div>
    <iframe src="//player.bilibili.com/player.html?isOutside=true&bvid=BV11H4y1F7uH&p=1" scrolling="no" frameborder="no"
      framespacing="0" allowfullscreen="true"></iframe>
  </div>
</template>

<style scoped>
.welcome {
  background-color: #ffffff;
  width: 100%;
  height: 15%;
  border-radius: 1.6rem;
  box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.2);
  padding-left: 7%;
  /* padding-top: 2%; */
  font-size: 2vw;
  display: flex;
}

.my-el-button {
  margin-top: 2%;
  background-color: #EFF2F5;
}

.time-container {
  /* background-color: black; */
  display: flex;
  position: absolute;
  top: 16%;
  left: 47%;
  /* 因为 top/left 指的是子元素左上角，所以用 translate 抵消一半自身宽高 */
  transform: translate(-50%, -50%);
}

.poem {
  /* background-color: black; */
  /* padding-bottom: 2%; */
  margin-left: 43%;
  font-family: '仿宋';
  height: 100%;
  margin-bottom: 10%;
  padding-left: 2%;
  padding-right: 2%;
  width: auto;
  height: 100%;
  border: 2px solid #ccc;
  border-radius: 1.3rem;
  display: inline-block;
  flex-direction: column;
  background-color: #EFF2F5;
}

.poem-1 {
  line-height: 1.5;
}

.poem-2 {
  text-indent: 4vw;
}


.video-recon {
  font-size: 1.5rem;
  width: auto;
  height: auto;
  border-radius: 1.0rem;
  padding-left: 2%;
  /* background-color: #a1eefa; */
}

.videos {
  width: 55%;
  margin-left: 45%;
  margin-top: 1%;
  height: 80%;
  padding-top: 1%;
  padding-left: 1%;
  padding-bottom: 2%;
  background-color: #ffffff;
  border-radius: 1.6rem;
  box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.2);
}


.videos>iframe {
  background-color: #F0B9CB;
  width: 95%;
  height: auto;
  margin-top: 2%;
  margin-left: 2%;
  aspect-ratio: 16/9;
  border-radius: 1.3rem;
  border-left: 8px solid #ccc;
  border-right: 8px solid #ccc;
  border-top: 5px solid #ccc;
  border-bottom: 5px solid #ccc;
}

.videos>div>a {
  color: black;
  /* background-color: ; */
  /* margin-left: 5%; */

  font-size: 1.5rem;
}
</style>
