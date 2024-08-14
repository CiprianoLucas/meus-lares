import {type ChatHandler} from './interfaces';

export function chat(): ChatHandler {
  const handler: ChatHandler = {
    connectionStatus: 'Desconectado',
    socket: null,
    message: '',
    inputMessage: '',

    connect(userId: string | string[]) {
      const url = `${import.meta.env.VITE_API_URL}/ws/chat/${userId}`
      handler.socket = new WebSocket(url);

      handler.socket.onopen = () => {
        handler.connectionStatus = 'Conectado';
      };

      handler.socket.onmessage = (event) => {
        handler.message = event.data;
      };

      handler.socket.onclose = () => {
        handler.connectionStatus = 'Desconectado';
      };

      handler.socket.onerror = (error) => {
        console.error('WebSocket Error: ', error);
      };
    },

    sendMessage() {
      if (handler.socket && handler.socket.readyState === WebSocket.OPEN) {
        handler.socket.send(handler.inputMessage);
        handler.inputMessage = '';
      }
    }
  };

  return handler;
}