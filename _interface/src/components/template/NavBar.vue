<template>
    <header class="bg-dark text-white py-3">
        <div class="container">
            <nav class="d-flex justify-content-center">
                <RouterLink class="mx-3 text-white text-decoration-none" to="/">Home</RouterLink>
                <RouterLink v-if="!username" class="mx-3 text-white text-decoration-none" to="/login">Login</RouterLink>
                <RouterLink v-if="!username" class="mx-3 text-white text-decoration-none" to="/usuario/cadastro/">Registrar</RouterLink>
                
                <div class="dropdown" v-if="isResident">
                    <RouterLink class="mx-3 text-white text-decoration-none" to="/requisicao/cadastro">Abrir solicitação</RouterLink>
                    <RouterLink class="mx-3 text-white text-decoration-none" to="/requisicao/minhas-requisicoes">Visualizar solicitações</RouterLink>
                </div>
                <div class="dropdown" v-if="isUnion">
                    <RouterLink class="mx-3 text-white text-decoration-none" to="/requisicao/pendentes">Solicitações pendentes</RouterLink>
                    <RouterLink class="mx-3 text-white text-decoration-none" to="/requisicao/capturados">Solicitações capturadas</RouterLink>
                </div>
                <RouterLink v-if="!!username" class="mx-3 text-white text-decoration-none" to="/condominio/cadastro">Cadastrar condomínio</RouterLink>
                <a v-if="!!username" class="mx-3 text-white text-decoration-none" @click="logout">Logout</a>
            </nav>
        </div>
    </header>
</template>
  
<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { RouterLink } from 'vue-router'
    import { api } from '@/http';

    const username = ref<string | null>(null);
    const isResident = ref(false)
    const isUnion = ref(false)


    async function logout(){
        await api.logout()
        window.location.reload()
    }

    onMounted(() => {
        console.log(document.cookie)
        username.value = localStorage.getItem("username")
        isResident.value = !!localStorage.getItem("isResident")
        isUnion.value = !!localStorage.getItem("isUnion")
    })
    
</script>

<script lang="ts">
    export default {
        name: 'NavBar'
    };
</script>