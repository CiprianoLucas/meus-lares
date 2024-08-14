<template>
    <div>
        <h2>Exemplo de chat</h2>
        <p>Status da conexão: {{ userChat.connectionStatus }}</p>
        <p>Mensagem recebida: {{ userChat.message }}</p>
        <input v-model="userChat.inputMessage" placeholder="Enviar mensagem..." />
        <button @click="userChat.sendMessage">Enviar</button>
    </div>
</template>
    
<script lang="ts">
    import { defineComponent, onMounted, onBeforeUnmount } from 'vue';
    import { useRoute } from 'vue-router';
    import {chat, type ChatHandler} from '@/http'
    export default defineComponent({
        setup() {
            const userChat: ChatHandler = chat();
            const route = useRoute()

            onMounted(() => {
                userChat.connect(route.params.userId);
            });

            onBeforeUnmount(() => {
                if (userChat.socket) {
                    userChat.socket.close();
                }
            });

            return { userChat };
        }
});
</script>
    