<template>
    <el-container>
        <el-main>
            <router-view :key="$route.fullPath"></router-view>
        </el-main>
        <el-footer v-if="showFooter" height="20px">
            <el-link href="http://github.com/Dragon-GCS" :underline="false">
                Coding by Dragon-GCS
                <img
                    :src="getIconUrl('ri:github-fill.svg')"
                    width="15"
                />
            </el-link>
        </el-footer>
    </el-container>
</template>


<script setup lang="ts">
import { getIconUrl } from "../utils";
const showFooter = document.body.clientWidth > 560
</script>

<style>
.el-footer {
    font-size: 12px;
    border-top: 1px solid #ebeef5;
}
</style>

