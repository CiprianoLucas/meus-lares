<template>
    <div class="container mt-5">
        <h1 v-if="condominiumId" class="text-center">Editar condomínio</h1>
        <h1 v-else class="text-center">Registrar condomínio</h1>
        <custom-form :form="condominiumForm" :inputs="inputs" />
        <div class="d-flex justify-content-between mt-5">
            <button @click="goBack" class="btn btn-secondary">Voltar</button>
            <button v-if="condominiumId" @click="updateCondominium" class="btn btn-primary">
                Salvar
            </button>
            <button v-else @click="registerCondominium" class="btn btn-primary">Cadastrar</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomForm from '@/components/forms/CustomForm.vue'
import { inputsProps } from '@/components/forms'
import type { Condominium } from '../interfaces'
import { useRouter } from 'vue-router'

const router = useRouter()
const inputs = app.ref(inputsProps)
const condominiumId = app.ref(app.routeParam('id'))

const condominiumForm = app.ref<Condominium>({
    name: '',
    cep: '',
    number: '',
    street: '',
    complement: '',
    neighborhood: '',
    city: 0,
    state: ''
})

app.watch(
    () => condominiumForm.value.cep,
    (newValue, oldValue) => {
        verifyCep(newValue)
    }
)

app.watch(
    () => condominiumForm.value.state,
    (newValue, oldValue) => {
        updateCities(newValue)
    }
)

async function updateCities(uf: string = '') {
    app.loading(true, 'Buscando endereço...')
    app.api
        .getListCashed<{ id: number; name: string; state: string }[]>('/place/cities/' + uf)
        .then(({ result }) => {
            const options = result.map((item) => ({ value: item.id, label: item.name }))
            const cityInput = inputs.value.find((input) => input.reference === 'city')
            if (cityInput && cityInput.options) {
                cityInput.options = options
            }
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error, "Cidades não foram atualizadas"), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
    app.loading(false)
}

async function verifyCep(cep: string = '') {
    if (cep.length === 9) {
        app.loading(true, 'Buscando endereço...')
        app.api
            .get('/place/cep/' + cep)
            .then(({ data }) => {
                condominiumForm.value.city = data.city
                condominiumForm.value.state = data.state
                condominiumForm.value.neighborhood = data.neighborhood
                condominiumForm.value.street = data.street
            })
            .catch((error) => {
                app.popup('Erro!', app.resumeErrors(error, "CEP não encontrado"), 'warning')
            })
            .finally(() => {
                app.loading(false)
            })
    }
}

function registerCondominium() {
    app.loading(true, 'Cadastrando...')
    app.api
        .post('/place/condominium/', condominiumForm.value)
        .then(({ data }) => {
            app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
            app.api.removeListCash('/place/condominium/')
            router.push('/condominio/' + data.id)
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function updateCondominium() {
    app.loading(true, 'Salvando...')
    app.api
        .patch('/place/condominium/' + condominiumId.value + '/', condominiumForm.value)
        .then(({ data }) => {
            app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
            app.api.removeListCash('/place/condominium/')
            router.push('/condominio/' + data.id)
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function goBack() {
    router.go(-1)
}

app.onMounted(async () => {
    if (condominiumId.value) {
        await getCondominiumValues()
    }
})

async function getCondominiumValues() {
    app.loading(true, 'Buscando dados...')
    app.api
        .get(`/place/condominium/${condominiumId.value}/`)
        .then(({ data }) => {
            condominiumForm.value = data
            condominiumForm.value.cep = data.cep.replace(/(\d{5})(\d{3})/, '$1-$2')
            delete condominiumForm.value.profile_photo
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}
</script>
