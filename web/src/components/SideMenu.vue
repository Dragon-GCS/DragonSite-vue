<template>
    <el-menu
    :collapse="isCollapsed"
    :unique-opened="true"
    :router="true"
    default-active="0-0"
    >
        <el-sub-menu v-for="(menu, idx) in menus" :index="`${idx}`">
            <template #title>
                <img width="20" :src="menu.icon" />
                <span>{{ menu.name }}</span>
            </template>
            <el-menu-item
            v-for="(subMenu, subIdx) in subMenus"
            :index="`${idx}-${subIdx}`"
            :route="{ name: 'main', query: { path: '/', logRequire: menu.logRequire, filter: subMenu.type}}"
            >
                <img :src="subMenu.icon" />
                <span>{{ subMenu.name }}</span>
            </el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import { menus, subMenus } from '../config';

let isCollapsed = ref<boolean>(document.body.clientWidth < 768);

onMounted(() => {
    window.onresize = () => {
        isCollapsed.value = document.body.clientWidth < 768;
    }
}
)
onUnmounted(() => {window.onresize = null})
</script>

<style>
.el-sub-menu span {
    /* 防止展开时宽度变化 */
    margin: 0 70px 0 15px;
}

.el-menu-item span{
    margin-left: 10px;
    margin-right: 0;
}
</style>