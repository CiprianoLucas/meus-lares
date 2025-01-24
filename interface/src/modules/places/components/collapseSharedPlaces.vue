<template>
    <h5 class="text-center">Espaços compartilhados</h5>
    <div class="d-flex justify-content-center my-2">
        <button class="btn btn-secondary py-2 px-3 w-100" type="button" @click="onChangeCollapse">
            {{ showCollapse ? 'Esconder' : 'Mostrar' }} Configuração
        </button>
    </div>

    <div class="collapse pt-3" ref="listHtml">
        <div class="d-flex justify-content-center mb-3 mt-2">
            <router-link
                :to="'/espaco-compartilhado/cadastro/?condominium=' + condominiumId"
                class="btn btn-primary"
                >Cadastrar novos espaços compartilhados</router-link
            >
        </div>
        <list-table
            :url="'/place/shared/?condominium=' + condominiumId"
            :headers="headers"
            :column-path="columnPath"
            :param-path="paramPath"
            :start="showCollapse"
        />
    </div>
</template>

<script setup lang="ts">
import { Collapse } from 'bootstrap'
import app from '@/app'
import ListTable from '@/components/tables/ListTable.vue'

const listHtml = app.ref<HTMLElement>()
const showCollapse = app.ref<boolean>(false)
const listCollapse = app.ref<Collapse | null>(null)
const headers = app.ref({
    id: null,
    identifier: 'Identificador',
    capacity: 'Capacidade'
})

const columnPath = app.ref({
    identifier: 'espaco-compartilhado/:espaco'
})

const paramPath = app.ref({
    ':espaco': 'id'
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
        listCollapse.value = new Collapse(listHtml.value, { toggle: false })
    }
})
</script>

<style></style>
