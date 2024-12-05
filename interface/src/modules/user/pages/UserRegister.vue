<template>
    <div class="container mt-5">
        <h2>Register</h2>
        <div class="mb-3">
            <label for="username" class="form-label">Nome de usuário:</label>
            <input
                type="text"
                class="form-control"
                id="username"
                v-model="userForm.username"
                required
            />
        </div>

        <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input type="email" class="form-control" id="email" v-model="userForm.email" required />
        </div>

        <div class="mb-3">
            <label for="cpf" class="form-label">CPF:</label>
            <input type="text" class="form-control" id="cpf" v-model="userForm.cpf" required />
        </div>

        <div class="mb-3">
            <label for="phone_number" class="form-label">Telefone:</label>
            <input
                type="text"
                class="form-control"
                id="phone_number"
                v-model="userForm.phone_number"
                required
            />
        </div>

        <div class="mb-3">
            <label for="full_name" class="form-label">Nome completo</label>
            <input
                type="text"
                class="form-control"
                id="full_name"
                v-model="userForm.full_name"
                required
            />
        </div>

        <div class="mb-3">
            <label for="password" class="form-label">Senha:</label>
            <input
                type="password"
                class="form-control"
                id="password"
                v-model="userForm.password"
                required
            />
        </div>

        <div class="mb-3">
            <label for="text" class="form-label">Data de nascimento:</label>
            <input type="text" class="form-control" id="birth" v-model="userForm.birth" required />
        </div>

        <button @click="RegisterUser" class="btn btn-primary">Cadastrar</button>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import type { User } from '../interfaces'

const fullName = String(app.routeQuery('full_name')) || ''
const email = String(app.routeQuery('email')) || ''

const userForm = app.ref<User>({
    username: '',
    email: email,
    cpf: '',
    phone_number: '',
    full_name: fullName,
    password: '',
    birth: ''
})

function RegisterUser() {
    app.api
        .post('/user/register/', userForm.value)
        .then(() => {
            app.popup('Sucesso!', 'Usuário cadastrado com sucesso.', 'success')
            app.redirect('/login')
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
}
</script>
