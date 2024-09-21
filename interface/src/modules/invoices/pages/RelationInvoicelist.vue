<template>
    <div class="container mt-5">
        <h1 class="text-center">Relacionamento das faturas</h1>
        <a href="/fatura/relacao/cadastro" class="btn btn-primary mx-3">Cadastrar</a>
        
        <div v-if="invoicesRelations.length === 0" class="alert alert-info text-center">
            Nenhum local disponível no momento.
        </div>

        <div v-else>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Morador</th>
                        <th>Local</th>
                        <th>Empresa</th>
                        <th>Unidade</th>
                        <th>Editar</th>
                        <th>Excluir</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="invoiceRelation in invoicesRelations" :key="invoiceRelation.id">
                        <td>{{ invoiceRelation.resident_name }}</td>
                        <td>{{ invoiceRelation.place_name }}</td>
                        <td>{{ invoiceRelation.company }}</td>
                        <td>{{ invoiceRelation.unit_number }}</td>
                        <td><a :href="`/fatura/relacao/${invoiceRelation.id}`">Editar</a></td>
                        <td><a href='#' @click="exclude(invoiceRelation.id)">Excluir</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { api } from '@/http'
import { type InvoiceRelation } from '../interfaces'
const invoicesRelations = ref<InvoiceRelation[]>([]);

function exclude(id: string) {
    api.delete(`/invoice/relation-invoices/${id}/`)
    .then(() => {
        invoicesRelations.value = invoicesRelations.value.filter(invoice => invoice.id !== id);
    })
    .catch(error => {
        console.error("Erro ao excluir a relação de fatura:", error);
    });
}

onMounted(() => {
    api.get('/invoice/relation-invoices/')
    .then(response => {
        invoicesRelations.value = response.data;
    })
    .catch(error => {
        console.error("Erro ao obter a lista de locais:", error);
    });
});
</script>

<style scoped>
.text-center {
    text-align: center;
}
.table {
    margin-top: 20px;
}
</style>
