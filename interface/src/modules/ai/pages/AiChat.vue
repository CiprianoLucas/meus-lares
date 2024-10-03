<template>
    <div class="chat-container">
        <div class="chat-box">
            <div v-for="(message, index) in messages" :key="index" class="chat-message" :class="message.role">
                <p v-html="message.content"></p>
            </div>
        </div>
    
        <div class="input-box">
            <input
            v-model="userMessage"
            type="text"
            placeholder="..."
            @keydown.enter="sendMessage"
            />
            <button @click="sendMessage">Enviar</button>
        </div>
    </div>
</template>
  
<script lang="ts" setup>
    import { ref } from 'vue';
    import { api } from '@/http'; // Supondo que você tenha uma instância axios configurada

    const userMessage = ref('');
    const messages = ref([
        { role: 'assistant', content: 'Olá! Como posso te ajudar?' }
    ]);

    const formatMessage = (message: string) => {
        return message.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    };

    const sendMessage = async () => {
    if (userMessage.value.trim() === '') return;

    messages.value.push({ role: 'user', content: userMessage.value });

    try {
        const response = await api.post('/ai/chat/', {
            message: userMessage.value
        });

        messages.value.push({ role: 'assistant', content: formatMessage(response.data.response) });

    } catch (error) {
        messages.value.push({ role: 'system', content: 'Error: Unable to process the request.' });
    }

    userMessage.value = '';
    };
</script>
<style scoped>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 80vh;
        justify-content: space-between;
        padding: 20px;
    }

    .chat-box {
        flex-grow: 1;
        overflow-y: auto;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        background-color: #f9f9f9;
        margin-bottom: 10px;
    }

    .chat-message {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 60%;
        word-wrap: break-word;
    }

    .chat-message.user {
        background-color: #d1e7ff;
        align-self: flex-end;
    }

    .chat-message.assistant {
        background-color: #e2ffe4;
        align-self: flex-start;
    }

    .chat-message.system {
        background-color: #fff8c4;
        text-align: center;
    }

    .input-box {
        display: flex;
        gap: 10px;
    }

    input {
        flex-grow: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    button {
        padding: 10px 15px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }

    button:hover {
        background-color: #0056b3;
    }

    .message {
        font-size: 16px;
        line-height: 1.5;
    }
</style>