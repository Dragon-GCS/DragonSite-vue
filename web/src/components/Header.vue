<template>
    <router-link to="/">
        <el-button :link="true">
            <h1>{{ siteName }}</h1>
        </el-button>
    </router-link>

    <router-link to="/login">
        <h1 v-if="state.token" style="cursor:pointer;">
            Welcome {{ state.username }}
        </h1>
        <el-button v-else auto-insert-space>登录</el-button>
    </router-link>
</template>

<script setup lang="ts">
import { siteName } from '../config'
import { state } from '../states'
</script>

<style scoped>
a:visited {
    color: #409eff;
}
</style>