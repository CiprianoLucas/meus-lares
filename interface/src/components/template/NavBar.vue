<template>
  <aside class="bg-dark text-white py-3 fixed-left vh-100">
    <div class="container d-flex flex-column align-items-start">
      <nav>
        <router-link class="mb-3 text-white text-decoration-none d-block" to="/"
          >Página inicial</router-link
        >
        <router-link
          v-if="!username"
          class="mb-3 text-white text-decoration-none d-block"
          to="/login"
          >Login</router-link
        >
        <router-link
          v-if="!username"
          class="mb-3 text-white text-decoration-none d-block"
          to="/usuario/cadastro"
          >Registrar</router-link
        >

        <div class="dropdown my-5" v-if="isResident">
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/requisicao/cadastro"
            >Abrir solicitação</router-link
          >
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/requisicao/minhas-requisicoes"
            >Visualizar solicitações</router-link
          >
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/fatura/lista"
            >Faturas</router-link
          >
        </div>
        <div class="dropdown my-5" v-if="isUnion">
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/requisicao/pendentes"
            >Solicitações pendentes</router-link
          >
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/requisicao/capturados"
            >Solicitações capturadas</router-link
          >
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/fatura/relacao-lista"
            >Relacionamento das faturas</router-link
          >
          <router-link
            class="mb-3 text-white text-decoration-none d-block"
            to="/condominio/lista"
            >Configurações</router-link
          >
        </div>
        <router-link
          v-if="!!username"
          class="my-5 text-white text-decoration-none d-block"
          to="/ai/"
          >Inteligência artificial</router-link
        >
        <router-link
          v-if="!!username"
          class="my-5 text-white text-decoration-none d-block"
          to="/condominio/cadastro"
          >Cadastrar condomínio</router-link
        >
        <a
          v-if="!!username"
          class="my-5 text-white text-decoration-none d-block"
          @click="logout"
          >Logout</a
        >
      </nav>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { api } from "@/http"

const username = ref<string | null>(null)
const isResident = ref(false)
const isUnion = ref(false)

async function logout() {
  await api.logout()
  window.location.reload()
}

onMounted(() => {
  username.value = localStorage.getItem("username")
  isResident.value = !!localStorage.getItem("isResident")
  isUnion.value = !!localStorage.getItem("isUnion")
})
</script>

<script lang="ts">
export default {
  name: "NavBar",
}
</script>

<style>
.fixed-left {
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  overflow-y: auto;
}

body {
  margin-left: 250px;
  padding: 20px;
}
</style>
