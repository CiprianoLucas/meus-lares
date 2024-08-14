<template>
    <header class="bg-dark text-white py-3">
        <div class="container">
            <nav class="d-flex justify-content-center">
            <RouterLink class="mx-3 text-white text-decoration-none" to="/">Home</RouterLink>
            <RouterLink class="mx-3 text-white text-decoration-none" to="/login">Login</RouterLink>
            </nav>
        </div>
    </header>
</template>
  
<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import { defineProps } from 'vue'
</script>