<template>
    <nav-bar/>
    <div class="container mt-5">
    <h2>Register Place</h2>
      <div class="mb-3">
        <label for="name" class="form-label">Nome:</label>
        <input 
          type="text" 
          class="form-control" 
          id="name" 
          v-model="placeForm.name" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="number" class="form-label">Número:</label>
        <input 
          type="text" 
          class="form-control" 
          id="number" 
          v-model="placeForm.number" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="street" class="form-label">Rua:</label>
        <input 
          type="text" 
          class="form-control" 
          id="street" 
          v-model="placeForm.street" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="city" class="form-label">Cidade:</label>
        <input 
          type="text" 
          class="form-control" 
          id="city" 
          v-model="placeForm.city" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="state" class="form-label">Estado:</label>
        <input 
          type="text" 
          class="form-control" 
          id="state" 
          v-model="placeForm.state" 
          required 
        />
      </div>

      <button @click="registerPlace" class="btn btn-primary">Cadastrar</button>
  </div>
</template>
  
<script lang="ts" setup>
    import NavBar from '@/components/template/NavBar.vue'
    import { ref } from 'vue'
    import { api } from '@/http'
    
    const placeForm = ref({
        name: '',
        number: '',
        street: '',
        city: '',
        state: ''
    });

    function registerPlace() {
        api.post('/place/', placeForm.value)
    };

</script>