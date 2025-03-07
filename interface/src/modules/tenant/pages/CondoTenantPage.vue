<template>
    <div>
        <div
            class="border-bottom d-flex flex-column justify-content-center align-items-center py-2"
        >
            <h2>{{ tenant.user_details?.full_name }}</h2>
        </div>
        <div
            class="border-bottom d-flex flex-column justify-content-center align-items-center py-2"
        >
            <img
                v-if="tenant.user_details?.self_photo"
                :src="tenant.user_details.self_photo"
                alt="foto de perfil do usuário"
                class="user-img"
            />
        </div>
        <div class="border-bottom mb-3 py-2">
            <div class="d-flex justify-content-center pb-3">
                <h3 class="p-0 m-0">Dados do usuário</h3>
            </div>
            <dl>
                <dt>Como quer ser chamado:</dt>
                <dd>{{ tenant.user_details?.nick }}</dd>
                <dt>Nome completo:</dt>
                <dd>{{ tenant.user_details?.full_name }}</dd>
                <dt>CPF:</dt>
                <dd>{{ tenant.user_details?.cpf }}</dd>
                <dt>Data de nascimento:</dt>
                <dd>{{ tenant.user_details?.birth }}</dd>
                <dt>Telefone:</dt>
                <dd>{{ tenant.user_details?.phone_number }}</dd>
                <dt>Email:</dt>
                <dd>{{ tenant.user_details?.email }}</dd>
                <dt>Documentos verificados:</dt>
                <dd>{{ verifiedStatusMap[tenant.user_details?.verified_status || 'pending'] }}</dd>
            </dl>
        </div>
        <div class="border-bottom mb-3 py-2">
            <div class="d-flex justify-content-center pb-3">
                <h3 class="p-0 m-0">Apartamento</h3>
            </div>
            <dl>
                <dt>Condomínio:</dt>
                <dd>{{ tenant.apartment_details?.condominium_details?.name }}</dd>
                <dt>Apartamento:</dt>
                <dd>{{ tenant.apartment_details?.identifier }}</dd>
            </dl>
        </div>
        <div class="border-bottom mb-3 py-2">
            <div class="d-flex justify-content-center pb-3">
                <h3 class="p-0 m-0">Relações</h3>
            </div>
            <dl>
                <dt>Responsável:</dt>
                <dd>{{ tenant.is_responsible?"Sim":"Não" }}</dd>
                <dt>Primeiro contato:</dt>
                <dd>{{ tenant.is_first_contact?"Sim":"Não" }}</dd>
                <dt>Locador:</dt>
                <dd>{{ tenant.is_renter?"Sim":"Não" }}</dd>
                <dt>Contrato:</dt>
                <dd>{{ tenant.is_renter?"Sim":"Não" }}</dd>
            </dl>
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
import { formatCPF, formatDate, formatPhoneNumber } from '@/components/formaters'
import type { Tenant } from '@/modules/tenant/interfaces'
import { verifiedStatusMap } from '@/modules/user/interfaces'

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
            if (tenant.value.user_details) {
                const user = tenant.value.user_details
                tenant.value.user_details.birth = formatDate(user.birth)
                tenant.value.user_details.cpf = formatCPF(user.cpf)
                tenant.value.user_details.phone_number = formatPhoneNumber(user.phone_number)
            }
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do morados', 'warning')
        })
}
</script>
