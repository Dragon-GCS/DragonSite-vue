<template>
  <div class="login-form-box">
    <el-form ref="formRef" :model="form" label-width="auto" label-position="top" :hide-required-asterisk="true">
      <el-form-item label="用户名" prop="name" required :inline-message="false">
        <el-input v-model="form.name" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码" prop="password" required>
        <el-input v-model="form.password" placeholder="请输入密码" :show-password="true" />
      </el-form-item>
      <el-form-item>
        <div class="login-button">
          <el-button type="primary" @click="onSubmit(formRef)">登录</el-button>
          <el-button :disabled="true">注册</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import type { FormInstance } from 'element-plus'
import { login, logout } from '../api'
import { state } from '../states';

const router = useRouter()
if (state.token) { logout(); router.push('home') }

const formRef = ref<FormInstance>()
const form = reactive({
  name: '',
  password: '',
})
const onSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      await login(form.name, form.password)
      if (state.token) { router.push('home') }
      else { formEl.resetFields('password') }
    }
  })
}
</script>

<style scoped>
.login-form-box {
  height: 50vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-button {
  display: flex;
  justify-content: space-evenly;
  width: 100%;
}
</style>