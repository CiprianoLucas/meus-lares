<template>
    <div class="container mt-2">
        <h1 class="text-center">Cadastrar morador</h1>
        <text-input label="Email do morador" placeholder="email@email.com" type="text" id="tenant-email"
            @change="findUser()" v-model="tenantForm.tenant_email" required />
        <text-input label="Nome do morador" type="text" id="tenant-name" v-model="tenantForm.tenant_name" disabled />
        <select-input @change="listTenants" label="Apartamento" id="apartment" v-model="tenantForm.apartment"
            :options="apartmentOptions" option-label="identifier" :disabled="apartmentId" :allow-empty="true"
            :preserve-search="true" />
        <div v-if="actualTenants !== null && actualTenants.length > 0" class="alert alert-warning">
            <p class="text-center"><strong>Atenção!</strong></p>
            <p class="justify-text">Já existe um morador, o novo morador terá vínculo com o atual. </p>
            <p class="justify-text">Portanto as alterações de contrato, permissões dentre outros aspéctos serão
                diretamente ligadas ao novo morador</p>
        </div>
        <radio-input help-modal="Teste 123" help-tooltip="teste" v-else v-model="tenantForm.contract"
            label="Tipo de vínculo" id="contrato" option-value="value" option-label="label" :options="constractTypes"
            tooltip="Através do contrato serão efetuadas todas as automações e permissões para o morador. ex: notificação de boletos, reservas de espaços..." />

        <label class="form-label mt-3">Outras configurações</label>
        <check-input id="first-contact" label="Contato principal"
            help-tooltip="Será a primeira pessoa a aparecer nos registros relacionados ao apartamento"
            help-modal="Será a primeira pessoa a aparecer nos registros relacionados ao apartamento"
            v-model="tenantForm.is_fisrt_contact" />
        <check-input id="responsible" label="Responsável"
            help-tooltip="Terá acessos como responsável do apartamento"
            help-modal="Terá acessos de responsável do apartamento. Como faturas, advertências, históricos de chamados..."
            v-model="tenantForm.is_responsible" />

        <div class="d-flex justify-content-between my-3">
            <button @click="goBack" class="btn btn-secondary">Voltar</button>
            <button @click="registerTenant" class="btn btn-primary">Cadastrar</button>
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
const actualTenants = app.ref<object[] | null>(null)
const constractTypes = app.ref([
    { value: "1", label: "Sem contrato" },
    { value: "2", label: "Com contrato" },
])

const tenantForm = app.ref({
    tenant_email: '',
    tenant_id: '',
    tenant_name: '',
    apartment: {} as Apartment | null,
    contract: '1',
    is_fisrt_contact: false,
    is_responsible: false,
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
            tenantForm.value.apartment = option
        })
        .catch((error) => {
            app.popup("Erro", app.resumeErrors(error), "danger")
        })
        .finally(() => { app.loading(false) })
}

function listTenants() {
    let apartmentIdToGet = null
    if (apartmentId.value) {
        apartmentIdToGet = apartmentId.value
    } else if (tenantForm.value.apartment?.id) {
        apartmentIdToGet = tenantForm.value.apartment.id
    }

    app.loading(true, 'Buscando...')
    app.api.getListCashed('/relation/tenant/?is_active=true&apartment=' + apartmentIdToGet)
        .then(({ result }) => {
            actualTenants.value = result as object[]
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

function registerTenant() {
    if (!tenantForm.value.tenant_id) {
        app.popup('Erro!', 'Usuário do morador não identificado', 'danger')
        return
    }
    if (!tenantForm.value.apartment?.id) {
        app.popup('Erro!', 'Apartamento não identificado', 'danger')
        return
    }
    app.loading(true, 'Cadastrando...')
    const payload = {
        apartment: tenantForm.value.apartment.id,
        user: tenantForm.value.tenant_id,
        is_responsible: tenantForm.value.is_responsible,
        is_fisrt_contact: tenantForm.value.is_fisrt_contact,
    }

    app.api
        .post('/relation/tenant/', payload)
        .then(() => {
            app.popup('Sucesso!', 'Morador cadastrado com sucesso', 'success')
            app.api.clearStartPath('/relation/tenant/?is_active=true&apartment=' + payload.apartment)
            router.push('/apartamento/' + payload.apartment)
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
        listTenants()
    }
})
</script>
