<template>
    <nav-bar/>
    <div class="container mt-5">
    <h2>Register</h2>
      <div class="mb-3">
        <label for="username" class="form-label">Nome de usuário:</label>
        <input 
          type="text" 
          class="form-control" 
          id="username" 
          v-model="form.username" 
          required 
        />
      </div>
      
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input 
          type="email" 
          class="form-control" 
          id="email" 
          v-model="form.email" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="cpf" class="form-label">CPF:</label>
        <input 
          type="text" 
          class="form-control" 
          id="cpf" 
          v-model="form.cpf" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="phone_number" class="form-label">Telefone:</label>
        <input 
          type="text" 
          class="form-control" 
          id="phone_number" 
          v-model="form.phone_number" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="full_name" class="form-label">Nome completo</label>
        <input 
          type="text" 
          class="form-control" 
          id="full_name" 
          v-model="form.full_name" 
          required 
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Senha:</label>
        <input 
          type="password" 
          class="form-control" 
          id="password" 
          v-model="form.password" 
          required 
        />
      </div>

      <button @click="RegisterUser" class="btn btn-primary">Cadastrar</button>
  </div>
</template>
  
<script lang="ts" setup>
    import NavBar from '@/components/template/NavBar.vue'
    import { ref } from 'vue'
    import { api } from '@/http'
import app from '@/app';
    
    const form = ref({
        username: '',
        email: '',
        cpf: '',
        phone_number: '',
        full_name: '',
        password: ''
    });

    const inputs = {
        username: 'Nome de usuário',
        email: 'Email',
        cpf: 'CPF',
        phone_number: 'Telefone',
        full_name: 'Nome completo',
        password: 'Senha'
    }
    const router = app.useRouter()

    function RegisterUser() {
        api.post('/user/register/', form.value)
        .then(()=>{
          app.popup("Sucesso!", "Usuário cadastrado com sucesso.", 'success')
          router.push('/login');
        })
        .catch((error)=>{
          app.popup("Erro!", app.resumeErrors(error, inputs), 'warning')
        })
    };

</script>