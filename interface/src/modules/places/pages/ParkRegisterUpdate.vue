<template>
    <div class="container mt-2">
        <h1 v-if="parkId" class="text-center">Editar estacionamento</h1>
        <h2 v-else class="text-center">Registrar estacionamentos</h2>
        <custom-form :form="parkForm" :inputs="inputs" />
        <div v-if="!parkId" class="d-flex justify-content-end py-2 border-bottom">
            <button @click="addPark" class="btn btn-secondary">Adicionar</button>
        </div>
        <div class="p-2">
            <p>
                <small
                    >Os estacionamentos adicionados só serão cadastrados ao clicar em
                    "Cadastrar"</small
                >
            </p>
        </div>
        <div class="d-flex justify-content-between my-3">
            <button @click="goBack" class="btn btn-secondary">Voltar</button>
            <button v-if="parkId" @click="updatePark" class="btn btn-primary">Salvar</button>
            <button v-else @click="registerParks" class="btn btn-primary">Cadastrar</button>
        </div>
        <div v-if="listParksRegister.length > 0">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Identificador</th>
                            <th scope="col">Apartamento</th>
                            <th scope="col">Opções</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(park, i) in listParksRegister" :key="i" scope="col">
                            <td>{{ park.identifier }}</td>
                            <td>{{ park.apartment_identifier }}</td>
                            <td>
                                <div class="d-flex justify-content-end">
                                    <button
                                        @click="complementModalBody = park.complement"
                                        class="btn btn-secondary py-0 px-1 mx-1"
                                        data-bs-toggle="modal"
                                        data-bs-target="#complementModal"
                                    >
                                        <small><i class="bi bi-file-text"></i></small>
                                    </button>
                                    <button
                                        @click="deletePark(i)"
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
import type { Apartment, Park } from '../interfaces'
import { useRouter } from 'vue-router'
import type { Input, Options } from '@/components/forms/interfaces'

const router = useRouter()
const apartmentList = app.ref<Options[]>([])
const inputs = app.ref<Input[]>([
    {
        reference: 'identifier',
        label: 'Identificador',
        size: 'bit',
        type: 'text',
        placeholder: 'Ex: Vaga'
    },
    {
        reference: 'sufix',
        label: 'Sufixo',
        size: 'bit',
        type: 'text',
        placeholder: 'Ex: 101, 102, a1...'
    },
    {
        reference: 'apartment',
        label: 'Apartamento (opcional)',
        options: apartmentList.value,
        size: 'sm',
        type: 'select'
    },
    {
        reference: 'complement',
        label: 'Descrição',
        size: 'xl',
        type: 'textarea'
    }
])
const parkId = app.ref(app.routeParam('id'))
const condominiumId = app.routeQuery('condominium')
const complementModalBody = app.ref()

const parkForm = app.ref<{ [key: string]: string }>({
    identifier: '',
    sufix: '',
    apartment: '',
    complement: ''
})

const listParksRegister = app.ref<Park[]>([])

function addPark() {
    let identifier = parkForm.value.identifier + parkForm.value.sufix

    identifier = identifier.trim()
    if (!identifier) {
        app.popup('Erro!', 'Não foi inserido identificador', 'warning')
        return
    }

    if (listParksRegister.value.some((park) => park.identifier === identifier)) {
        app.popup('Erro!', 'Já existe um estacionamento com esse identificador.', 'warning')
        return
    }

    const apartment = apartmentList.value.find(
        (apartment) => apartment.value === parkForm.value.apartment
    )

    const newPark = <Park>{
        complement: parkForm.value.complement,
        apartment: apartment?.value || null,
        apartment_identifier: apartment?.label || null,
        identifier: identifier
    }

    listParksRegister.value.push(newPark)

    if (Number(parkForm.value.sufix)) {
        const newSufix = String(Number(parkForm.value.sufix) + 1)
        parkForm.value.sufix = newSufix
    }
    console.log(listParksRegister.value)
}

function deletePark(i: number) {
    listParksRegister.value.splice(i, 1)
}

function registerParks() {
    if (!condominiumId) {
        app.popup('Erro!', 'Condomínio não identificado', 'danger')
    }
    app.loading(true, 'Cadastrando...')
    const payload = {
        condominium_id: condominiumId,
        parks: listParksRegister.value
    }

    app.api
        .post('/place/parks/bulk-create/', payload)
        .then(() => {
            app.popup('Sucesso!', 'Estacionamentos salvos com sucesso', 'success')
            app.api.clearStartPath('/place/park/?condominium=' + condominiumId)
            router.push('/condominio/' + condominiumId)
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function updatePark() {
    app.loading(true, 'Atualizando...')
    app.api
        .patch('/place/park/' + parkId.value + '/', parkForm.value)
        .then(({ data }) => {
            app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
            app.api.removeListCash('/place/park/')
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
    if (parkId.value) {
        await getParkValues()
        return
    }
    getApartments()
})

async function getApartments() {
    app.api
        .getListCashed<Apartment[]>(`/place/apartment/?condominium=` + condominiumId)
        .then(({ result }) => {
            const newApartmentList = result.map((apartment) => {
                const toSelect = {
                    value: apartment.id as string,
                    label: apartment.identifier as string
                }
                return toSelect
            })

            apartmentList.value.splice(0, apartmentList.value.length, ...newApartmentList)
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}

async function getParkValues() {
    app.api
        .get(`/place/park/${parkId.value}/`)
        .then(({ data }) => {
            parkForm.value = data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}
</script>
