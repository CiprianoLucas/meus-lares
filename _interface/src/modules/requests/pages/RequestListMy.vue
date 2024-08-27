<template>
    <nav-bar/>
    <div class="container mt-5">
        <h1 class="text-center">Chamados Pendentes</h1>
        
        <div v-if="pendingRequests.length === 0" class="alert alert-info text-center">
            Nenhum chamado pendente no momento.
        </div>

        <div v-else>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Local</th>
                        <th>Título</th>
                        <th>Descrição</th>
                        <th>Tipo</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in pendingRequests" :key="request.id">
                        <td>{{ request.id }}</td>
                        <td>{{ request.place_name }}</td>
                        <td>{{ request.title }}</td>
                        <td>{{ request.description }}</td>
                        <td>{{ typeMap[request.type] }}</td>
                        <td>{{ statusMap[request.status] }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import NavBar from '@/components/template/NavBar.vue'
import { ref, onMounted } from 'vue'
import { api } from '@/http'


const typeMap = {
    'R': 'Reclamação',
    'M': 'Manutenção',
    'O': 'Outros'
};

const statusMap = {
    'P': 'Pendente',
    'A': 'Aprovado',
    'C': 'Concluído'
};

// Armazena a lista de chamados pendentes
const pendingRequests = ref([]);

onMounted(() => {
    // Obtém a lista de chamados pendentes ao montar o componente
    api.get('/request/residents/')
    .then(response => {
        pendingRequests.value = response.data;
    })
    .catch(error => {
        console.error("Erro ao obter a lista de chamados pendentes:", error);
    });
});
</script>

<style scoped>
.text-center {
    text-align: center;
}
.table {
    margin-top: 20px;
}
</style>
