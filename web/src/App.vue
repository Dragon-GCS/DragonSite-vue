<template>
  <el-container>
    <el-header>
      <Header />
    </el-header>
    <el-container>
      <side-menu />
      <Suspense>
        <el-main>
          <router-view :key="$route.fullPath" v-slot="{ Component }">
            <component :is="Component" />
          </router-view>
        </el-main>
      </Suspense>
    </el-container>
  </el-container>
</template>

<setup lang="ts">
</setup>

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
