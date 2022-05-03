<template>
    <div class="item-box" @mouseenter="show = !show" @mouseleave="show = !show">
        <div style="width:110px;position:absolute;z-index: 1;display: flex;">
            <el-checkbox v-if="show || selected" @change="select"></el-checkbox>
        </div>
        <router-link :to="
        {name: 'main', 
        query: {
            path: data.full_path,
            logRequire: route.query.logRequire,
            filter: route.query.filter
        }}">
            <div>
                <img :src='`/assets/${data["type"]}.png`' :alt="data.name" width="64">
            </div>
            {{ data.name }}
        </router-link>
        <el-button-group v-if="show" style="margin: 5px 0px;">
            <el-button type="info" size="small">删除</el-button>
            <el-button type="info" size="small">重命名</el-button>
        </el-button-group>
    </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref } from 'vue'
const show = ref(false);
const selected = ref(false)
const route = useRoute();
const emit = defineEmits(["selectCheckbox"]);
const props = defineProps(["data", "showCheckbox"]);
const select = () => {
    selected.value = !selected.value;
    emit('selectCheckbox', selected.value, props.data);
}
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