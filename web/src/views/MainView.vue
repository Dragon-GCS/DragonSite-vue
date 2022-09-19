<template>
    <el-row class="func-bar">
        <el-breadcrumb>
            <el-breadcrumb-item v-for="path in path_array" :to="{
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
                <i class="i-ic-outline-create-new-folder" style="font-size:20px" @click="newFolder" />
            </el-button>
            <!-- 全部选择 -->
            <el-button type="primary">
                <i class="i-fluent-select-all-on-24-filled" style="font-size:20px" @click="selectAll" />
            </el-button>
            <!-- 批量删除 -->
            <el-button type="primary" v-show="!(select_item.length===0)">
                <i class="i-ph-trash-fill" style="font-size:20px" @click="removeAll" />
            </el-button>
            <!-- 上传文件 -->
            <el-button type="primary">
                <el-upload v-show="!uploading" style="display: flex;" :action="post_url" :multiple="true"
                    :headers="get_tokens()" name="files" :before-upload="beforeUpload" :on-success="uploadSuccess"
                    :on-error="uploadError" :on-progress="uploadProgress" :show-file-list="false"
                    :with-credentials="true">
                    <i class="i-ic-baseline-file-upload" style="font-size:20px"></i>
                </el-upload>
                <el-progress v-show="uploading" :percentage="percentage" :stroke-width="2" type="circle" :width="20"
                    status="success" />
            </el-button>
        </el-button-group>
    </el-row>
    <div style="display: flex; flex-wrap: wrap;">
        <Item v-for="item,idx in items" :data="item" :idx="idx" :selectedArray="selected_array" @select="handleSelect"
            @remove="handleRemoveResource" @rename="handleRename" @preview="handlePreview">
        </Item>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox, ElUpload } from "element-plus";
import { breadcrumb } from "../utils"
import { loadResource, createFolder, downloadFile, removeResource, renameResource, get_tokens } from "../api"
import { UserData, items, previewable } from "../config";

defineEmits(["pointerenter", "pointerleave"]);

const route = useRoute();
const router = useRouter();
const path_array: [string, string][] = breadcrumb((route.query.path || "/").toString())
const post_url = `/api/disk/upload?login_require=${route.query.logRequire}&path=${route.query.path}`
const uploading = ref<boolean>(false)
const percentage = ref<number>(0)

// Load resource
let selected_array = ref<boolean[]>([])

items.value = []
loadResource(
    (route.query.path || "/").toString(),
    route.query.logRequire === "true",
    (route.query.filter || "all").toString()
).then((res) => {
    items.value = res.data
    for (let i = 0; i < items.value.length; i++) {
        selected_array.value.push(false)
    }
    console.log("load resource", res)
})

const select_item = ref<UserData[]>([])
const handleSelect = (idx: number) => {
    // v-model will auto update selected_array
    if (selected_array.value[idx]) {
        select_item.value.push(items.value[idx])
    } else {
        select_item.value = select_item.value.filter(
            (item) => item.name !== items.value[idx].name)
    }
}

const selectAll = () => {
    if (select_item.value.length === items.value.length) {
        select_item.value = []
        for (let i = 0; i < selected_array.value.length; i++) {
            selected_array.value[i] = false
        }
    } else {
        for (let i = 0; i < selected_array.value.length; i++) {
            selected_array.value[i] = true
        }
        select_item.value = items.value
    }
}

const handlePreview = (idx: number) => {
    let resource = items.value[idx]
    items.value = items.value.filter((item) => previewable.includes(item.category))
    idx = items.value.findIndex((item) => item.path === resource.path)
    if (resource.is_dir) {
        router.push({
            name: 'main',
            query: {
                idx,
                logRequire: route.query.logRequire,
                filter: route.query.filter
            }
        })
    } else if (previewable.includes(resource.category)) {
        router.push({
            name: 'preview',
            query: {
                idx,
                logRequire: route.query.logRequire as string,
            }
        })
    } else {
        downloadFile(resource.name, resource.path, route.query.logRequire === "true")
    }
}

const newFolder = () => {
    ElMessageBox.prompt("请输入文件夹名称", "新建文件夹", {
        inputPattern: /^[a-zA-Z0-9_]+$/,
        inputErrorMessage: "文件夹名称只能包含字母、数字和下划线"
    }).then(({ value }) => {
        if (!value) { return }
        if (items.value.filter(e => e.name === value).length != 0) {
            ElMessage.error("文件夹已存在"); return
        }
        createFolder(
            (route.query.path || "/").toString(),
            value,
            route.query.logRequire === "true"
        ).then((res) => {
            items.value = items.value.concat(res)
            items.value.sort()
            ElMessage.success("文件夹创建成功")
        })
    }).catch((err) => {
        ElMessage.info("取消新建文件夹")
    })
}

const handleRename = (resource: UserData, new_name: string) => {
    let parent = resource.parent_path === "/" ? "" : resource.parent_path
    let new_path = parent + '/' + new_name

    if (items.value.filter(e => (e.path === new_path && e.is_dir === resource.is_dir)).length != 0) {
        ElMessage.error("名称已存在"); return
    }
    renameResource(
        resource.path,
        new_path,
        resource.is_dir,
        route.query.logRequire === "true"
    ).then((res) => {
        let index = items.value.indexOf(resource)
        items.value[index] = res[0]
        ElMessage.success("重命名成功")
    })
}

const handleRemoveResource = (resource: UserData) => {
    removeResource(
        (route.query.path || "/").toString(),
        [resource.name],
        [resource.is_dir],
        route.query.logRequire === "true",
    ).then((res) => {
        if (res.status !== 200 || !res.data.success) {
            ElMessage.error("删除失败"); return
        }
        items.value = items.value.filter(e => e !== resource)
        selected_array.value.fill(false)
        console.log("remove resource", res)
        ElMessage.success("删除成功")
    })
}

const removeAll = async () => {
    ElMessageBox.confirm(`确定删除选中的${select_item.value.length}个资源?`, "确认提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
    }).then(() => {
        removeResource(
            (route.query.path || "/").toString(),
            select_item.value.map(e => e.name),
            select_item.value.map(e => e.is_dir),
            route.query.logRequire === "true",
        ).then((res) => {
            if (res.status !== 200 || !res.data.success) {
                ElMessage.error("删除失败"); return
            }
            items.value = items.value.filter(e => !select_item.value.includes(e))
            select_item.value = []
            selected_array.value.fill(false)
            ElMessage.success("删除成功")
        })
    }).catch(() => {
        console.log("取消删除")
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
    ElMessage.success(`${res[0].name}上传成功`)
}

const uploadError = (err: any, file: any, fileList: any) => {
    if (err.status === 401) {
        ElMessage.error("未登录")
        router.push({ name: "login", query: { redirect: route.fullPath } })
    }
    uploading.value = false
    console.log("上传失败", err)
    ElMessage.error("上传失败")
}
const uploadProgress = (event: any, file: any, fileList: any) => {
    percentage.value = Math.round(event.percent)
    if (event.percent === 100) {
        uploading.value = false
    }
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

