<template>
  <div class="container mt-5">
    <h1 class="text-center">Síndicos</h1>

    <!-- Input para adicionar novo síndico -->
    <div class="input-group mb-3">
      <input
        type="email"
        class="form-control"
        v-model="newUnionEmail"
        placeholder="Digite o email do síndico"
        aria-label="Email do Síndico"
        aria-describedby="button-addon2"
      />
      <button
        class="btn btn-primary"
        type="button"
        id="button-addon2"
        @click="addUnion"
        :disabled="!newUnionEmail"
      >
        Adicionar
      </button>
    </div>

    <!-- Mensagem de erro ao adicionar -->
    <div v-if="errorMessage" class="alert alert-danger text-center">
      {{ errorMessage }}
    </div>

    <!-- Tabela de síndicos -->
    <div v-if="unions.length === 0" class="alert alert-info text-center">
      Nenhum síndico encontrado.
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
          <tr v-for="resident in unions" :key="resident.id">
            <td>{{ resident.username }}</td>
            <td>{{ resident.email }}</td>
            <td>
              <a @click="deleteUnion(resident.id)" >excluir</a>
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

const unions = ref([]);
const newUnionEmail = ref("");
const errorMessage = ref("");
const route = useRoute();
const placeId = ref(route.params.id)

onMounted(() => {
  fetchUnions();
});

function fetchUnions() {
  api
    .get(`/place/${placeId.value}/unions/`)
    .then((response) => {
      unions.value = response.data;
    })
    .catch((error) => {
      console.error("Erro ao obter a lista de síndicos:", error);
    });
}

function deleteUnion(userId: string) {
  api
    .delete(`/place/${placeId.value}/unions/${userId}`)
    .then(() => {
      unions.value = unions.value.filter((resident) => resident.id !== userId);
    })
    .catch((error) => {
      console.error("Erro ao deletar o síndico:", error);
    });
}

function addUnion() {

  api
    .post(`/place/${placeId.value}/unions/`, { email: newUnionEmail.value })
    .then((response) => {
      unions.value.push(response.data)
      newUnionEmail.value = ""
      errorMessage.value = ""
    })
    .catch((error) => {
      console.error("Erro ao adicionar o síndico:", error);
      errorMessage.value =
        "Não foi possível adicionar o síndico. Verifique o email e tente novamente."
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
