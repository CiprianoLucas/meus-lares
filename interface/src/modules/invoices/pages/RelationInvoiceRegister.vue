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
    import app from '@/app'
    import { type Place } from '../../places/interfaces'
    import { type User } from '../../user/interfaces'
    import { companyMap } from '../interfaces'
    
	const route = app.useRoute();
	const router = app.useRouter();
	const invoiceRelationId = app.ref(route.params.id);
    const places = app.ref<Place[]>([]);
    const residents = app.ref<User[]>([]);

    const invoiceRelationForm = app.ref({
        company: '',
        unit_number: '',
        resident: '',
        place: '',
    });

    function updateSelectRedidents() {
        app.api.getCashed<User[]>(`/place/${invoiceRelationForm.value.place}/residents/`)
		.then(response => {
            residents.value = response;
        })
        .catch(error => {
            app.popup("Erro!", "Falha ao listar os moradores", "warning")
        });
    }

    function registerInvoiceRelation() {
        app.api.post('/invoice/relation-invoices/', invoiceRelationForm.value)
		.then(({data})=>{
            sessionStorage.removeItem("/invoice/relation-invoices/")
            app.popup("Sucesso!", "Relação de fatura salvo", "success")
			router.push('/fatura/relacao-lista')
		})
        .catch(error=> {
            app.popup("Erro!", app.resumeErrors(error), "warning")
        })
    };

	function updateInvoiceRelation() {
        app.api.put(`/invoice/relation-invoices/${invoiceRelationId.value}/`, invoiceRelationForm.value)
        .then(response =>{
            sessionStorage.removeItem("/invoice/relation-invoices/")
            app.popup("Sucesso!", "Relação de fatura salvo", "success")
			router.push('/fatura/relacao-lista')
        })
        .catch(error=>{
            app.popup("Erro!", app.resumeErrors(error), "warning")
        })
    };

	app.onMounted(() => {
        app.api.getCashed<Place[]>('/place/unions/')
        .then(response => {
            places.value = response;
        })
        .catch(error => {
            app.popup("Erro!", "Falha ao buscar lista de locais", "warning")
        });
		if (invoiceRelationId.value){
			app.api.get(`/invoice/relation-invoices/${invoiceRelationId.value}/`)
			.then(response => {
				invoiceRelationForm.value = response.data;
                updateSelectRedidents()
			})
			.catch(() => {
				app.popup("Erro!", "Falha ao buscar informações dessa relação de faturas", "warning")
			});
		}
	});

</script>