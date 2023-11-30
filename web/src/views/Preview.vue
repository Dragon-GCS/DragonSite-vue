<template>
    <div id="content">
        <img v-if="type === 'image'" :src="blob" class="content" />
        <video v-else-if="type === 'video'" :src="blob" controls class="content" />
        <div v-else>
            Not support
        </div>
        <h2> {{ decodeURI(name) }} </h2>
        <div class="controls">
            <el-button type="primary" @click="move(index - 1)" :disabled="!items[index - 1]">Previous</el-button>
            <el-button type="primary"
                @click="downloadFile(name, path as string)">Download</el-button>
            <el-button type="primary" @click="move(index + 1)" :disabled="!items[index + 1]">Next</el-button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { previewFile, downloadFile } from '../api';
import { items } from '../states';

const route = useRoute();
const router = useRouter()

const { path, personal, idx } = route.query
const index = Number.parseInt(idx as string)

const { type, name, res } = await previewFile(path as string)
const blob = window.URL.createObjectURL(res)

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
    window.URL.revokeObjectURL(blob)
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