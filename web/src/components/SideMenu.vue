<template>
    <el-menu :collapse="isCollapsed" :unique-opened="true" :router="true" default-active="0-0">
        <el-sub-menu v-for="({ name, icon, personal }, idx) in  menus " :index="`${idx}`">
            <template #title>
                <img width="20" :src="icon" />
                <span>{{ name }}</span>
            </template>
            <el-menu-item v-for="({ type, icon, name }, subIdx) in  subMenus " :index="`${idx}-${subIdx}`" :route="{
                name: 'home', query: {
                    path: route.query.personal === personal ? route.query.path : '',
                    personal, filter: type
                }
            }">
                <img :src="icon" />
                <span>{{ name }}</span>
            </el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script setup lang="ts">
import { menus, subMenus } from '../config';

const route = useRoute()
const isCollapsed = ref<boolean>(document.body.clientWidth < 768);
onMounted(() => {
    window.onresize = () => {
        isCollapsed.value = document.body.clientWidth < 768;
    }
}
)
onUnmounted(() => { window.onresize = null })
</script>

<style>
.el-sub-menu span {
    /* 防止展开时宽度变化 */
    margin: 0 70px 0 15px;
}

.el-menu-item span {
    margin-left: 10px;
    margin-right: 0;
}
</style>