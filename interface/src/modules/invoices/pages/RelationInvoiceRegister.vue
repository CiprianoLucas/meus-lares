<template>
    <div class="container mt-5">
		<h1 class="text-center">Registrar relação de fatura:</h1>
			<div class="mb-3">
				<label for="company_invoice" class="form-label">Empresa emissora da fatura:</label>
				<select 
                class="form-control" 
                id="company_invoice" 
                v-model="invoiceRelationForm.company" 
                required
                >
                <option v-for="(label, key) in companyMap" :key="key" :value="key">
                    {{ label }}
                </option>
            </select>
			</div>

	<div class="mb-3">
		<label for="place" class="form-label">Lugar:</label>
		<select 
                class="form-control" 
                id="place" 
                v-model="invoiceRelationForm.place" 
                @change="updateSelectRedidents"
                required
            >
                <option v-for="place in places" :key="place.id" :value="place.id">
                    {{ place.name }} - {{ place.street }}, {{ place.number }}, {{ place.city }} - {{ place.state }}
                </option>
            </select>
	</div>

	<div class="mb-3">
		<label for="resident" class="form-label">Morador:</label>
		<select 
                class="form-control" 
                id="resident" 
                v-model="invoiceRelationForm.resident" 
                required
            >
                <option v-for="user in residents" :key="user.id" :value="user.id">
                    {{ user.username }} - {{ user.email }}
                </option>
            </select>
	</div>

	<div class="mb-3">
		<label for="city" class="form-label">Unidade condumidora:</label>
		<input 
			type="text" 
			class="form-control" 
			id="city" 
			v-model="invoiceRelationForm.unit_number" 
			required 
		/>
	</div>
      	<button v-if="!invoiceRelationId" @click="registerInvoiceRelation" class="btn btn-primary">Cadastrar</button>
        <button v-else  @click="updateInvoiceRelation" class="btn btn-primary mx-3">Atualizar</button>
  	</div>
</template>
  
<script lang="ts" setup>
    import { ref, onMounted } from 'vue'
	import { useRoute, useRouter } from 'vue-router'
    import { type Place } from '../../places/interfaces'
    import { type User } from '../../user/interfaces'
    import { api } from '@/http'
    import { companyMap } from '../interfaces'
    
	const route = useRoute();
	const router = useRouter();
	const invoiceRelationId = ref(route.params.id);
    const places = ref<Place[]>([]);
    const residents = ref<User[]>([]);

    const invoiceRelationForm = ref({
        company: '',
        unit_number: '',
        resident: '',
        place: '',
    });

    function updateSelectRedidents() {
        api.get(`/place/${invoiceRelationForm.value.place}/residents/`)
		.then(response => {
            residents.value = response.data;
        })
        .catch(error => {
            console.error("Erro ao obter a lista de moradores:", error);
        });
    }

    function registerInvoiceRelation() {
        api.post('/invoice/relation-invoices/', invoiceRelationForm.value)
		.then(({data})=>{
			invoiceRelationId.value = data.id
			router.push({ name: 'relacao-fatura-lista', params: { id: data.id } })
		})
    };

	function updateInvoiceRelation() {
        api.put(`/invoice/relation-invoices/${invoiceRelationId.value}/`, invoiceRelationForm.value)
    };

	onMounted(() => {
        api.get('/place/unions/')
        .then(response => {
            places.value = response.data;
        })
        .catch(error => {
            console.error("Erro ao obter a lista de locais:", error);
        });
		if (invoiceRelationId.value){
			api.get(`/invoice/relation-invoices/${invoiceRelationId.value}/`)
			.then(response => {
				invoiceRelationForm.value = response.data;
                updateSelectRedidents()
			})
			.catch(error => {
				console.error("Erro ao obter os detalhes do local:", error);
			});
		}
	});

</script>