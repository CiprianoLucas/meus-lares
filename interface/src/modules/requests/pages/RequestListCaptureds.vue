<template>
    <div class="container mt-5">
        <h1 class="text-center">Chamados capturados</h1>
        
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
                        <th>Abandonar</th>
                        <th>Concluir</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in requestList" :key="request.id">
                        <td>{{ request.place_name }}</td>
                        <td>{{ request.title }}</td>
                        <td>{{ request.description }}</td>
                        <td>{{ typeMap[request.type] }}</td>
                        <td>{{ statusMap[request.status] }}</td>
                        <td><a @click="updateRequest(request.id, 'P')"><i class="bi bi-x-circle text-danger"></i></a></td>
                        <td><a @click="updateRequest(request.id, 'C')"><i class="bi bi-check-circle text-success"></i></a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { type Request, typeMap, statusMap } from '../interfaces'

// Armazena a lista de chamados pendentes
const requestList = app.ref<Request[]>([])
const url = '/request/pendents/'

function updateRequest(id: string, status: 'P' | 'A' | 'C') {
    app.api.put(url + id, { status: status })
    .then(() => {
        let obj = requestList.value.find(item => item.id === id)
        if (obj) obj.status = status
        app.popup('Sucesso!', 'Chamado atualizado', 'success')
        sessionStorage.removeItem(url)
        sessionStorage.removeItem('/request/guardians/')
    })
    .catch(() => {
        app.popup('Erro!', 'Falha ao atualizar o chamado', 'warning')
    })
}

app.onMounted(() => {
    app.api.getCashed<Request[]>('/request/guardians/')
    .then(response => {
        requestList.value = response
    })
    .catch(() => {
        app.popup('Erro!', 'Falha ao obter a lista de chamados', 'warning')
    })
})
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
