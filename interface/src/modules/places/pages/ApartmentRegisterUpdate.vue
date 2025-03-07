<template>
    <div class="container mt-2">
        <h1 v-if="apartmentId" class="text-center">Editar apartamento</h1>
        <h2 v-else class="text-center">Registrar apartamentos</h2>
        <custom-form :form="apartmentForm" :inputs="inputs" />
        <div v-if="!apartmentId" class="d-flex justify-content-end py-2 border-bottom">
            <button @click="addApartment" class="btn btn-secondary">Adicionar</button>
        </div>
        <div v-if="!apartmentId" class="p-2">
            <p>
                <small
                    >Os apartamentos adicionados só serão cadastrados ao clicar em
                    "Cadastrar"</small
                >
            </p>
        </div>
        <div class="d-flex justify-content-between my-3">
            <button @click="goBack" class="btn btn-secondary">Voltar</button>
            <button v-if="apartmentId" @click="updateApartment" class="btn btn-primary">
                Salvar
            </button>
            <button v-else @click="registerApartments" class="btn btn-primary">Cadastrar</button>
        </div>
        <div v-if="listApartmentsRegister.length > 0">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Identificador</th>
                            <th scope="col">Opções</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(aparment, i) in listApartmentsRegister" :key="i" scope="col">
                            <td>{{ aparment.identifier }}</td>
                            <td>
                                <div class="d-flex justify-content-end">
                                    <button
                                        @click="complementModalBody = aparment.complement"
                                        class="btn btn-secondary py-0 px-1 mx-1"
                                        data-bs-toggle="modal"
                                        data-bs-target="#complementModal"
                                    >
                                        <small><i class="bi bi-file-text"></i></small>
                                    </button>
                                    <button
                                        @click="deleteApartment(i)"
                                        class="btn btn-danger py-0 px-1 mx-1"
                                    >
                                        <small><i class="bi bi-trash"></i></small>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div
            class="modal fade"
            id="complementModal"
            tabindex="-1"
            aria-labelledby="complementModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="complementModalLabel">Descrição</h1>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>
                    <div class="modal-body">
                        {{ complementModalBody }}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Fechar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomForm from '@/components/forms/CustomForm.vue'
import type { Apartment } from '../interfaces'
import { useRouter } from 'vue-router'
import type { Input } from '@/components/forms/interfaces'

const router = useRouter()
const inputs = app.ref<Input[]>([
    {
        reference: 'identifier',
        label: 'Identificador',
        size: 'bit',
        type: 'text',
        placeholder: 'Ex: apt, sala...'
    },
    {
        reference: 'complement',
        label: 'Descrição',
        size: 'xl',
        type: 'textarea'
    }
])
const apartmentId = app.ref(app.routeParam('id'))
if (!apartmentId.value) {
    inputs.value.splice(1, 0, {
        reference: 'sufix',
        label: 'Sufixo',
        size: 'bit',
        type: 'text',
        placeholder: 'Ex: 101, 102, a1...'
    })
}

const condominiumId = app.routeQuery('condominium')
const complementModalBody = app.ref()

const apartmentForm = app.ref<{ [key: string]: string }>({
    identifier: '',
    sufix: '',
    complement: ''
})

const listApartmentsRegister = app.ref<Apartment[]>([])

function addApartment() {
    let identifier = apartmentForm.value.identifier + apartmentForm.value.sufix

    identifier = identifier.trim()
    if (!identifier) {
        app.popup('Erro!', 'Não foi inserido identificador', 'warning')
        return
    }

    if (listApartmentsRegister.value.some((aparment) => aparment.identifier === identifier)) {
        app.popup('Erro!', 'Já existe um apartamento com esse identificador.', 'warning')
        return
    }

    const newApartment = <Apartment>{
        complement: apartmentForm.value.complement,
        identifier: identifier
    }

    listApartmentsRegister.value.push(newApartment)

    app.popup('Adicionado', `apartamento ${newApartment.identifier}`, 'success', 1500)

    if (Number(apartmentForm.value.sufix)) {
        const newSufix = String(Number(apartmentForm.value.sufix) + 1)
        apartmentForm.value.sufix = newSufix
    }
}

function deleteApartment(i: number) {
    listApartmentsRegister.value.splice(i, 1)
}

function registerApartments() {
    if (!condominiumId) {
        app.popup('Erro!', 'Condomínio não identificado', 'danger')
    }
    app.loading(true, 'Cadastrando...')
    const payload = {
        condominium_id: condominiumId,
        apartments: listApartmentsRegister.value
    }

    app.api
        .post('/place/apartments/bulk-create/', payload)
        .then(() => {
            app.popup('Sucesso!', 'Apartamentos salvos com sucesso', 'success')
            app.api.clearStartPath('/place/apartment/?condominium=' + condominiumId)
            router.push('/condominio/' + condominiumId)
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function updateApartment() {
    app.loading(true, 'Atualizando...')
    const payload = {
        identifier: apartmentForm.value.identifier,
        complement: apartmentForm.value.complement
    }
    app.api
        .patch('/place/apartment/' + apartmentId.value + '/', payload)
        .then(() => {
            app.popup('Sucesso!', 'Informações do apartamento salvas', 'success')
            app.api.clearStartPath('/place/apartment/')
            router.push('/apartamento/' + apartmentId.value)
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
    if (apartmentId.value) {
        await getApartmentValues()
    }
})

async function getApartmentValues() {
    app.api
        .get(`/place/apartment/${apartmentId.value}/`)
        .then(({ data }) => {
            apartmentForm.value = data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}
</script>
