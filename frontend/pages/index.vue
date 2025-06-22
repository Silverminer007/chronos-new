<script lang="ts" setup>
/*definePageMeta({
  requiresAuth: true,
})*/
import Calendar from "~/components/calendar/Calendar.vue";
import {onMounted, ref} from 'vue'

const {events, loading, error} = useEvents();

const drawerVisible = ref(false)

const toggleDrawer = () => {
  drawerVisible.value = !drawerVisible.value
}

// Auf großen Screens Drawer offen lassen
onMounted(() => {
  if (window.innerWidth >= 1024) {
    drawerVisible.value = true
  }
})

</script>

<template>
  <p v-if="error">{{ error }}</p>
  <Toolbar class="sticky top-0 z-20 shadow">
    <template #start>
      <Button class="mr-3 lg:hidden" @click="toggleDrawer">
        <Icon class="w-8 h-8" name="solar:hamburger-menu-linear"/>
      </Button>
      <span class="text-xl font-semibold">Hey, Justus</span>
    </template>

    <template #end>
      <Button class="border-none px-4 py-2">
        <Icon name="pajamas:plus"/>
        New
      </Button>
    </template>
  </Toolbar>

  <Drawer
      v-model:visible="drawerVisible"
      :dismissable="true"
      :modal="false"
      :showCloseIcon="true"
      class="w-64 border-r border-gray-200 shadow hidden lg:block"
  >
  </Drawer>
  <div v-if="events">
    <Calendar :events="events" :loading="loading" layout="list"/>
  </div>
</template>

<style scoped>

</style>