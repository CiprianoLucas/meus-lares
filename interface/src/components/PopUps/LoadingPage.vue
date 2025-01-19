<template>
    <transition name="fade">
        <div v-if="visible" class="loading-page">
            <div class="loading-content">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p v-if="message" class="loading-message text-dark">{{ message }}</p>
            </div>
        </div>
    </transition>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import { loagingPageStore } from '../template/Loading/stores';

const loading = loagingPageStore()

const visible = ref(loading.show);
const message = ref(loading.message);

watch(
    () => loading.show,
    (newValue) => {
        visible.value = newValue;
        message.value = loading.message;
    }
);
</script>

<style scoped>
.loading-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(225, 225, 225, 0.99);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9998;
}

.loading-content {
    text-align: center;
    color: white;
}

.loading-message {
    margin-top: 10px;
    font-size: 1.2rem;
}
</style>