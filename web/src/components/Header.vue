<template>
    <el-button @click="goHome" type="text">
        <h1>{{ siteName }}</h1>
    </el-button>
    <el-button @click="login" auto-insert-space>登录</el-button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
defineEmits(["pointerenter", "pointerleave"]);
const router = useRouter();
const login = () => router.push({ path: '/login' });
const goHome = () => router.push({ path: '/'});
defineProps({
    "siteName": String
});
</script>
