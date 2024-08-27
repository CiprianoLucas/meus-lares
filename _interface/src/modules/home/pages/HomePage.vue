<template>
    <nav-bar/>
    <div class="container mt-5">
        <h1 class="text-center">Bem-vindo ao Sistema de Gestão de Condomínios</h1>
        <p class="text-center">Gerencie seus chamados de manutenção e reclamação de forma simples e eficiente.</p>

        <div class="row mt-5">
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">Meus Chamados</h5>
                        <p class="card-text">Visualize e acompanhe seus chamados de manutenção e reclamação.</p>
                        <router-link to="/meus-chamados" class="btn btn-primary">Ver Chamados</router-link>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">Criar Novo Chamado</h5>
                        <p class="card-text">Abra um novo chamado de manutenção ou reclamação.</p>
                        <router-link to="/novo-chamado" class="btn btn-primary">Criar Chamado</router-link>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">Chamados Abertos</h5>
                        <p class="card-text">Veja todos os chamados abertos no condomínio.</p>
                        <router-link to="/chamados-abertos" class="btn btn-primary">Ver Chamados Abertos</router-link>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-4 offset-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">Configurações do Condomínio</h5>
                        <p class="card-text">Gerencie as configurações do seu condomínio.</p>
                        <router-link to="/configuracoes" class="btn btn-secondary">Configurações</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import NavBar from '@/components/template/NavBar.vue'

</script>

<style scoped>
.text-center {
    text-align: center;
}
.card {
    margin-bottom: 20px;
}
</style>