<template>
    <div class="container mt-5">
        <h1 class="text-center">Chamados Pendentes</h1>
        
        <div v-if="carregando" class="alert alert-info text-center">
            Carregando...
        </div>
        <div v-else-if="requestList.length === 0" class="alert alert-info text-center">
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
                        <th>Opções</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in requestList" :key="request.id">
                        <td>{{ request.id }}</td>
                        <td>{{ request.place_name }}</td>
                        <td>{{ request.title }}</td>
                        <td>{{ request.description }}</td>
                        <td>{{ typeMap[request.type] }}</td>
                        <td>{{ statusMap[request.status] }}</td>
                        <td><a v-if="request.status == 'P'" @click="capture(request.id)">Capturar</a></td>
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

const requestList = ref<Request[]>([]);

const carregando = ref(true)

function capture(id: number) {
    api
    .put(`/request/pendents/${id}/`, { status: 'A' })
    .then(() => {
        let obj = requestList.value.find(item => item.id === id)
        if (obj) obj.status = 'A';
    })
    .catch((error) => {
        console.error("Erro ao adicionar o residente:", error);
    });
}

onMounted(() => {
    api.get('/request/pendents')
    .then(response => {
        requestList.value = response.data;
        carregando.value = false
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
