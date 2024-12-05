<template>
    <div class="container mt-5">
        <h1 class="text-center">Condomínios</h1>
        <custom-table :data="places" :options="true" />
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomTable from '@/components/tables/CustomTable.vue'
import { type Place } from '../../places/interfaces'
const places = app.ref<Place[]>([])

app.onMounted(() => {
    app.api
        .getCashed<Place[]>('/place/unions/')
        .then((response) => {
            places.value = response
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
