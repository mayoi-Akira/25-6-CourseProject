<template>
  <div class="clock">{{ time }}</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Clock',
  data() {
    return {
      time: '' as string,
      timerId: null as number | null
    };
  },
  methods: {
    updateTime() {
      const now = new Date();
      this.time = now.toLocaleTimeString('zh-CN', { hour12: false });
    }
  },
  mounted() {
    this.updateTime();
    // 每秒更新
    this.timerId = window.setInterval(this.updateTime, 1000);
  },
  beforeUnmount() {
    // 组件销毁时清除定时器
    if (this.timerId !== null) {
      clearInterval(this.timerId);
    }
  }
});
</script>

<style scoped>
.clock {
  font-size: 2rem;
  font-family: "consolas";
}
</style>
