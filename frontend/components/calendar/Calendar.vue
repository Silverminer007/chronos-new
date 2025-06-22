<script lang="ts" setup>
import type {Event} from '~/types/event'

import CalendarListLayoutSkeleton from "~/components/calendar/list-layout/CalendarListLayoutSkeleton.vue";
import CalendarListLayout from "~/components/calendar/list-layout/CalendarListLayout.vue";

const {events, loading, layout} = defineProps<{ events: Event[], loading: boolean, layout: 'list' | 'invisible' }>()

</script>

<template>
  <div v-if="layout == 'list'">
    <div v-if="loading">
      <CalendarListLayoutSkeleton/>
    </div>
    <div v-if="!loading">
      <CalendarListLayout :events="events"/>
    </div>
  </div>
</template>

<style scoped>

</style>