<template>
    <div class="container mt-5">
        <h1 class="text-center">{{ $t("homepage_title") }}</h1>
        <p class="text-center">
            {{ $t("homepage_description") }}
        </p>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'

app.onMounted(() => {})
</script>

<style scoped>
.text-center {
    text-align: center;
}
.card {
    margin-bottom: 20px;
}
</style>
