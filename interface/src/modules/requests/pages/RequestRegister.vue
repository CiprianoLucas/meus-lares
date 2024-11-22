<template>
    <div class="container mt-5">
        <h1 class="text-center">Registrar chamado</h1>
        
        <div class="mb-3">
            <label for="place" class="form-label">Local:</label>
            <select 
                class="form-control" 
                id="place" 
                v-model="requestForm.place" 
                required
            >
                <option v-for="place in places" :key="place.id" :value="place.id">
                    {{ place.name }} - {{ place.street }}, {{ place.number }}, {{ place.city }} - {{ place.state }}
                </option>
            </select>
        </div>

        <div class="mb-3">
            <label for="title" class="form-label">Título:</label>
            <input 
                type="text" 
                class="form-control" 
                id="title" 
                v-model="requestForm.title" 
                required 
            />
        </div>

        <div class="mb-3">
            <label for="description" class="form-label">Descrição:</label>
            <textarea 
                class="form-control" 
                id="description" 
                v-model="requestForm.description" 
                rows="3" 
                required 
            ></textarea>
        </div>

        <div class="mb-3">
            <label for="type" class="form-label">Tipo:</label>
            <select 
                class="form-control" 
                id="type" 
                v-model="requestForm.type" 
                required
            >
                <option value="R">RECLAMAÇÃO</option>
                <option value="M">MANUTENÇÃO</option>
                <option value="O">OUTROS</option>
            </select>
        </div>

        <button v-if="!requestId" @click="registerRequest" class="btn btn-primary">Cadastrar</button>
        <button v-else @click="updatePlace" class="btn btn-primary mx-3">Atualizar</button>
    </div>
</template>

<script lang="ts" setup>

import app from '@/app'
import { type Place } from '../../places/interfaces'

const requestId = app.ref(app.routeParam('id'))

const places = app.ref<Place[]>([])

const requestForm = app.ref({
    place: null,
    title: '',
    description: '',
    type: null
})

function registerRequest() {
    app.api.post('/request/', requestForm.value)
    .then(({data})=>{
        sessionStorage.removeItem('/request/residents/')
		app.redirect('/requisicao/minhas-requisicoes')
	})
    .catch((error)=>{
        app.popup('Erro!', app.resumeErrors(error), 'warning', 10000)
    })
}

function updatePlace() {
        app.api.put(`/request/${requestId.value}/`, requestForm.value)
        .then(()=> {
            sessionStorage.removeItem('/request/residents/')
		    app.redirect('/requisicao/minhas-requisicoes')
        })
        .catch(error =>{
            app.popup('Erro!', app.resumeErrors(error), 'warning', 10000)
        })
    }

app.onMounted(() => {
    app.api.getCashed<Place[]>('/place/residents/')
    .then(response => {
        places.value = response
    })
    .catch(() => {
        app.popup('Erro!', 'Falha ao obter o locais', 'warning')
    })

    if (requestId.value){
        app.api.get(`/request/${requestId.value}/`)
        .then(response => {
            requestForm.value = response.data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter o chamado', 'warning')
        })
    }
})

</script>
