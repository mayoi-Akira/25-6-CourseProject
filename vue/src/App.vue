<script lang="ts">
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      isRegister: false,
      regUsername: '',
      regPassword: '',
      regPasswordConfirm: '',
      regErrorMessage: '',
    }
  },
  methods: {
    async handleLogin() {
      this.errorMessage = ''
      try {
        const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password, role: 'user' }),
        })
        const data = await response.json()

        if (response.ok) {
          alert(`登录成功，欢迎 ${data.username || this.username}!`)
        } else {
          this.errorMessage = data.message
        }
      } catch (err) {
        console.error('登录请求出错:', err)
        this.errorMessage = '网络异常，请稍后重试'
      }
    },
    async handleRegister() {
      this.regErrorMessage = ''
      try {
        const response = await fetch('http://127.0.0.1:5000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.regUsername,
            password: this.regPassword,
            passwordConfirm: this.regPasswordConfirm,
            role: 'user',
          }),
        })
        const data = await response.json()

        if (response.ok) {
          alert('注册成功！请返回登录')
          this.isRegister = false
          this.username = this.regUsername
          this.password = ''
          this.regUsername = ''
          this.regPassword = ''
          this.regPasswordConfirm = ''
        } else {
          this.regErrorMessage = data.message
        }
      } catch (err) {
        console.error('注册请求出错:', err)
        this.regErrorMessage = '网络异常，请稍后重试'
      }
    },
  },
}
</script>

<template>
  <div class="login-container">
    <div class="tabs">
      <button :class="{ active: !isRegister }" @click="isRegister = false">登录</button>
      <button :class="{ active: isRegister }" @click="isRegister = true">注册</button>
    </div>

    <div v-if="!isRegister">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input id="username" v-model="username" type="text" placeholder="请输入用户名" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>
        <button type="submit">登录</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>

    <div v-else>
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="reg-username">用户名</label>
          <input
            id="reg-username"
            v-model="regUsername"
            type="text"
            placeholder="请输入用户名"
            required
          />
        </div>
        <div class="form-group">
          <label for="reg-password">密码</label>
          <input
            id="reg-password"
            v-model="regPassword"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>
        <div class="form-group">
          <label for="reg-password-confirm">确认密码</label>
          <input
            id="reg-password-confirm"
            v-model="regPasswordConfirm"
            type="password"
            placeholder="请再次输入密码"
            required
          />
        </div>
        <button type="submit">注册</button>
      </form>
      <p v-if="regErrorMessage" class="error">{{ regErrorMessage }}</p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  width: 300%;
  max-width: 40vw;
  margin: 20vh 20vh;
  padding: 4vh 3vw;
  border: 0.1vw solid #ccc;
  border-radius: 1vw;
  box-shadow: 0 0.5vh 1.5vh rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  font-size: 1.1vw;
}

.tabs {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3vh;
}
.tabs button {
  flex: 1;
  padding: 1.5vh 0;
  background: #f0f0f0;
  border: none;
  cursor: pointer;
  font-size: 1vw;
}
.tabs button.active {
  background: #f0768b;
  color: white;
}

h2 {
  text-align: center;
  margin-bottom: 3vh;
  font-size: 1.4vw;
}

.form-group {
  margin-bottom: 2vh;
}

label {
  display: block;
  margin-bottom: 1vh;
  font-size: 0.95vw;
}

input {
  width: 100%;
  padding: 1.2vh 1vw;
  box-sizing: border-box;
  border: 0.1vw solid #ccc;
  border-radius: 0.4vw;
  font-size: 1vw;
}

button {
  width: 100%;
  padding: 1.5vh;
  background-color: #f0768b;
  color: white;
  border: none;
  border-radius: 0.4vw;
  cursor: pointer;
  font-size: 1.1vw;
}

button:hover {
  background-color: pink;
}

.error {
  color: red;
  margin-top: 2vh;
  text-align: center;
  font-size: 1vw;
}
</style>
