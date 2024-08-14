<template>
	<nav-bar/>
	<div class="container">
		<div class="row">
			<div
				v-for="category in categories"
				:key="category.id"
				class="col-lg-3 col-md-4 col-6 mb-4"
			>
				<a href="#" class="text-decoration-none">
					<div class="card border-0 shadow-sm text-center">
						<div class="card-body d-flex flex-column align-items-center justify-content-center p-4">
							<img
								:src="category.icon"
								class="img-fluid mb-3"
								style="height: 50px;"
								:alt="category.name"
							/>
							<h5 class="card-text fw-bold text-dark">{{ category.name }}</h5>
						</div>
					</div>
				</a>
			</div>
		</div>
	</div>
</template>

<script lang="ts" setup>
	import NavBar from '@/components/template/NavBar.vue'
	import { ref, onMounted } from 'vue'
	import { api } from '@/http'

	interface Category {
		id: string
		name: string
		icon: string
	}

	const categories = ref<Category[]>([])

	onMounted(() => {
	})
</script>