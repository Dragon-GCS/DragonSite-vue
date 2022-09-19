<template>
  <el-container>
    <el-header>
      <Header :site-name="siteName"></Header>
    </el-header>
    <el-container>
      <side-menu />
      <el-main>
        <router-view :key="$route.fullPath"></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import axios from 'axios';
import qs from "qs"
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import { siteName, loginState } from './config';
document.title = siteName

const router = useRouter()
axios.defaults.paramsSerializer = (params) => {
  return qs.stringify(params, { indices: false })
}

// 添加响应拦截器
axios.interceptors.response.use((response) => {
  // 对响应数据做点什么
  console.log("response", response)
  return response;
}, (error) => {
  // 对响应错误做点什么
  if (error.response.status === 401) {
    ElMessage.info(error.response.data.detail)
    loginState.value = false
    router.push({
      name: 'login',
      query: {
        redirect: router.currentRoute.value.fullPath
      }
    })
  }
  if (error.response.status === 400) {
    ElMessage.info(error.response.data.detail)
    loginState.value = false
  }
  if (error.response.status === 422) {
    console.log(error.response.data.detail)
  }
  return error
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

.el-container {
  height: 100%;
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e6e6e6;
}

a {
  text-decoration: none;
}

a.router-link-active {
  text-decoration: none;
  color: #409EFF;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
