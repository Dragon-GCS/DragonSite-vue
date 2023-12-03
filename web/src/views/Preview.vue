<template>
    <div id="content">
        <img v-if="type === 'image'" :src="src" class="content" />
        <video v-else-if="type === 'video'" :src="src" controls class="content" />
        <div v-else>
            Not support
        </div>
        <h2> {{ decodeURI(name) }} </h2>
        <div class="controls">
            <el-button type="primary" @click="move(index - 1)" :disabled="!items[index - 1]">Previous</el-button>
            <el-button type="primary" @click="downloadFile(name, path as string)">Download</el-button>
            <el-button type="primary" @click="move(index + 1)" :disabled="!items[index + 1]">Next</el-button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { getPreviewUrl, downloadFile } from '../api';
import { items } from '../states';

const route = useRoute();
const router = useRouter()

const { path, personal, idx } = route.query
const index = Number.parseInt(idx as string)
const src = getPreviewUrl(path as string)
var name: string
var type: string

if (index && items.value[index]) {
    name = items.value[index].name
    type = items.value[index].meta?.category || ''
} else {
    const headers = new Headers()
    headers.append('Range', 'bytes=0-0')
    const res = await fetch(src, { headers })
    name = res.headers.get('Content-Disposition')?.split('filename=')[1] || ''
    type = res.headers.get('Content-Type')?.split('/')[0] || ''
}

const move = (nex_idx: number) => {
    if (!items.value[nex_idx]) { return }
    router.push({
        name: 'preview',
        query: {
            path: items.value[nex_idx].id,
            idx: nex_idx,
            personal: personal as string,
        }
    })
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