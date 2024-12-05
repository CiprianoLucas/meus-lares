<template>
    <div class="container mt-5">
        <h1 class="text-center">Residentes</h1>

        <!-- Input para adicionar novo residente -->
        <div class="input-group mb-3">
            <input
                type="email"
                class="form-control"
                v-model="newResidentEmail"
                placeholder="Digite o email do residente"
                aria-label="Email do Residente"
                aria-describedby="button-addon2"
            />
            <button
                class="btn btn-primary"
                type="button"
                id="button-addon2"
                @click="addResident"
                :disabled="!newResidentEmail"
            >
                Adicionar
            </button>
        </div>

        <!-- Mensagem de erro ao adicionar -->
        <div v-if="errorMessage" class="alert alert-danger text-center">
            {{ errorMessage }}
        </div>

        <!-- Tabela de residentes -->
        <div v-if="residents.length === 0" class="alert alert-info text-center">
            Nenhum residente encontrado.
        </div>

        <div v-else>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="resident in residents" :key="resident.id">
                        <td>{{ resident.username }}</td>
                        <td>{{ resident.email }}</td>
                        <td>
                            <a @click="deleteResident(resident.id)">excluir</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { type User } from '../../user/interfaces'

const residents = app.ref<User[]>([])
const newResidentEmail = app.ref('')
const errorMessage = app.ref('')

const placeId = app.ref(app.routeParam('id'))
const url = `/place/${placeId.value}/residents/`

app.onMounted(() => {
    fetchResidents()
})

function fetchResidents() {
    app.api
        .getCashed<User[]>(url)
        .then((data) => {
            residents.value = data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao listar os residentes.', 'warning')
        })
}

function deleteResident(userId: string) {
    app.api
        .delete(url + userId)
        .then(() => {
            residents.value = residents.value.filter((resident) => resident.id !== userId)
            sessionStorage.removeItem(url)
            app.popup('Sucesso!', 'Residente excluido com sucesso.', 'success')
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao excluir um residente.', 'warning')
        })
}

function addResident() {
    app.api
        .post(url, { email: newResidentEmail.value })
        .then((response) => {
            residents.value.push(response.data)
            newResidentEmail.value = ''
            errorMessage.value = ''
            sessionStorage.removeItem(url)
            app.popup('Sucesso!', 'Residente cadastrado com sucesso.', 'success')
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
}
</script>

<style scoped>
.text-center {
    text-align: center;
}
.table {
    margin-top: 20px;
}
.btn-danger {
    color: white;
}
</style>
