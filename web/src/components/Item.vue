<template>
    <div class="item-box" @mouseenter="show=true" @mouseleave="show=false">
        <div class="check-box">
            <el-checkbox
            v-show="show || selectedArray[idx]"
            @change="emit('select', idx)"
            v-model="selectedArray[idx]" />
        </div>
        <div @click="clickResource" class="click-block">
            <p><img :src='`/assets/${icon}.png`' :alt="data.name" width="64" /></p>
            <p>{{ getDisplayName() }}</p>
        </div>
        <el-button-group v-show="show" style="margin: 5px 0px;">
            <el-button type="info" size="small" @click="remove">删除</el-button>
            <el-button type="info" size="small" @click="rename">重命名</el-button>
        </el-button-group>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { ElMessageBox } from 'element-plus';
import { downloadFile } from '../api';

const route = useRoute();
const router = useRouter()
const props = defineProps(["data", "selectedArray", "idx"]);
const emit = defineEmits(["select", "remove", "rename"]);

const show = ref(false);
const icon = props.data.is_dir ? 'folder' : props.data.category

const getDisplayName = () => {
    return props.data.name.length > 12 ? props.data.name.slice(0, 6) + '...' + props.data.name.slice(-3) : props.data.name
}

const clickResource = () => {
    if (props.data.is_dir) {
        router.push({
            name: 'main',
            query: {
                path: props.data.path,
                logRequire: route.query.logRequire,
                filter: route.query.filter
            }
        })
    } else if (['image', 'video', 'pdf', 'document'].includes(props.data.category)) {
        router.push({
            name: 'preview',
            query: {
                path: props.data.path,
                logRequire: route.query.logRequire,
                type: props.data.category
            }
        })
    } else {
        downloadFile(props.data.path, route.query.logRequire === "true")
    }
}
const remove = () => {
    ElMessageBox.confirm(`确定删除${props.data.name}?`, '确认提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(() => {
        emit('remove', props.data);
    }).catch(() => {
        console.log('取消删除');
    });
}

const rename = () => {
    ElMessageBox.prompt('请输入新的文件名', '重命名', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\w\-. ]+$/,
        inputErrorMessage: '文件名只能包含字母、数字、空格、下划线、中划线和点'
    }).then(({ value }) => {
        if (!value) { return }
        emit('rename', props.data, value)
    }).catch((error) => {
        console.log('取消重命名', error);
    });
}

</script>

<style>
.check-box {
    position: absolute;
    width: 100px;
    display: flex;
    z-index: 1;
}

.click-block {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.click-block:hover {
    color: #409EFF;
    cursor: pointer;
}

.item-box {
    padding: 10px 5px;
    border-radius: 5%;
    border: 1px solid #FFFFFF;
    width: 110px;
    height: 110px;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 0.5em;
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