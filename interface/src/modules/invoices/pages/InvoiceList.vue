<template>
    <div class="container mt-5">
        <h1 class="text-center">Relacionamento das faturas</h1>

        <div v-if="invoices.length === 0" class="alert alert-info text-center">
            Nenhum local disponível no momento.
        </div>

        <div v-else>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Empresa</th>
                        <th>Valor</th>
                        <th>nº boleto</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="invoice in invoices" :key="invoice.id">
                        <td>{{ invoice.company }}</td>
                        <td>{{ 'R$ ' + invoice.value.toLocaleString('pt-BR') }}</td>
                        <td>{{ invoice.ticket_number }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { type Invoice } from '../interfaces'
const invoices = app.ref<Invoice[]>([])

app.onMounted(() => {
    app.api
        .getCashed<Invoice[]>('/invoice/invoices/')
        .then((response) => {
            invoices.value = response
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao listar as faturas', 'warning')
        })
})
</script>

<style scoped>
.text-center {
    text-align: center;
}
.table {
    margin-top: 20px;
}
</style>
