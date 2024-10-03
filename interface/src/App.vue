<template>
	<nav-bar/>
	<RouterView />
</template>
  
<script setup lang="ts">
	import NavBar from '@/components/template/NavBar.vue'
	import { RouterView } from 'vue-router'
</script>
// DON'T CHANGE THIS FILE