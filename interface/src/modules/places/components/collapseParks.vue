<template>

<h5 class="text-center">Estacionamento</h5>
    <div class="d-flex justify-content-center my-2">
        <button class="btn btn-secondary py-2 px-3 w-100" type="button" @click="onChangeCollapse">
            {{ showCollapse ? "Esconder" : "Mostrar" }} configuração
        </button>
    </div>

    <div class="collapse pt-3" ref="listHtml">
        <div class="d-flex justify-content-center mb-3 mt-2">
            <router-link :to="'condominio/condominio/apartamento/cadastro/'" class="btn btn-primary">Consultar
                placa</router-link>
        </div>
        <div class="d-flex justify-content-center mb-3 mt-2">
            <router-link :to="'condominio/condominio/apartamento/cadastro/'" class="btn btn-primary">Cadastrar novo
                estacionamento</router-link>
        </div>
        <list-table :url="'/place/park/?condominium=' + condominiumId" :headers="headers" :column-path="columnPath"
            :param-path="paramPath" :start="showCollapse" />
    </div>
</template>

<script setup lang="ts">
import { Collapse } from 'bootstrap';
import app from '@/app';
import ListTable from '@/components/tables/ListTable.vue';

const listHtml = app.ref<HTMLElement>();
const showCollapse = app.ref<boolean>(false);
const listCollapse = app.ref<Collapse | null>(null);
const headers = app.ref({
    'apartment_id': null,
    'id': null,
    'identifier': "Identificador",
    'apartment': "Apartamento"
})

const columnPath = app.ref({
    'identifier': "estacionamento/:parkId",
    'apartment': "apartamento/:apartmentId"
})

const paramPath = app.ref({
    ':parkId': "id",
    ':apartmentId': "apartment_id"
})

const props = defineProps<{
    condominiumId: string
}>()

function onChangeCollapse() {
    showCollapse.value = !showCollapse.value
    if (showCollapse.value) {
        listCollapse.value?.show()
    } else {
        listCollapse.value?.hide()
    }
}

app.onMounted(() => {
    if (listHtml.value) {
        listCollapse.value = new Collapse(listHtml.value, { toggle: false });
    }
});


</script>

<style></style>