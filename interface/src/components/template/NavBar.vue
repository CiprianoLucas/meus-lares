<template>
    <div class="pos-f-t">
      <div class="collapse" id="navbarToggleExternalContent">
        <div class="bg-dark p-4">
          <h4 class="text-white">Collapsed content</h4>
          <span class="text-muted">Toggleable via the navbar brand.</span>
        </div>
      </div>
      <nav class="navbar navbar-dark bg-dark">
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarToggleExternalContent"
          aria-controls="navbarToggleExternalContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
      </nav>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { api } from '@/http';
  
  const username = ref<string | null>(null);
  const isResident = ref(false);
  const isUnion = ref(false);
  
  async function logout() {
    await api.logout();
    window.location.reload();
  }
  
  onMounted(() => {
    username.value = localStorage.getItem('username');
    isResident.value = !!localStorage.getItem('isResident');
    isUnion.value = !!localStorage.getItem('isUnion');
  });
  </script>
  
  <style>
  </style>
  