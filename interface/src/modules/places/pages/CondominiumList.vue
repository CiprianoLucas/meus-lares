<template>
    <div class="container mt-2">
        <div class="d-flex justify-content-center mb-3">
            <router-link to="/condominio/cadastro" class="btn btn-primary">
                <p class="h5 mb-1">Cadastrar novo condomínio</p>
            </router-link>
        </div>
        <h1 class="text-center mt-5">Condomínios</h1>
        <custom-table :headers="headers" url="/place/condominium/" :cashTime="300" title="name" img="profile_photo"
            :hide="['id', 'name', 'profile_photo']" redirect="condominio" :params="['id']" />
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomTable from '@/components/tables/CustomTable.vue'
const headers = app.ref({
    'id': "",
    'name': "",
    'profile_photo': "",
    'url': "",
    'street': "Logradouro",
    'city_name': "Cidade",
    'state': "Estado",
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
