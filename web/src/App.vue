<script setup lang="ts">
import { siteName } from './config';
document.title = siteName
</script>

<template>
  <el-container class="main-con">
    <el-header>
      <Header :site-name="siteName"></Header>
    </el-header>
    <el-container>
      <side-menu/>
      <el-main>
        <router-view :key="$route.fullPath"></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>


<style>
.main-con {
  height: 100%;
  flex-direction: column;
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
