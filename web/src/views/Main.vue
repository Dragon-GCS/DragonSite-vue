<template>
    <el-row class="func-bar">
        <Breadcrumb />
        <Menu />
    </el-row>
    <div style="display: flex; flex-wrap: wrap;">
        <Item v-for="data in items" :key="data.id" :data="data" />
    </div>
</template>

<script setup lang="ts">
import { sortFunc } from '../utils'
import { loadResource, currentPaths } from '../api'
import { items, paths } from '../states';

const route = useRoute();
const { path, filter } = route.query

const resp = await loadResource(path as string, filter as string)
items.value = []
if (resp instanceof Array) {
    items.value = resp.sort(sortFunc)
    if (
        !(paths.value.length) ||
        (paths.value.length === 1 && paths.value.at(-1)?.name != 'Home') ||
        (paths.value.length > 1 && route.query.path !== paths.value.at(-1)?.id)
    ) { paths.value = await currentPaths(); }
}

for (let i = 0; i < items.value.length; i++) {
    items.value[i].selected = false
}
console.log('load resource', resp)
</script>


<style>
.func-bar {
    padding: 0 15px 5px 15px;
    border-bottom: 1px solid #333333;
    justify-content: space-between;
    align-items: center;
}
</style>