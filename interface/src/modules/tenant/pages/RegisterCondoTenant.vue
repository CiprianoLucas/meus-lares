<template>
    <div class="container mt-2">
        <h1 class="text-center">Cadastrar morador</h1>
        <text-input label="Email do morador" placeholder="email@email.com" type="text" id="tenant-email"
            @change="findUser()" v-model="tenantForm.tenant_email" required />
        <text-input label="Nome do morador" type="text" id="tenant-name" v-model="tenantForm.tenant_name" disabled />
        <select-input label="Apartamento" id="apartment" v-model="tenantForm.apartment" :options="apartmentOptions"
            option-label="identifier" :disabled="apartmentId" :allow-empty="true"
            :preserve-search="true" />
        <div class="alert alert-warning">
            <p class="text-center"><strong>Atenção!</strong></p>
            <p class="justify-text">Já existe um morador, o novo morador terá vínculo com o atual. </p>
            <p class="justify-text">Portanto as alterações de contrato, permissões dentre outros aspéctos serão
                diretamente ligadas ao novo morador</p>
        </div>
        <radio-input v-model="tenantForm.contract" label="Tipo de vínculo" id="contrato" option-value="value"
            option-label="label" :options="constractTypes" />

        <label class="form-label mt-3">Outras configurações</label>
        <check-input id="first-contact" label="Contato principal"
            tooltip="Será a primeira pessoa a aparecer nos registros relacionados ao apartamento"
            v-model="tenantForm.is_fisrt_contact" />

        <div class="d-flex justify-content-between my-3">
            <button @click="goBack" class="btn btn-secondary">Voltar</button>
            <button @click="registerSharedPlaces" class="btn btn-primary">Cadastrar</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { useRouter } from 'vue-router'
import TextInput from '@/components/forms/TextInput.vue'
import SelectInput from '@/components/forms/SelectInput.vue'
import type { Apartment } from '@/modules/places/interfaces'
import RadioInput from '@/components/forms/RadioInput.vue'
import CheckInput from '@/components/forms/CheckInput.vue'

const router = useRouter()
const apartmentId = app.ref(app.routeQuery('apartment'))
const condominiumId = app.routeQuery('condominium')
const apartmentOptions = app.ref<Apartment[]>([])
const constractTypes = app.ref([
    { value: "1", label: "Sem contrato" },
    { value: "2", label: "Com contrato" },
])

const tenantForm = app.ref({
    tenant_email: '',
    tenant_id: '',
    tenant_name: '',
    apartment: null,
    contract: '',
    is_fisrt_contact: false,
})

function findUser() {
    app.loading(true, 'Buscando...')
    app.api.get('/user/email/' + tenantForm.value.tenant_email)
        .then(({ data }) => {
            tenantForm.value.tenant_name = data.name
            tenantForm.value.tenant_id = data.id

        })
        .catch((error) => {
            if (error.status == 404) {
                app.popup("Usuário não encontrado", "", "warning")
            } else {
                app.popup("Erro", app.resumeErrors(error), "danger")
            }
        })
        .finally(() => { app.loading(false) })
}

function getApartment() {
    app.loading(true, 'Buscando...')
    app.api.get(`/place/apartment/${apartmentId.value}/`)
        .then(({ data }) => {
            const option = {
                id: data.id,
                identifier: data.identifier
            }
            apartmentOptions.value = [option]
            tenantForm.value.apartment = data.id
        })
        .catch((error) => {
            app.popup("Erro", app.resumeErrors(error), "danger")
        })
        .finally(() => { app.loading(false) })
}

function listApartments() {
    app.loading(true, 'Buscando...')
    app.api.getListCashed('/place/apartments-all/' + condominiumId)
        .then(({ result }) => {
            apartmentOptions.value = result as Apartment[]
        })
        .catch((error) => {
            app.popup("Erro", app.resumeErrors(error), "danger")
        })
        .finally(() => { app.loading(false) })
}

function registerSharedPlaces() {
    if (!condominiumId) {
        app.popup('Erro!', 'Condomínio não identificado', 'danger')
    }
    app.loading(true, 'Cadastrando...')
    const payload = {
        condominium_id: condominiumId
    }

    app.api
        .post('/place/shareds/bulk-create/', payload)
        .then(() => {
            app.popup('Sucesso!', 'Espaços compartilhados salvos com sucesso', 'success')
            app.api.clearStartPath('/place/shared/?condominium=' + condominiumId)
            router.push('/condominio/' + condominiumId)
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
    if (condominiumId) {
        listApartments()
    }
    if (apartmentId.value) {
        getApartment()
    }
})
</script>
