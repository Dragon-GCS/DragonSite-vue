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
            <!-- 新建文件夹 -->
            <el-button type="primary">
                <img width="15"
                :src="getIconUrl('ic:outline-create-new-folder.svg', 'white')"
                @click="createFolder"/>
            </el-button>
            <!-- 上传文件 -->
            <el-button type="primary">
                <el-upload style="display: flex;"
                action="post_url"
                :multiple="true"
                :data="{logRequire: $route.query.logRequire}"
                >
                    <img width="15"
                    :src="getIconUrl('ic:baseline-file-upload.svg', 'white')" />
                </el-upload>
            </el-button>
        </el-button-group>
    </el-row>
    <div>querys: {{ query }}</div>
    <div>full_path: {{route.fullPath}}</div>
    <div style="display: flex; flex-wrap: wrap;">
        <Item 
        v-for="item in items"
        :data="item"
        @select-checkbox="handleSelect">
        </Item>
        <But/>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus';
import Item from '../components/Item.vue';
import { useRoute, useRouter } from 'vue-router';
import { breadcrumb, getIconUrl } from '../utils'
import { items } from '../data';

const route = useRoute();
const router = useRouter();
const params = route.params;
const query = route.query;
const create_folder = ref(false);
const path_array: [String, String][] = breadcrumb((route.query.path || "/").toString())
const select_item  = ref<Record<string, string>[]>([])
const handleSelect = (state: boolean, item: Record<string, string>) => {
    if (state) {
        select_item.value.push(item)
    } else {
        select_item.value = select_item.value.filter(e => e.full_path !== item.full_path)
    }
}
const createFolder = () => {
    console.log("createFolder")
    ElMessageBox.prompt('Please input your e-mail', 'Tip', {
    confirmButtonText: 'OK',
    cancelButtonText: 'Cancel',
    inputPattern:
      /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
    inputErrorMessage: 'Invalid Email',
  })
    .then(({ value }) => {
      ElMessage({
        type: 'success',
        message: `Your email is:${value}`,
      })
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: 'Input canceled',
      })
    })
}
</script>


<style>
.func-bar {
    padding: 0 15px 5px 15px;
    border-bottom: 1px solid #333333;
    justify-content: space-between;
    align-items: center;
}
</style>

