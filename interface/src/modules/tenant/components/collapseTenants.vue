<template>
    <h5 class="text-center">Moradores</h5>
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
                >Cadastra novo Morador</router-link
            >
        </div>
        <list-cards
            :url="'/relation/tenant/?condominium=' + condominiumId"
            redirect="morador"
            :params="['id']"
            img="user_identity_photo"
            :start="true"
            title="user_full_name"
            :headers="headersTenants"
        />
    </div>
</template>

<script setup lang="ts">
import { Collapse } from 'bootstrap'
import app from '@/app'
import ListCards from '@/components/tables/ListCards.vue'

const listHtml = app.ref<HTMLElement>()
const showCollapse = app.ref<boolean>(false)
const listCollapse = app.ref<Collapse | null>(null)

const props = defineProps<{
    condominiumId: string
}>()

const headersTenants = app.ref({
    id: null,
    user_full_name: null,
    user_identity_photo: null,
    is_renter: 'Aluguel:',
    is_responsible: 'Responsável:'
})

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
