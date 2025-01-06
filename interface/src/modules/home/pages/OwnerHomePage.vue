<template>
    <div class="container mt-2">
        <div class="row mt-2">
            <div class="col-6">
                <router-link to="/condominio/lista" class="text-white text-decoration-none">
                    <div class="card d-flex justify-content-center align-items-center p-3">
                        <img src="https://cdn-icons-png.flaticon.com/512/1066/1066153.png"
                            class="card-img-top" alt="morador">
                        <div class="card-body pb-0">
                            <h6 class="card-title mb-0">Condomínios</h6>
                        </div>
                    </div>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'

</script>

<style scoped>
.text-center {
    text-align: center;
}

.card {
    margin-bottom: 20px;
}
</style>
