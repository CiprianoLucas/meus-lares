<template>
    <div class="container mt-5">
        <h1 class="text-center">Condomínios</h1>
        
        <div v-if="places.length === 0" class="alert alert-info text-center">
            Nenhum local disponível no momento.
        </div>

        <div v-else>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Número</th>
                        <th>Rua</th>
                        <th>Cidade</th>
                        <th>Estado</th>
                        <th>Opções</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="place in places" :key="place.id">
                        <td>{{ place.name }}</td>
                        <td>{{ place.number }}</td>
                        <td>{{ place.street }}</td>
                        <td>{{ place.city }}</td>
                        <td>{{ place.state }}</td>
                        <td><a :href="`/condominio/${place.id}`">editar</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { type Place } from '../../places/interfaces'
const places = app.ref<Place[]>([]);

app.onMounted(() => {
    app.api.getCashed<Place[]>('/place/unions/')
        .then((response) => {
            places.value = response;
        })
        .catch(()=>{
            app.popup('Erro!', 'Falha ao listar os condomínios', 'warning')
        })
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
