<template>
    <header class="bg-dark text-white py-3">
        <div class="container">
            <nav class="d-flex justify-content-center">
                <RouterLink class="mx-3 text-white text-decoration-none" to="/">Home</RouterLink>
                <RouterLink v-if="!isAuthenticated" class="mx-3 text-white text-decoration-none" to="/login">Login</RouterLink>
                <a v-if="isAuthenticated" class="mx-3 text-white text-decoration-none" @click="logout">Logout</a>
            </nav>
        </div>
    </header>
</template>
  
<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { RouterLink } from 'vue-router'
    import { api } from '@/http';

    const isAuthenticated = ref(false)

    async function logout(){
        await api.logout()
        window.location.reload()
    }

    onMounted(() => {
        console.log(document.cookie)
        const username = localStorage.getItem('username')
        isAuthenticated.value = !!username
    })
</script>