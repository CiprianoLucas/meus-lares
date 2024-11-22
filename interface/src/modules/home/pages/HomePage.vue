<template>
    <div class="container mt-5">
        <h1 class="text-center">Bem-vindo ao Sistema de Gestão de Condomínios</h1>
        <p class="text-center">Gerencie seus chamados de manutenção e reclamação de forma simples e eficiente.</p>
        <div>
            <div v-if="isResident" class="row mt-5">
                <h2 class="text-center">Para você residente</h2>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Meus Chamados</h5>
                            <p class="card-text">Visualize e acompanhe seus chamados de manutenção e reclamação.</p>
                            <router-link to="/requisicao/minhas-requisicoes" class="btn btn-primary">Ver Chamados</router-link>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Criar Novo Chamado</h5>
                            <p class="card-text">Abra um novo chamado de manutenção ou reclamação.</p>
                            <router-link to="/requisicao/cadastro" class="btn btn-primary">Criar Chamado</router-link>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Faturas</h5>
                            <p class="card-text">Visualize todas as suas faturas.</p>
                            <router-link to="/fatura/lista" class="btn btn-primary">Visualizar</router-link>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="isUnion" class="row mt-5">
                <h2 class="text-center">Para você síndico ou representante</h2>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Chamados Abertos</h5>
                            <p class="card-text">Veja todos os chamados abertos no condomínio.</p>
                            <router-link to="/requisicao/pendentes" class="btn btn-primary">Ver Chamados Abertos</router-link>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Chamados capturados</h5>
                            <p class="card-text">Veja os chamados que você está responsável</p>
                            <router-link to="/requisicao/capturados" class="btn btn-primary">Ver chamados capturados</router-link>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h5 class="card-title">Configurações do Condomínio</h5>
                            <p class="card-text">Gerencie as configurações do seu condomínio.</p>
                            <router-link to="/condominio/lista" class="btn btn-secondary">Configurações</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import app from '@/app'

    const username = app.ref<string | null>(null)
    const isResident = app.ref(false)
    const isUnion = app.ref(false)

    app.onMounted(() => {
        username.value = localStorage.getItem("username")
        isResident.value = !!localStorage.getItem("isResident")
        isUnion.value = !!localStorage.getItem("isUnion")
    })

</script>

<style scoped>
.text-center {
    text-align: center;
}
.card {
    margin-bottom: 20px;
}
</style>