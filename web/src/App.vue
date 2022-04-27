<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
</script>

<template>
  <el-container class="main-con">
    <Header site-name="DragonSite"></Header>
    <el-container>
      <side-menu/>
      <Main></Main>
    </el-container>
  </el-container>
</template>


<style>
.main-con {
  height: 100%;
  flex-direction: column;
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
