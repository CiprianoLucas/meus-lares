<template>
    <loading-page />
    <div class="all-nav">
        <div class="nav-container">
            <nav-bar />
        </div>
    </div>
    <div class="d-flex justify-content-center align-items-center">
        <div class="content-wrapper w-100 px-3">
            <RouterView />
        </div>
    </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/template/NavBar/NavBar.vue'
import LoadingPage from './components/PopUps/LoadingPage.vue'
import { RouterView } from 'vue-router'
</script>
<style scoped>
.content-wrapper {
    max-width: 1200px;
    width: 100%;
}

.all-nav {
    width: 100%;
    background: #212529;
    display: flex;
    justify-content: center;
}

.nav-container {
    max-width: 1200px;
    width: 100%;
}
</style>
