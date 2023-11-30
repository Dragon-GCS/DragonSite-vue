<template>
    <el-button-group>
        <!-- 新建文件夹 -->
        <el-button type="primary">
            <i class="i-ic-outline-create-new-folder" style="font-size:20px" @click="newFolder" />
        </el-button>
        <!-- 全部选择 -->
        <el-button type="primary">
            <i class="i-fluent-select-all-on-24-filled" style="font-size:20px" @click="selectAll" />
        </el-button>
        <!-- 批量删除 -->
        <el-button type="primary">
            <i class="i-ph-trash-fill" style="font-size:20px" @click="remove()" />
        </el-button>
        <!-- 上传文件 -->
        <el-button type="primary">
            <el-upload v-show="!uploading" style="display: flex;" :action="postUrl" :multiple="true" name="files"
                :before-upload="beforeUpload" :on-success="uploadSuccess" :on-error="uploadError"
                :on-progress="uploadProgress" :show-file-list="false" :with-credentials="true">
                <i class="i-ic-baseline-file-upload" style="font-size:20px"></i>
            </el-upload>
            <el-progress v-show="uploading" :percentage="percentage" :stroke-width="2" type="circle" :width="20"
                status="success" />
        </el-button>
    </el-button-group>
</template>

<script setup lang="ts">
import { createFolder } from '../api';
import { items } from '../states';
import { remove, sortFunc } from '../utils';

const route = useRoute();
const { path, personal } = route.query
const router = useRouter();
const uploading = ref<boolean>(false)
const percentage = ref<number>(0)


let postUrl = `/api/disk/resources?personal=${personal}`
if (path) { postUrl += `&path=${path}` }

const selectAll = () => {
    let selectedItems = items.value.filter(e => e.selected)
    let select = selectedItems.length !== items.value.length
    for (let item of items.value) item.selected = select
}

const newFolder = () => {
    ElMessageBox.prompt('请输入文件夹名称', '新建文件夹', {
        inputPattern: /^[^/\\:\?\.\*\'<>|]+$/,
        inputErrorMessage: '包含非法字符（/\\:?.*<>\'|）'
    }).then(({ value }) => {
        if (!value) { return }
        if (items.value.filter(e => e.name === value).length != 0) {
            ElMessage.error('文件夹已存在'); return
        }
        createFolder(path as string, value).then((res) => {
            items.value = items.value.concat(res)
            items.value.sort(sortFunc)
            ElMessage.success('文件夹创建成功')
        })
    }).catch((e) => {
        ElMessage.info('取消新建文件夹:' + e)
    })
}

const beforeUpload = (file: File) => {
    if (items.value.filter(e => e.name === file.name).length !== 0) {
        ElMessage.error(`文件${file.name}已存在`);
        return false
    }
    if (!uploading.value) {
        uploading.value = true
    }
    return true;
}

const uploadSuccess = (res: any, file: any, fileList: any) => {
    items.value = items.value.concat(res)
    items.value.sort()
    ElMessage.success(`${res[0]?.name}上传成功`)
}

const uploadError = (err: any, file: any, fileList: any) => {
    if (err.status === 401) {
        ElMessage.error('未登录')
        router.push({ name: 'login', query: { redirect: route.fullPath } })
    }
    uploading.value = false
    ElMessage.error('上传失败')
}
const uploadProgress = (event: any, file: any, fileList: any) => {
    percentage.value = Math.round(event.percent)
    if (event.percent === 100) {
        uploading.value = false
    }
}

</script>
