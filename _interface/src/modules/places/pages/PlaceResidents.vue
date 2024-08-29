<template>
  <div class="container mt-5">
    <h1 class="text-center">Residentes</h1>

    <!-- Input para adicionar novo residente -->
    <div class="input-group mb-3">
      <input
        type="email"
        class="form-control"
        v-model="newResidentEmail"
        placeholder="Digite o email do residente"
        aria-label="Email do Residente"
        aria-describedby="button-addon2"
      />
      <button
        class="btn btn-primary"
        type="button"
        id="button-addon2"
        @click="addResident"
        :disabled="!newResidentEmail"
      >
        Adicionar
      </button>
    </div>

    <!-- Mensagem de erro ao adicionar -->
    <div v-if="errorMessage" class="alert alert-danger text-center">
      {{ errorMessage }}
    </div>

    <!-- Tabela de residentes -->
    <div v-if="residents.length === 0" class="alert alert-info text-center">
      Nenhum residente encontrado.
    </div>

    <div v-else>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Ação</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="resident in residents" :key="resident.id">
            <td>{{ resident.username }}</td>
            <td>{{ resident.email }}</td>
            <td>
              <a @click="deleteResident(resident.id)" >excluir</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { api } from "@/http";
import { useRoute } from "vue-router";

const residents = ref([]);
const newResidentEmail = ref("");
const errorMessage = ref("");
const route = useRoute();
const placeId = ref(route.params.id)

onMounted(() => {
  fetchResidents();
});

function fetchResidents() {
  api
    .get(`/place/${placeId.value}/residents/`)
    .then((response) => {
      residents.value = response.data;
    })
    .catch((error) => {
      console.error("Erro ao obter a lista de residentes:", error);
    });
}

function deleteResident(userId: string) {
  api
    .delete(`/place/${placeId.value}/residents/${userId}`)
    .then(() => {
      residents.value = residents.value.filter((resident) => resident.id !== userId);
    })
    .catch((error) => {
      console.error("Erro ao deletar o residente:", error);
    });
}

function addResident() {

  api
    .post(`/place/${placeId.value}/residents/`, { email: newResidentEmail.value })
    .then((response) => {
      residents.value.push(response.data); // Assume que o servidor retorna o residente criado
      newResidentEmail.value = "";
      errorMessage.value = ""; // Limpa mensagem de erro, se houver
    })
    .catch((error) => {
      console.error("Erro ao adicionar o residente:", error);
      errorMessage.value =
        "Não foi possível adicionar o residente. Verifique o email e tente novamente.";
    });
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
.table {
  margin-top: 20px;
}
.btn-danger {
  color: white;
}
</style>
