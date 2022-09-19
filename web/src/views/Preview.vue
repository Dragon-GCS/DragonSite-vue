<template>
    <div id="content">
        <img v-if="type==='image'" :src="blob" class="content" />
        <video v-else-if="type==='video'" :src="blob" controls class="content" />
        <div v-else>
            Not support
        </div>
        <h2>
        {{ files[idx].name }}
        </h2>
        <div class="controls">
            <el-button type="primary" @click="prevFile" :disabled="idx <= 0">Previous</el-button>
            <el-button type="primary" @click="download">Download</el-button>
            <el-button type="primary" @click="nextFile" :disabled="idx >= (files.length - 1)">Next</el-button>
        </div>
    </div>

</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { previewFile, downloadFile } from '../api';
import { items } from '../config';

const route = useRoute();
const router = useRouter()

const idx = Number.parseInt(route.query.idx as string);
const type = items.value[idx].category;
const files = items.value

const blob = ref("")
previewFile(files[idx].path as string, route.query.logRequire === "true").then((res) => {
    blob.value = URL.createObjectURL(new Blob([res]))
})

const download = () => {
    downloadFile(files[idx].name, files[idx].path as string, route.query.logRequire === "true")
}
const prevFile = () => {
    if (idx <= 0) { return }
    router.push({
        name: 'preview',
        query: {
            idx: idx - 1,
            logRequire: route.query.logRequire as string,
        }
    })
    window.URL.revokeObjectURL(blob.value)
}

const nextFile = () => {
    if (idx >= (files.length - 1)) { return }
    router.push({
        name: 'preview',
        query: {
            idx: idx + 1,
            logRequire: route.query.logRequire as string,
        }
    })
    window.URL.revokeObjectURL(blob.value)
}

</script>

<style>
#content {
    width: 100%;
    height: 90%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.content {
    width: 100%;
    height: 90%;
    object-fit: contain;
}

.controls {
    width: 50%;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    margin-top: 15px;
}
</style>