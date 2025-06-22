<script lang="ts" setup>
import type {Event} from "~/types/event";
import EventCard from "~/components/calendar/list-layout/EventCard.vue";
import {dateOf} from "~/utils/datetime";
import EventDetails from "~/components/calendar/EventDetails.vue";

const {events} = defineProps<{ events: Event[] }>()

const dateEventMap = computed(() => {
  const dateEventMap = new Map<string, Event[]>();
  if (!events) return dateEventMap;
  events.forEach(event => {
    const dateAsDate = event.start.split('T')[0];
    if (!dateEventMap.has(dateAsDate)) {
      dateEventMap.set(dateAsDate, []);
    }
    dateEventMap.get(dateAsDate)?.push(event);
  });
  return dateEventMap;
})

const op = ref();
const selectedEvent = ref()
const showEvent = (e: MouseEvent, event: Event) => {
  op.value.hide();

  if (selectedEvent.value?.id === event.id) {
    selectedEvent.value = null;
    return;
  }
  selectedEvent.value = event;
  nextTick(() => {
    op.value.show(e);
  })
}
</script>

<template>
  <ScrollTop/>
  <div v-for="[date, events] in dateEventMap.entries()" :key="date">
    <Chip class="m-2 p-2">{{ dateOf(date) }}</Chip>
    <div v-for="event in events" :key="event.id" @click="showEvent($event, event)">
      <EventCard :event="event" class="m-2"/>
    </div>
  </div>
  <Popover ref="op">
    <div v-if="selectedEvent">
      <EventDetails :event="selectedEvent"/>
    </div>
  </Popover>
</template>

<style scoped>

</style>