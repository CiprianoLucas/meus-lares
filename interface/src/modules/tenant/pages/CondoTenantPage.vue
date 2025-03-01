<template>
    <div>
        <div
            class="border-bottom d-flex flex-column justify-content-center align-items-center py-2"
        >
            <h2>{{ tenant.user_full_name }}</h2>
        </div>
        <div class="border-bottom px-4 py-3">
            <div class="d-flex justify-content-between mb-3">
                <h3 class="p-0 m-0">Descrição:</h3>
            </div>
        </div>
        <div class="mb-3">
            <!-- <dl>
                <dt>Nome completo:</dt>
                <dd>{{ tenant?.full_name }}</dd>
                <dt>CPF:</dt>
                <dd>{{ tenant?.cpf }}</dd>
                <dt>Data de nascimento:</dt>
                <dd>{{ tenant?.birth }}</dd>
                <dt>Verificação de identidade:</dt>
                <dd>{{ verifiedStatusMap[tenant?.verified_status || 'pending'] }}</dd>
            </dl> -->
        </div>
        <div class="d-flex justify-content-between border-bottom px-4 pt-2 pb-5">
            <button class="btn btn-danger py-1">Excluir</button>
            <button class="btn btn-warning py-1">
                {{ tenant.is_active ? 'Desativar' : 'Ativar' }}
            </button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import type { Tenant } from '@/modules/tenant/interfaces'

const tenantId = app.ref<string>(app.routeParam('id').toString())
const tenant = app.ref<Tenant>({})

app.onMounted(async () => {
    app.loading(true)
    await getTenantValues()
    app.loading(false)
})

async function getTenantValues() {
    app.api
        .get(`/relation/tenant/${tenantId.value}/`)
        .then(({ data }) => {
            tenant.value = data
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
}
</script>
