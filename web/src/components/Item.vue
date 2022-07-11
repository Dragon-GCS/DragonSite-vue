<template>
    <div class="item-box" @mouseenter="show=true" @mouseleave="show=false">
        <div class="check-box">
            <el-checkbox
            v-show="show || selected"
            @change="select"
            />
        </div>
        <router-link
        :to="{
            name: 'main', 
            query: {
                path: data.full_path,
                logRequire: route.query.logRequire,
                filter: route.query.filter
            }}"
        >
            <img :src='`/assets/${data["type"]}.png`' :alt="data.name" width="64"/>
            {{ data.name }}
        </router-link>
        <el-button-group v-show="show||selected" style="margin: 5px 0px;">
        <el-popconfirm :title="`确认删除${data.name}`">
            <template #reference @mouseenter="show=true">
                <el-button type="info" size="small" @click="show=true">删除</el-button>
            </template>
        </el-popconfirm>
            <el-button type="info" size="small">重命名</el-button>
        </el-button-group>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router';
const route = useRoute();
const emit = defineEmits(["select"]);
const props = defineProps(["data"]);

const show = ref(false);
const selected = ref(false)

const changeShow = () => {
    show.value = !show.value
}
const select = () => {
    selected.value = !selected.value;
    emit('select', selected.value, props.data.full_path);
}
const remove = async () => {}
</script>

<style>
.check-box {
    position: absolute;
    width: 100px;
    display: flex;
    z-index: 1;
}
.item-box {
    padding: 10px 5px;
    border-radius: 5%;
    border: 1px solid #FFFFFF;
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
.item-box a {
    display: flex;
    flex-direction: column;
}
</style>