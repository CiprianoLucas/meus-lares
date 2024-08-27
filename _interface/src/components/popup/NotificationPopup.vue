<template>
    <transition name="fade">
        <div v-if="visible" class="notification-popup">
            <p>{{ message }}</p>
        </div>
    </transition>
</template>
  
<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    
    interface Props {
        message: string;
    }
    
    const props = defineProps<Props>();
    
    const visible = ref(true);
    
    onMounted(() => {
        setTimeout(() => {
        visible.value = false;
        }, 5000); // 5 segundos
    });
</script>
  
<style scoped>
    .notification-popup {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #333;
        color: #fff;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    
    .fade-enter-active, .fade-leave-active {
        transition: opacity 0.5s;
    }
    
    .fade-enter, .fade-leave-to /* .fade-leave-active em <2.1.8 */ {
        opacity: 0;
    }
</style>