<script lang="ts" setup>
import type {Event} from "~/types/event";
import {moveDateByDiff} from "~/utils/datetime";

const {event} = defineProps<{ event: Event }>();
const emit = defineEmits(['update:event'])

const computedStartDate = computed({
  get: () => new Date(event.start),
  set: (value) => {
    console.log(value.toISOString())
    const newStartDateTime = value.toISOString().split('T')[0] + 'T' + event.start.split('T')[1];
    event.end = moveDateByDiff(event.end, newStartDateTime, event.start);
    event.start = newStartDateTime;
  }
})
const computedStartTime = computed({
  get: () => new Date(event.start),
  set: (value) => {
    const newStartDateTime = event.start.split('T')[0] + 'T' + value.toISOString().split('T')[1];
    event.end = moveDateByDiff(event.end, newStartDateTime, event.start);
    event.start = newStartDateTime;
  }
})

const computedEndDate = computed({
  get: () => new Date(event.end),
  set: (value) => {
    event.end = value.toISOString().split('T')[0] + 'T' + event.end.split('T')[1];
  }
})
const computedEndTime = computed({
  get: () => new Date(event.end),
  set: (value) => {
    event.end = event.end.split('T')[0] + 'T' + value.toISOString().split('T')[1];
  }
})

</script>

<template>
  <Inplace>
    <template #display>
      <p class="text-2xl text-bold">{{ event.title }}</p>
      <div v-if="sameDay(event.start, event.end)">
        <p>{{ dateOf(event.start) }}</p>
        <p>
          {{ timeOfDay(event.start) }} Uhr -
          {{ timeOfDay(event.end) }} Uhr
        </p>
      </div>
      <div v-else>
        <p v-if="event.start">Start: {{ formatDate(event.start, 'dd LLL yyyy HH:mm') }}
          Uhr</p>
        <p v-if="event.end">Ende: {{ formatDate(event.end, 'dd LLL yyyy HH:mm') }}
          Uhr</p>
      </div>
      <p v-if="event.venue">Ort: {{ event.venue }}</p>
      <p v-if="event.notes">Notizen: {{ event.notes }}</p>
    </template>
    <template #content="{closeCallback}" class="max-w-screen">
      <div class="flex flex-col gap-2 w-full">
        <div class="inline-flex items-center gap-2">
          <IftaLabel class="flex-grow">
            <InputText id="title" v-model="event.title" autofocus class="w-full"/>
            <label for="title">Beschreibung</label>
          </IftaLabel>
          <Button class="size-xl!" severity="success" text @click="closeCallback;emit('update:event')">
            <Icon name="solar:check-circle-bold"/>
          </Button>
        </div>
        <div class="inline-flex items-center gap-2">
          <IftaLabel>
            <DatePicker v-model="computedStartDate" fluid iconDisplay="input" showIcon/>
            <label for="startDate">Start</label>
          </IftaLabel>
          <IftaLabel>
            <DatePicker v-model="computedStartTime" fluid iconDisplay="input" showIcon timeOnly/>
            <label for="startDate">Uhrzeit</label>
          </IftaLabel>
        </div>
        <div class="inline-flex items-center gap-2">
          <IftaLabel>
            <DatePicker v-model="computedEndDate" fluid iconDisplay="input" showIcon/>
            <label for="startDate">Ende</label>
          </IftaLabel>
          <IftaLabel>
            <DatePicker v-model="computedEndTime" fluid iconDisplay="input" showIcon timeOnly/>
            <label for="startDate">Uhrzeit</label>
          </IftaLabel>
        </div>
        <div class="inline-flex items-center gap-2">
          <IftaLabel class="flex-grow">
            <InputText id="venue" v-model="event.venue" autofocus class="w-full"/>
            <label for="venue">Ort</label>
          </IftaLabel>
        </div>
        <div class="inline-flex items-center gap-2">
          <IftaLabel class="flex-grow">
            <Textarea id="notes" v-model="event.notes" auto-resize autofocus class="w-full"/>
            <label for="notes">Notizen</label>
          </IftaLabel>
        </div>
      </div>
    </template>
  </Inplace>
</template>

<style scoped>

</style>