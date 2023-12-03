<template>
    <div class="item-box" @mouseenter="show = true" @mouseleave="show = false">
        <div class="check-box">
            <el-checkbox v-show="show || data.selected" v-model="data.selected" />
        </div>
        <div @click="preview" class="click-block">
            <p><img :src='imgUrl' :alt="data.name" width="64" height="64" /></p>
            <p>{{ data.name.length > 12 ? data.name.slice(0, 6) + '...' + data.name.slice(-3) : data.name }}</p>
        </div>
        <el-button-group v-show="show" style="margin: 5px 0px;">
            <el-button type="info" size="small" @click="remove(data)">删除</el-button>
            <el-button type="info" size="small" @click="rename">重命名</el-button>
        </el-button-group>
    </div>
</template>

<script setup lang="ts">
import { downloadFile, getThumbnail, renameResource } from '../api';
import { previewable, UserData } from '../config';
import { items, paths } from '../states';
import { remove } from '../utils'

const router = useRouter();
const route = useRoute();

const { personal, filter } = route.query;
const { data } = defineProps<{ data: UserData }>();

const show = ref(false);
let imgUrl = ''

if (data.is_dir) {
    imgUrl = '/static/folder.png'
} else if (data.meta?.category === 'image') {
    imgUrl = window.URL.createObjectURL(await getThumbnail(data.id))
}
else {
    imgUrl = `/static/${data.meta?.category}.png`
}

const preview = async () => {
    if (data.is_dir) {
        paths.value.push({ id: data.id, name: data.name })
        router.push({
            name: 'home',
            query: { path: data.id, personal, filter }
        })
    } else if (previewable.includes(data.meta?.category || '')) {
        items.value = items.value.filter((item) => previewable.includes(item.meta?.category || ''))
        let idx = items.value.findIndex((item) => item.id === data.id)
        router.push({
            name: 'preview',
            query: { path: data.id, idx, personal }
        })
    } else {
        downloadFile(data.name, data.id)
    }
}


const rename = () => {
    ElMessageBox.prompt('请输入新的文件名', '重命名', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\w\-. \u4e00-\u9fa5]+$/,
        inputErrorMessage: '文件名只能包含字母、数字、空格、下划线、中划线和点'
    }).then(async ({ value }) => {
        if (!value) { return }
        let res = await renameResource(data.parent?.id || '', data.id, value)
        if (!res[0]) return
        data.name = res[0].name
        ElMessage.success("重命名成功")
    }).catch((error) => {
        ElMessage.info(`已取消删除 ${error}`);
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
