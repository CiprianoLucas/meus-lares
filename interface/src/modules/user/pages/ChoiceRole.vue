<template>
    <div class="mt-4">
        <div v-if="user.roles.length > 0" class="d-flex justify-content-center align-items-center ">
            <h2>Qual perfil deseja acessar?</h2>
        </div>
        <div class="row">
            <div v-if="user.roles.length == 0">
                <div class="d-flex justify-content-center align-items-center border rounded p-3 mt-3">
                    <p class="text-center">
                        Não identificamos registros no seu nome em qualquer modelo de perfil.<br><br>
                        Passe seu e-mail para o responsável do condomínio para registra-lo.<br><br>
                        Verifique nas notificações ou em seu email se não há uma solicitação de registro para ser
                        aprovada.
                    </p>
                </div>
            </div>
            <div v-if="user.roles.includes('tenant')" class="col-6 p-3">
                <router-link to="/morador" @click="userstore.role = 'tenant'" class="text-white text-decoration-none">
                    <div class="card d-flex justify-content-center align-items-center">
                        <img src="https://static.vecteezy.com/ti/vetor-gratis/p1/6883355-inquilinos-casa-residentes-icone-em-branco-vetor.jpg"
                            class="card-img-top" alt="morador">
                        <div class="card-body">
                            <h5 class="card-title">Morador</h5>
                        </div>
                    </div>
                </router-link>
            </div>
            <div v-if="user.roles.includes('owner')" class="col-6 p-3">
                <router-link to="/proprietario" @click="userstore.role = 'owner'"
                    class="text-white text-decoration-none">
                    <div class="card d-flex justify-content-center align-items-center">
                        <img src="https://cdn-icons-png.flaticon.com/512/2098/2098368.png" class="card-img-top"
                            alt="morador">
                        <div class="card-body">
                            <h5 class="card-title">Proprietário</h5>
                        </div>
                    </div>
                </router-link>
            </div>
        </div>
        <router-link v-if="!user.roles.includes('owner')" to="/condominio/cadastro" class="btn btn-primary mt-3">
                    Quer administrar seu próprio condomínio? Então clique aqui!
        </router-link>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { userStore } from '../stores';
import { onBeforeMount } from 'vue';

const userstore = userStore()
const user = app.ref(userstore)

onBeforeMount(() => {
    app.api.get("/user/roles/").then(({ data }) => {
        userstore.roles = data.roles
        user.value = userstore
    }).catch(() => {
        app.popup('Erro!', 'Falha ao obter a lista de perfis', 'warning')
    })
})

</script>