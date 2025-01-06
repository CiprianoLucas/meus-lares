<template>
    <div class="container mt-2">
        <router-link to="/condominio/cadastro" class="text-dark text-decoration-none">
            <div class="d-flex justify-content-center align-items-center border rounded p-2 m-1">
                <h6 class="text-center m-0">Cadastrar novo condomínio</h6>
            </div>
        </router-link>
        <h1 class="text-center mt-5">Condomínios</h1>
        <custom-table :headers="headers" url="/place/condominium/" :cashTime="300" title="name" img="profile_photo" />
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomTable from '@/components/tables/CustomTable.vue'
import { type Place } from '../../places/interfaces'
const places = app.ref<Place[]>([])
const headers = app.ref({
    'name': "",
    'profile_photo': "",
    'street': "Logradouro",
    'city_name': "Cidade",
    'state': "Estado",
})

app.onMounted(() => {
    app.api
        .getListCashed<Place[]>('/place/condominium/')
        .then(({result}) => {
            places.value = result
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao listar os condomínios', 'warning')
        })
})
</script>

<style scoped>
.text-center {
    text-align: center;
}
.table {
    margin-top: 20px;
}
</style>
