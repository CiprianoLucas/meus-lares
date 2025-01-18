<template>
    <div class="d-flex justify-content-center my-2">
        <button class="btn btn-secondary py-2 px-3 w-100" type="button" @click="onChangeCollapse">
            Apartamentos
        </button>
    </div>
    <div>
        <div class="collapse" ref="listHtml">
            <list-table :url="'/place/apartment/?condominium=' + condominiumId" :headers="headers"
                :column-path="columnPath" :param-path="paramPath" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { Collapse } from 'bootstrap';
import app from '@/app';
import ListTable from '@/components/tables/ListTable.vue';

const listHtml = app.ref<HTMLElement>();
const listCollapse = app.ref<Collapse | null>(null);
const headers = app.ref({
    'tenant': null,
    'id': null,
    'identifier': "Identificador",
    'tenant_name': "Morador"
})

const columnPath = app.ref({
    'identifier': "place/apartment/:apartmentId",
    'tenant_name': "relation/tenant/:tenantId"
})

const paramPath = app.ref({
    ':tenantId': "tenant",
    ':apartmentId': "id"
})

const props = defineProps<{
    condominiumId: string
}>()

function onChangeCollapse() {
    listCollapse.value?.toggle()
}

app.onMounted(() => {
    if (listHtml.value) {
        listCollapse.value = new Collapse(listHtml.value, { toggle: false });
    }
});


</script>

<style></style>