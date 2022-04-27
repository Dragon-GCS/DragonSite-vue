<template>
    <el-row class="func-bar">
        <el-breadcrumb>
            <el-breadcrumb-item
                v-for="path in path_array"
                :to="{
                    name: 'main',
                    query: {
                        path: path[1],
                        logRequire: $route.query.logRequire,
                        filter: $route.query.filter
                    }
                }"
            >{{ path[0] }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-button-group>
            <el-button type="primary">
                <img width="15" :src="getIconUrl('ic:outline-create-new-folder.svg', 'white')" />
            </el-button>
            <el-button type="primary">
                <el-upload style="display: flex;" action="post_url">
                    <img width="15" :src="getIconUrl('ic:baseline-file-upload.svg', 'white')" />
                </el-upload>
            </el-button>
        </el-button-group>
    </el-row>
    <div>this is main contain</div>
    <div>querys: {{ query }}</div>
    <div>full_path: {{route.fullPath}}</div>
    <div style="display: flex; flex-wrap: wrap;">
        <Item v-for="item in resp.data" :data="item">
        </Item>
    </div>

</template>

<script setup lang="ts">
import axios from 'axios';
import Item from '../components/Item.vue';
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { breadcrumb, getIconUrl } from '../utils'

const emits = defineEmits(['pointerenter', 'pointerleave'])
const route = useRoute();
const router = useRouter();
const path_array: Array<[String, String]> = breadcrumb((route.query.path || "/").toString())
const params = route.params;
const query = route.query;
console.log(params, query, route.fullPath);

let resp = ref({
    data: Array<{ name: string, full_path: string }>(),
    msg: String
})

const post_url = "/api/disk";

axios({
    method: 'get',
    url: '/api/disk',
    params: route.query
}).then(res => {
    resp.value = res.data.response;
    console.log(res.code);
}).catch(err => {
    console.log(err);
    router.push({ name: 'NotFound', params: {path: '404'} });
});

</script>


<style>
.func-bar {
    margin: 0;
    padding: 0 15px 5px 15px;
    border-bottom: 1px solid #333333;
    justify-content: space-between;
    align-items: center;
}
</style>

