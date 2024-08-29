<template>
    <div class="container mt-5">
        <h1 class="text-center">Meus chamados</h1>
        
        <div v-if="requestList.length === 0" class="alert alert-info text-center">
            Nenhum chamado pendente no momento.
        </div>

        <div v-else>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Local</th>
                        <th>Título</th>
                        <th>Descrição</th>
                        <th>Tipo</th>
                        <th>Status</th>
                        <th>Opções</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in requestList" :key="request.id">
                        <td>{{ request.place_name }}</td>
                        <td>{{ request.title }}</td>
                        <td>{{ request.description }}</td>
                        <td>{{ typeMap[request.type] }}</td>
                        <td>{{ statusMap[request.status] }}</td>
                        <td><a v-if="request.status == 'P'" :href="`/requisicao/${request.id}`">Editar</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { api } from '@/http'
import { type Request, typeMap, statusMap } from '../interfaces'

// Armazena a lista de chamados pendentes
const requestList = ref<Request[]>([]);

onMounted(() => {
    // Obtém a lista de chamados pendentes ao montar o componente
    api.get('/request/residents/')
    .then(response => {
        requestList.value = response.data;
    })
    .catch(error => {
        console.error("Erro ao obter a lista de chamados pendentes:", error);
    });
});
</script>

<style scoped>

td a {
        cursor: pointer;
    }
.text-center {
    text-align: center;
}
.table {
    margin-top: 20px;
}
</style>
