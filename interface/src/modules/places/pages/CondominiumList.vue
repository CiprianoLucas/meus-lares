<template>
    <div class="container mt-2">
        <div class="d-flex justify-content-center mb-3">
            <router-link to="/condominio/cadastro" class="btn btn-primary">
                Cadastrar novo condomínio
            </router-link>
        </div>
        <h1 class="text-center mt-5">Condomínios</h1>
        <list-cards
            :start="true"
            :headers="headers"
            url="/place/condominium/"
            :cashTime="300"
            title="name"
            img="profile_photo"
            :hide="['id', 'name', 'profile_photo']"
            redirect="condominio"
            :params="['id']"
            :searchable="true"
        />
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import ListCards from '@/components/tables/ListCards.vue'
const headers = app.ref({
    id: null,
    name: null,
    profile_photo: null,
    url: null,
    street: '',
    city_name: '',
    state: ''
})
</script>
