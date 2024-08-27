<template>
    <nav-bar/>
    <div class="container mt-5">
        <h2>Register Request</h2>
        
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

        <button @click="registerRequest" class="btn btn-primary">Cadastrar</button>
    </div>
</template>

<script lang="ts" setup>
import NavBar from '@/components/template/NavBar.vue'
import { ref, onMounted  } from 'vue'
import { api } from '@/http'

const places = ref([]);

const requestForm = ref({
    place: null,
    title: '',
    description: '',
    type: null
});

function registerRequest() {
    api.post('/request/', requestForm.value)
}

onMounted(() => {
    api.get('/place/residents/')
    .then(response => {
        places.value = response.data;
    })
    .catch(error => {
        console.error("Erro ao obter a lista de locais:", error);
    });
});

</script>
