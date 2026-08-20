<template>
  <div class="min-h-screen text-slate-900 lg:flex">
    <Sidebar />
    <div class="min-w-0 flex-1 lg:pl-[276px]">
      <Header />
      <main
        class="mx-auto w-full max-w-[1580px] px-4 pb-24 pt-6 sm:px-6 lg:px-8 xl:px-10 lg:pb-12 lg:pt-8"
      >
        <router-view v-slot="{ Component, route }">
          <transition name="page" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>
<script setup>
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'
</script>
<style scoped>
.page-enter-active,
.page-leave-active {
  transition:
    opacity 0.18s ease,
    transform 0.18s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-3px);
}
</style>
