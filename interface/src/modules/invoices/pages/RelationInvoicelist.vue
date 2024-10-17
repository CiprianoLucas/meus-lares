<template>
    <div class="container mt-5">
        <h1 class="text-center">Relacionamento das faturas</h1>
        <a href="/fatura/relacao/cadastro" class="btn btn-primary mx-3 m-3">Cadastrar</a>
        
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
import app from '@/app'
import { type InvoiceRelation } from '../interfaces'
const invoicesRelations = app.ref<InvoiceRelation[]>([]);
const url = "/invoice/relation-invoices/"

function exclude(id: string) {
    app.api.delete(url + id)
    .then(() => {
        invoicesRelations.value = invoicesRelations.value.filter(invoice => invoice.id !== id);
        app.popup("Sucesso!", "Relação de faturas excluido.", "warning")
        sessionStorage.removeItem(url)
    })
    .catch(error => {
        app.popup("Erro!", "Falha ao excluir relação de faturas", "warning")
    });
}

app.onMounted(() => {
    app.api.getCashed<InvoiceRelation[]>(url)
    .then(response => {
        invoicesRelations.value = response;
    })
    .catch(error => {
        app.popup("Erro!", "Falha ao listar relações de faturas", "warning")
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
