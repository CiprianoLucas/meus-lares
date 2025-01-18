import { defineStore } from 'pinia';
import type { Role } from "./interfaces"

interface UserState {
  email: string;
  nick: string;
  role: Role;
  roles: Role[];
}

export const userStore = defineStore('user', {
  state: (): UserState => ({
    email: "",
    nick: "",
    role: "",
    roles: []
  }),
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'user',
        storage: localStorage,
      },
    ],
  } as any,
});
