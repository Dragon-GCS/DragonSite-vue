<template>
    <el-breadcrumb>
        <el-breadcrumb-item v-for="path in paths" :to="{
            name: 'home',
            query: { ...route.query, path: path.id }
        }" @click="cutPaths(path)">
            {{ path.name }}
        </el-breadcrumb-item>
    </el-breadcrumb>
</template>

<script setup lang="ts">
import { paths } from '../states';
const route = useRoute();
const cutPaths = (path: {id: string, name: string}) => {
    const idx = paths.value.findIndex((p) => p.id === path.id)
    paths.value = paths.value.slice(0, idx + 1)
}
</script>

<style scoped>
.el-breadcrumb {
    overflow-x: scroll;
    display: -webkit-box;
    width: 60%;
    height: calc(var(--el-font-size-medium) + 10px);
}
.el-breadcrumb::-webkit-scrollbar{
    height: 5px;
}
.el-breadcrumb::-webkit-scrollbar-thumb {
    display: none;
    height: 5px;
}

.el-breadcrumb::-webkit-scrollbar-thumb:hover {
    display: block;
    background: #ccc;
    border-radius: 5px;
}
</style>
