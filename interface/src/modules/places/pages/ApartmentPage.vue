<template>
    <div v-if="apartment.id">
        <div
            class="border-bottom d-flex flex-column justify-content-center align-items-center py-2"
        >
            <h2>{{ apartment.identifier }}</h2>
        </div>
        <div class="border-bottom px-4 py-3">
            <div class="d-flex justify-content-between mb-3">
                <h3 class="p-0 m-0">Descrição:</h3>
                <router-link
                    :to="'/apartamento/edicao/' + apartmentId"
                    class="btn btn-secondary py-0"
                    ><small>Editar</small></router-link
                >
            </div>
            <p
                v-html="
                    apartment.complement
                        ? apartment.complement.replace(/\n/g, '<br>')
                        : '-- Sem descrição --'
                "
            ></p>
        </div>
        <div class="text-center py-3 mb-3 border-bottom">
            <h5 class="text-center mb-3">Moradores atuais</h5>
            <list-cards
                :url="'/relation/tenant/?is_active=true&apartment=' + apartmentId"
                redirect=""
                img="user_identity_photo"
                :start="true"
                title="user_fullname"
                :headers="headersTenants"
            />
            <router-link
                :to="'/morador/cadastro/?apartment=' + apartmentId"
                class="btn btn-primary mt-4 py-2 px-3 w-100"
                type="button"
            >
                Cadastrar morador
            </router-link>
            <button class="btn btn-secondary mt-4 py-2 px-3 w-100" type="button">
                Histórico de moradores
            </button>
        </div>
        <div class="text-center py-3 mb-3 border-bottom">
            <h5 class="">Estacionamento</h5>
            <list-table
                :url="'/place/park/?apartment=' + apartmentId"
                :headers="headersPark"
                :column-path="columnPathPark"
                :param-path="paramPathPark"
                :start="true"
                :searchable="false"
            />
        </div>
        <div class="d-flex justify-content-between border-bottom px-4 pt-2 pb-5">
            <button @click="deleteApartment" class="btn btn-danger py-1">Excluir</button>
            <button @click="onOffApartment" class="btn btn-warning py-1">
                {{ apartment.is_active ? 'Desativar' : 'Ativar' }}
            </button>
        </div>
    </div>
    <div v-else>
        <div class="d-flex justify-content-center border-bottom px-4 py-3">
            <p class="text-center">Falha ao obter informações do condominio.</p>
        </div>
        <div class="d-flex justify-content-center border-bottom px-4 py-3">
            <button @click="goBack" class="btn btn-secondary py-1">Voltar</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import type { Apartment } from '../interfaces'
import { useRouter } from 'vue-router'
import type { Tenant } from '@/modules/tenant/interfaces'
import ListCards from '@/components/tables/ListCards.vue'
import ListTable from '@/components/tables/ListTable.vue'

const router = useRouter()
const apartmentId = app.ref<string>(app.routeParam('id').toString())
const apartment = app.ref<Apartment>({})
const tenantsHistory = app.ref<Tenant[]>()

const headersTenants = app.ref({
    id: null,
    user_fullname: null,
    user_identity_photo: null,
    is_renter: 'Aluguel:',
    is_responsible: 'Responsável:'
})

const headersPark = app.ref({
    id: null,
    identifier: 'Identificador'
})

const columnPathPark = app.ref({
    identifier: 'estacionamento/:parkId'
})

const paramPathPark = app.ref({
    ':parkId': 'id'
})

app.onMounted(async () => {
    app.loading(true)
    await getApartmentValues()
    await getTenants()
    app.loading(false)
})

function deleteApartment() {
    app.loading(true)
    app.api
        .delete(`/place/apartment/${apartmentId.value}/`)
        .then(() => {
            app.api.clearStartPath('/place/apartment/?condominium=' + apartment.value.condominium)
            app.api.clearStartPath('/place/park/?condominium=' + apartment.value.condominium)
            app.popup('Excluido', 'Apartamento excluido com sucesso.')
            router.push('/condominio/' + apartment.value.condominium)
        })
        .catch((error) => {
            app.popup('Erro', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function onOffApartment() {
    app.loading(true)
    app.api
        .patch(`/place/apartment/${apartmentId.value}/`, { is_active: !apartment.value.is_active })
        .then(() => {
            apartment.value.is_active = !apartment.value.is_active
            app.popup('Atualizado', 'Apartamento atualizado com sucesso.')
        })
        .catch((error) => {
            app.popup('Erro', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function goBack() {
    router.go(-1)
}

async function getApartmentValues() {
    app.api
        .get(`/place/apartment/${apartmentId.value}/`)
        .then(({ data }) => {
            apartment.value = data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}

async function getTenants() {
    app.api
        .getListCashed<Tenant[]>('/relation/tenant/?apartment=' + apartmentId.value)
        .then(({ result }) => {
            tenantsHistory.value = result
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}
</script>
