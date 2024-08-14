export interface ChatHandler {
    connectionStatus: string;
    socket: WebSocket | null;
    message: string;
    inputMessage: string;
    connect: (userId: string | string[]) => void;
    sendMessage: () => void;
  }