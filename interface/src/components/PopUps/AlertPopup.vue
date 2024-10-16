<template>
    <transition>
        <div v-if="visible" class="popup">
            <div :class="`alert alert-${type} alert-dismissible`" role="alert">
                <strong >{{ title }}</strong><br><p v-html="message"></p>
                <button type="button" class="btn-close" aria-label="Fechar" @click="forceRemovePopup"></button>
            </div>
        </div>
    </transition>
</template>
  
<script lang="ts" setup>
    import {ref} from 'vue'
    import type {typesBootstrap} from './interfaces'
  
    const props = defineProps<{
        title: string;
        message: string;
        type: typesBootstrap;
        time: number
    }>();
    
    const visible = ref(false);
    const type = props.type;
    const time = props.time;
    const title = props.title;
    const message = props.message;


    
    const removePopup = () => {
        visible.value = false;
    };

    const forceRemovePopup = () => {
        const popupElement = document.querySelector('.popup');
        if (popupElement) {
            popupElement.remove();
        }
    }

    setTimeout(() => {
        visible.value = true;
    }, 1);
    
    setTimeout(() => {
        removePopup();
    }, time);

</script>
  
<style scoped>
    .popup {
        position: fixed;
        bottom: 1rem;
        right: 1rem;
        padding: 1rem;
    }

    .v-enter-active{
        transition: all 0.3s ease;
    }
    .v-leave-active {
        transition: all 1s ease;
    }

    .v-enter-from{
        opacity: 0;
        transform: translateY(100px);
    }
    .v-leave-to {
        opacity: 0;
        transform: translateY(10px);
    }
</style>

  