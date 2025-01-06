import { defineStore } from 'pinia';
import type { Role } from "./interfaces"

interface UserState {
  username: string;
  role: Role;
  roles: Role[];
}

export const userStore = defineStore('user', {
  state: (): UserState => ({
    username: "",
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
