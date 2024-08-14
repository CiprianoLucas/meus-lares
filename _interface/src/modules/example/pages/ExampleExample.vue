<template>
    <nav-bar/>
    <div class="container">
        <p>{{ message }}</p>
    </div>
</template>
  
<script lang="ts" setup>
    import NavBar from '@/components/template/NavBar.vue'
    import { ref, onMounted } from 'vue'
    import { api } from '@/http'
    
    const message = ref('')
    
    const getFetch = () => {
        api.get('/example/')
        .then(() => {
            message.value = 'Example: Success'
        })
        .catch(() => {
            message.value = 'Example: Error'
        })
    }
    
    onMounted(() => {
        getFetch()
    })
</script>