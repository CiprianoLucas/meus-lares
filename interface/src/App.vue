<template>
    <nav-bar />
    <div class="p-3">
        <RouterView />
    </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/template/NavBar/NavBar.vue'
import { RouterView } from 'vue-router'
</script>
