<template>
    <div class="container mt-2">
        <h1 v-if="sharedId" class="text-center">Editar espaço compartilhado</h1>
        <h2 v-else class="text-center">Registrar espaços compartilhados</h2>
        <custom-form :form="sharedForm" :inputs="inputs" />
        <div v-if="!sharedId" class="d-flex justify-content-end py-2 border-bottom">
            <button @click="addSharedPlace" class="btn btn-secondary">Adicionar</button>
        </div>
        <div v-if="!sharedId" class="p-2">
            <p>
                <small
                    >Os espaços compartilhados adicionados só serão cadastrados ao clicar em
                    "Cadastrar"</small
                >
            </p>
        </div>
        <div class="d-flex justify-content-between my-3">
            <button @click="goBack" class="btn btn-secondary">Voltar</button>
            <button v-if="sharedId" @click="excludeSharedPlace" class="btn btn-danger">
                Excluir
            </button>
            <button v-if="sharedId" @click="updateSharedPlace" class="btn btn-primary">
                Salvar
            </button>
            <button v-else @click="registerSharedPlaces" class="btn btn-primary">Cadastrar</button>
        </div>
        <div v-if="listSharedPlacesRegister.length > 0">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Identificador</th>
                            <th scope="col">capacidade</th>
                            <th scope="col">Opções</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(shared, i) in listSharedPlacesRegister" :key="i" scope="col">
                            <td>{{ shared.identifier }}</td>
                            <td>{{ shared.capacity }}</td>
                            <td>
                                <div class="d-flex justify-content-end">
                                    <button
                                        @click="complementModalBody = shared"
                                        class="btn btn-secondary py-0 px-1 mx-1"
                                        data-bs-toggle="modal"
                                        data-bs-target="#complementModal"
                                    >
                                        <small><i class="bi bi-file-text"></i></small>
                                    </button>
                                    <button
                                        @click="deleteSharedPlace(i)"
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
                        <p>
                            <strong>Capacidade máxima:</strong> {{ complementModalBody?.capacity }}
                        </p>
                        <p>
                            <strong>Permite reservas:</strong>
                            {{ complementModalBody?.is_reserveable ? 'Sim' : 'Não' }}
                        </p>
                        <p v-if="complementModalBody?.clean_time">
                            <strong>Tempo de limpeza após uso (HH:MM):</strong>
                            {{ Math.floor(complementModalBody.clean_time / 60) }}:{{
                                complementModalBody.clean_time % 60
                            }}
                        </p>
                        <p v-else><strong>Tempo de limpeza após uso:</strong> 0</p>
                        <p><strong>Descrição:</strong> {{ complementModalBody?.complement }}</p>
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
import type { SharedPlace } from '../interfaces'
import { useRouter } from 'vue-router'
import type { Input, Options } from '@/components/forms/interfaces'

const router = useRouter()
const inputs = app.ref<Input[]>([
    {
        reference: 'identifier',
        label: 'Identificador',
        size: 'bit',
        type: 'text',
        placeholder: 'Ex: Salão, Quadra'
    },
    {
        reference: 'capacity',
        label: 'Capacidade máxima',
        size: 'sm',
        type: 'text'
    },
    {
        reference: 'is_reserveable',
        label: 'Permite reservas',
        size: 'sm',
        type: 'check'
    },
    {
        reference: 'clean_time',
        label: 'Tempo de limpeza após uso (HH:MM)',
        size: 'sm',
        type: 'text',
        mask: '##:##',
        placeholder: 'Ex: 01:30'
    },
    {
        reference: 'complement',
        label: 'Descrição',
        size: 'xl',
        type: 'textarea'
    }
])
const sharedId = app.ref(app.routeParam('id'))
const condominiumId = app.routeQuery('condominium')
const complementModalBody = app.ref<SharedPlace>()

if (!sharedId.value) {
    inputs.value.splice(1, 0, {
        reference: 'sufix',
        label: 'Sufixo',
        size: 'bit',
        type: 'text',
        placeholder: 'Ex: 101, 102, a1...'
    })
}

const sharedForm = app.ref<{ [key: string]: string }>({
    identifier: '',
    sufix: '',
    capacity: '',
    is_reserveable: '',
    clean_time: '',
    complement: ''
})

const listSharedPlacesRegister = app.ref<SharedPlace[]>([])

function addSharedPlace() {
    let identifier = sharedForm.value.identifier + sharedForm.value.sufix

    identifier = identifier.trim()
    if (!identifier) {
        app.popup('Erro!', 'Não foi inserido identificador', 'warning')
        return
    }

    if (listSharedPlacesRegister.value.some((shared) => shared.identifier === identifier)) {
        app.popup('Erro!', 'Já existe um espaço compartilhado com esse identificador.', 'warning')
        return
    }
    const hourCleanTime = sharedForm.value.clean_time.slice(0, 2)
    const minCleanTime = sharedForm.value.clean_time.slice(3, 5)
    const clean_time = Number(hourCleanTime) * 60 + Number(minCleanTime)

    const newSharedPlace = <SharedPlace>{
        complement: sharedForm.value.complement,
        identifier: identifier,
        capacity: Number(sharedForm.value.capacity),
        is_reserveable: Boolean(sharedForm.value.is_reserveable),
        clean_time: clean_time
    }

    listSharedPlacesRegister.value.push(newSharedPlace)

    if (Number(sharedForm.value.sufix)) {
        const newSufix = String(Number(sharedForm.value.sufix) + 1)
        sharedForm.value.sufix = newSufix
    }
    console.log(listSharedPlacesRegister.value)
}

function excludeSharedPlace() {
    app.loading(true, 'Excluindo...')
    app.api
        .delete(`/place/shared/${sharedId.value}/`)
        .then(() => {
            app.popup('Excluido', 'Espaço compartilhado excluido com sucesso')
            app.api.clearStartPath('/place/shared/?condominium=' + sharedForm.value.condominium)
            router.push('/condominio/' + sharedForm.value.condominium)
        })
        .catch((error) => {
            app.popup('Erro', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function deleteSharedPlace(i: number) {
    listSharedPlacesRegister.value.splice(i, 1)
}

function registerSharedPlaces() {
    if (!condominiumId) {
        app.popup('Erro!', 'Condomínio não identificado', 'danger')
    }
    app.loading(true, 'Cadastrando...')
    const payload = {
        condominium_id: condominiumId,
        shareds: listSharedPlacesRegister.value
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

function updateSharedPlace() {
    app.loading(true, 'Atualizando...')
    app.api
        .patch(`/place/shared/${sharedId.value}/`, sharedForm.value)
        .then(({ data }) => {
            app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
            app.api.removeListCash('/place/shared/?condominium=' + sharedForm.value.condominium)
            router.push('/condominio/' + sharedForm.value.condominium)
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
    if (sharedId.value) {
        await getSharedPlaceValues()
        return
    }
})

async function getSharedPlaceValues() {
    app.api
        .get(`/place/shared/${sharedId.value}/`)
        .then(({ data }) => {
            sharedForm.value = data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}
</script>
