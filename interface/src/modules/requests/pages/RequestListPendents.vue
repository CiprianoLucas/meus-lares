<template>
    <div class="container mt-5">
        <h1 class="text-center">Chamados Pendentes</h1>
        <button @click="getList(true)" class="btn btn-primary mx-3 m-3">Atualizar</button>
        
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
import app from '@/app'
import { type Request, typeMap, statusMap } from '../interfaces'

const requestList = app.ref<Request[]>([]);
const carregando = app.ref(true)
const url = '/request/pendents/'

function capture(id: string) {
    app.api.put(url + id , { status: 'A' })
    .then(() => {
        let obj = requestList.value.find(item => item.id === id)
        if (obj) obj.status = 'A';
        app.popup('Sucesso!', 'Chamado capturado', 'success')
        sessionStorage.removeItem(url)
    })
    .catch(() => {
        app.popup('Erro!', 'Falha ao capturar o chamado', 'warning')
    });
}

function getList(force: boolean){
    app.api.getCashed<Request[]>(url, force)
    .then(response => {
        requestList.value = response;
        carregando.value = false
    })
    .catch(() => {
        app.popup('Erro!', 'Falha ao obter a lista de chamados', 'warning')
    });
}

app.onMounted(() => {
    getList(false)
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
