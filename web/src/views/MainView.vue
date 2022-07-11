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
                    filter: $route.query.filter }
            }">
            {{ path[0] }}
            </el-breadcrumb-item>
        </el-breadcrumb>
        <el-button-group>
            <!-- 新建文件夹 -->
            <el-button type="primary">
                <i
                class="i-ic-outline-create-new-folder"
                style="font-size:20px"
                @click="createFolder"
                />
            </el-button>
            <!-- 批量删除 -->
            <el-button type="primary" v-show="!(select_item.length===0)">
                <i
                class="i-ph-trash-fill"
                style="font-size:20px"
                @click="removeAll"
                />
            </el-button>
            <!-- 上传文件 -->
            <el-button type="primary">
                <el-upload style="display: flex;"
                action="post_url"
                :multiple="true"
                :data="{logRequire: $route.query.logRequire}"
                >
                    <i class="i-ic-baseline-file-upload" style="font-size:20px"></i>
                </el-upload>
            </el-button>
        </el-button-group>
    </el-row>
    <div>querys: {{ route.query }}</div>
    <div>full_path: {{route.fullPath}}</div>
    <div>select: {{ select_item }}</div>
    <div style="display: flex; flex-wrap: wrap;">
        <Item 
        v-for="item in items"
        :data="item"
        @select="handleSelect">
        </Item>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Item from '../components/Item.vue';
import { useRoute, useRouter } from 'vue-router';
import { breadcrumb } from '../utils'
import { items } from '../data';
import { ElMessageBox } from 'element-plus';

defineEmits(["pointerenter", "pointerleave"]);

const route = useRoute();
const router = useRouter();
const path_array: [string, string][] = breadcrumb((route.query.path || "/").toString())
const select_item  = ref<Array<string>>([])
const handleSelect = (state: boolean, path: string) => {
    if (state) {
        select_item.value.push(path)
    } else {
        select_item.value = select_item.value.filter(e => e !== path)
    }
}
const createFolder = () => {
    ElMessageBox.prompt('请输入文件夹名称', '新建文件夹', {
        inputPattern: /^[a-zA-Z0-9_]+$/,
        inputErrorMessage: '文件夹名称只能包含字母、数字和下划线'
    }).then(async ({ value }) => {
        if (value) {
            items.push({
                name: value,
                full_path: `${route.query.path}/${value}`,
                type: "folder"
            })
            items.sort()
            console.log(items)
        }
    }).catch(() => {
        console.log('取消')
    })
}
const removeAll = async () => {
    console.log('Remove all files')
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

