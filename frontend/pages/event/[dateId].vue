<script lang="ts" setup>

import {useSingleEvent} from "~/composables/useEvents";
import EventCardSkeleton from "~/components/calendar/list-layout/EventCardSkeleton.vue";

const route = useRoute();
const {dateId} = route.params;

const {event, loading, error} = useSingleEvent(dateId);
</script>

<template>
  <EventCardSkeleton v-if="loading"/>
  <div v-if="event">
    <InputText v-model="event.title" :default-value="event.title"/>
    <DatePicker :default-value="new Date(event.start)"/>
  </div>
</template>

<style scoped>

</style>