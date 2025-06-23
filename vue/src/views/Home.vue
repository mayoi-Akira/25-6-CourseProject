<script lang="ts">
import { errorMessages } from 'vue/compiler-sfc'
import myClock from '../components/myClock.vue'
export default {
  name: 'Home',
  inject: ['user'],
  components: { myClock },
  data() {
    return {
      back_end: 'http://127.0.0.1:5000',
      poem: {
        first: "",
        second: "",
      },
      stati: {
        user_num: 0,
        model_num: 0,
        exp_num: 0,
        max_acc: 0.0,
        avg_acc: 0.0,
        train_time: 0,
      }
    }
  },
  methods: {
    async get_poem() {
      try {
        const response = await fetch(`${this.back_end}/poem`)
        if (!response.ok) {
          this.poem.first = "获取失败"
          this.poem.second = "获取失败"
          throw new Error(`诗句获取失败 ${response.status}`)
        }
        const data = await response.json()
        this.poem.first = data.first
        this.poem.second = data.second
      } catch (err) {
        console.error(err)
      }
    },
    async get_stati() {
      try {
        const response = await fetch(`${this.back_end}/stati`)
        const data = await response.json()
        if (!response.ok) {
          throw new Error(`${data.error},状态码:${response.status}`)
        }
        this.stati = data
      } catch (err) {
        alert(`数据获取错误: ${err}`)
      }
    }
  },
  mounted() {
    this.get_poem(),
      this.get_stati()
  },

}
</script>

<template>
  <!-- 最上方欢迎栏-->
  <div class="welcome">
    <div style="position:absolute;width:auto; height:auto; margin-top: 1.6%; left:5%;">
      <i>Hello, {{ user.name }} ~</i>
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
    <el-button class="my-el-button" size="large" @click="get_poem">
      <el-icon>
        <Refresh />
      </el-icon>换一换</el-button>
  </div>

  <div class="buttom">
    <!--左下的统计页-->
    <div class="stati">
      <div class="floor">
        <p>
        <div>
          <el-icon>
            <UserFilled />
          </el-icon>
          &nbsp;用户数量：
        </div>
        <div>{{ stati.user_num }}
        </div>
        </p>
        <p>
        <div>
          <el-icon>
            <Tools />
          </el-icon>
          &nbsp;实验次数：
        </div>
        <div>{{ stati.exp_num }}</div>
        </p>
      </div>
      <div class="floor">
        <p>
        <div>
          <div><el-icon>
              <Grid />
            </el-icon>&nbsp;模型数量：</div>
        </div>
        <div>{{ stati.model_num }}</div>
        </p>

        <p>
        <div><el-icon>
            <TrophyBase />
          </el-icon>&nbsp;测试集最佳准确率：</div>
        <div>{{ stati.max_acc }}</div>
        </p>
      </div>
      <div class="floor" style="margin-bottom: 0px;">
        <p>
        <div> <el-icon>
            <Opportunity />
          </el-icon>&nbsp;测试集平均准确率：</div>
        <div>{{ stati.avg_acc }}</div>
        </p>
        <p>
        <div><el-icon>
            <Timer />
          </el-icon>&nbsp;总训练时间：</div>
        <div>{{ stati.train_time }}</div>
        </p>
      </div>
    </div>

    <!--右下的视频-->
    <div class="videos">
      <div class="video-recon">
        <h3>视频推荐：</h3>
      </div>
      <iframe src="//player.bilibili.com/player.html?isOutside=true&bvid=BV11H4y1F7uH&p=1" scrolling="no"
        frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
    </div>
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
  position: relative;
}

.buttom {
  /* background-color: aqua; */
  display: flex;
  flex-direction: row;
  height: auto;
}

.stati {
  /* background-color: ; */
  width: 45%;
  /* height: 50%; */
  /* background-color: #ffffff; */
  /* box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.2); */
  margin-top: 1%;
  border-radius: 1.6rem;
  margin-right: 0;
  /* margin-left: ; */
  display: flex;
  flex-direction: column;
  /* margin-bottom: 1%; */

}

.floor {
  border-radius: 1.6rem;
  width: 100%;
  height: 22vh;
  display: flex;
  margin-bottom: 3%;
}

.floor>p {
  padding: 2%;
  font-size: 1.6vw;
  border-radius: 1.6rem;
  width: 48%;
  height: 100%;
  background-color: #ffffff;
  box-shadow: 0px 2px 8px 0px rgba(0, 0, 0, 0.2);
  margin-right: 2%;
}

.floor>p>:nth-child(2) {
  margin-top: 7%;
  text-align: center;
}

.time-container {
  /* background-color: black; */
  display: flex;
  position: absolute;
  top: 50%;
  left: 45%;
  transform: translate(-50%, -50%);
}

.poem {
  /* background-color: black; */
  /* padding-bottom: 2%; */
  position: absolute;
  right: 10%;
  font-family: '华文行楷';
  height: 100%;
  margin-bottom: 10%;
  padding-left: 2%;
  padding-right: 2%;
  width: auto;
  height: 100%;
  border: 1px solid #d2cfcf;
  border-radius: 1.3rem;
  display: inline-block;
  flex-direction: column;
  background-color: #ffffff;
}

.my-el-button {
  position: absolute;
  right: 4.3%;
  top: 30%;
  background-color: #ffffff;
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
  margin-left: 0%;
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
  background-color: black;
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
