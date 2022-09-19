<template>
    <img v-if="type==='image'" :src="blob" style="width: 100%; height: 100%; object-fit: contain;" />
    <video v-else-if="type==='video'" controls style="width: 100%; height: 100%;">
        <source :src="blob" type="video/mp4" />
    </video>
    <div v-else>
        Not support
    </div>

</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { previewFile } from '../api';

// TODO preview
const route = useRoute();
const path = route.query.path as string;
const login_require = route.query.logRequire === "true";
const type = route.query.type as string;

let blob = ref("")
previewFile(path, login_require).then((res) => {
    blob.value = URL.createObjectURL(new Blob([res.data]))
})

console.log(type, blob)
window.URL.revokeObjectURL(blob.value)
</script>