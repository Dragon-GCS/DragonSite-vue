<template>
    <el-header height="50px">
        <el-button @click="goHome" type="text">
            <h1>{{ siteName }}</h1>
        </el-button>
        <el-button @click="login" auto-insert-space>登录</el-button>
    </el-header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();
const login = () => router.push({ path: '/login' });
const goHome = () => router.push({ path: '/', query: { path: '/' } });
defineProps({
    "siteName": String
});
</script>

<style>
.el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e6e6e6;
}
</style>
