<template>
    <el-button @click="goHome" :link="true">
        <h1>{{ siteName }}</h1>
    </el-button>

    <el-button v-if="!loginState" @click="login" auto-insert-space>登录</el-button>
    <h1 v-else @click="logout" style="cursor:pointer">Welcome {{ username }}</h1>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { loginState, username } from '../config'
import { logout as logoutApi } from '../api'

defineProps({ "siteName": String })
defineEmits(["pointerenter", "pointerleave"])

const router = useRouter()
const login = () => router.push({ path: '/login' }) 
const goHome = () => router.push({ path: '/'})
const logout = () => {
    logoutApi()
    router.push({ path: '/'})
}
</script>
