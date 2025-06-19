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
  <div class="auth-wrapper">
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
</div>
</template>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>

<style scoped>
.auth-wrapper {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #d27376 0%, #ffffff 100%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  width: 90%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.85);
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.tabs {
  display: flex;
  margin-bottom: 1.5rem;
}
.tabs button {
  flex: 1;
  padding: 0.75rem;
  background: #f0f0f0;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}
.tabs button.active {
  background: #f0768b;
  color: white;
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
}

button[type="submit"] {
  width: 100%;
  padding: 0.75rem;
  background-color: #f0768b;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 1rem;
}

button[type="submit"]:hover {
  background-color: pink;
}

.error {
  color: red;
  margin-top: 0.5rem;
  text-align: center;
}
</style>
