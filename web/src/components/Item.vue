<template>
    <div class="item-box" @mouseenter="show = !show" @mouseleave="show = !show">
        <div style="width:110px;position: absolute;z-index: 1;display: flex;">
            <el-checkbox v-if="show || selected" @change="selected = !selected"></el-checkbox>
        </div>
        <router-link :to="
        {name: 'main', 
        query: {
            path: data.full_path,
            logRequire: route.query.logRequire,
            filter: route.query.filter
        }}">
            <div>
                <img :src="getImageUrl(data)" :alt="data.name" width="64" @click="toItem()">
            </div>
            {{ data.name }}
        </router-link>
        <el-button-group v-if="show" style="margin: 5px 0px;">
            <el-button type="info" size="small">删除</el-button>
            <el-button type="info" size="small">重命名</el-button>
        </el-button-group>
    </div>
    {{ data }}
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref } from 'vue'
const show = ref(false);
const selected = ref(false)
const route = useRoute();
const getImageUrl = (data: Record<string, any>) => {
    if (data.isDir) {
        //https://icons8.com/icons/set/folder
        return new URL("../assets/folder.png", import.meta.url).href;
    }
    else {
        return new URL(`../assets/${data.type}.png`, import.meta.url).href;
    }
}

const props = defineProps(
    {
        data: {
            type: Object,
            default() {
                return { name: '', isDir: false, type: 'file' }
            }
        },
    }
)
const emits = defineEmits(
    ['pointerenter', "pointerleave"]
)
</script>

<style>
.item-box {
    padding: 10px;
    border-radius: 5%;
    border: 1px solid #FFFFFF;
    margin: 10px;
    width: 110px;
    height: 110px;
    display: flex;
    flex-direction: column;
    align-items: center
}

.item-box:hover {
    border: 1px solid #ccc;
    background-color: #f5f5f5;
}
</style>