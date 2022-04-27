<template>
    <el-menu :collapse="isCollapsed" :unique-opened="true" :router="true" default-active="0-0">
        <el-sub-menu v-for="(menu, idx) in subMenus" :index="`${idx}`">
            <template #title>
                <img width="20" :src="getIconUrl(menu.icon)" />
                <span>{{ menu.name }}</span>
            </template>
            <el-menu-item
                v-for="(cate, subIdx) in cates"
                :index="`${idx}-${subIdx}`"
                :route="{
                    name: 'main',
                    query: {
                        path: '/',
                        logRequire: menu.logRequire,
                        filter: cate.by}}"
            >
                <img :src="getIconUrl(cate.icon)" />
                <span>{{ cate.name }}</span>
            </el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {subMenus, cates} from '../config';

export default defineComponent({
    data() {
        return {
            isCollapsed: document.body.clientWidth < 768,
            subMenus,
            cates,
        }
    },

    mounted() {
        window.onresize = () => {
            return (() => {
                this.isCollapsed = document.body.clientWidth < 768;
            })()
        };
    },

    destoryed() { window.onresize = null },

    methods: {
        getIconUrl(icon: String) {
            return `https://api.iconify.design/${icon}?color=currentColor`
        }
    }
})
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