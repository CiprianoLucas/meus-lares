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
import app from '@/app'
import { type User } from "../../user/interfaces"

const unions = app.ref<User[]>([]);
const newUnionEmail = app.ref("");
const errorMessage = app.ref("");
const route = app.useRoute();
const placeId = app.ref(route.params.id)
const url = `/place/${placeId.value}/unions/`
const inputs = {
  email: "Email"
}

app.onMounted(() => {
  fetchUnions();
});

function fetchUnions() {
  app.api.getCashed<User[]>(url)
    .then((response) => {
      unions.value = response;
    })
    .catch((error) => {
      app.popup("Erro!", "Erro ao obter a lista de síndicos.", "warning")
    });
}

function deleteUnion(userId: string) {
	app.api.delete(`/place/${placeId.value}/unions/${userId}`)
		.then(() => {
			unions.value = unions.value.filter((resident) => resident.id !== userId);
      sessionStorage.removeItem(url)
      app.popup("Sucesso!", "Síndico deletado", "success")
		})
		.catch((error) => {
      app.popup("Erro!", "Erro ao deletar o síndico.", "warning")
		});
}

function addUnion() {

  app.api.post(`/place/${placeId.value}/unions/`, { email: newUnionEmail.value })
		.then((response) => {
			unions.value.push(response.data)
			newUnionEmail.value = ""
			errorMessage.value = ""
      sessionStorage.removeItem(url)
      app.popup("Sucesso!", "Síndico cadastrado", "success")
		})
		.catch((error) => {
			app.popup("Erro!", app.resumeErrors(error, inputs), "warning")
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
