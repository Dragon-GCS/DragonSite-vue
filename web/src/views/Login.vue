<template>
  <div class="login-form-box">
    <el-form ref="ruleFormRef" :model="ruleForm" label-width="auto" label-position="top" :hide-required-asterisk="true">
      <el-form-item label="用户名" prop="name" required :inline-message="false">
        <el-input v-model="ruleForm.name" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码" prop="password" required>
        <el-input v-model="ruleForm.password" placeholder="请输入密码" :show-password="true" />
      </el-form-item>
      <el-form-item>
        <div class="login-button">
          <el-button type="primary" @click="onSubmit">登录</el-button>
          <el-button :disabled="true">注册</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance } from 'element-plus'

const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive({
  name: '',
  password: '',
})

const onSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!', fields)
    }
  })
}
</script>

<style>
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