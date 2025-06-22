<script lang="ts" setup>
import type {Event} from '~/types/event'

const {event} = defineProps<{ event: Event }>()

const startAsDate = new Date(event.start);
const endAsDate = new Date(event.end);

const zeroPad = (num: number) => String(num).padStart(2, '0')

</script>

<template>
  <Card class="overflow-hidden not-sm:max-w-screen sm:w-lg">
    <template #title>
      {{ event.title }}
    </template>
    <template #subtitle>
      {{ zeroPad(startAsDate.getHours()) }}:{{ zeroPad(startAsDate.getMinutes()) }} Uhr
      - {{ zeroPad(endAsDate.getHours()) }}:{{ zeroPad(endAsDate.getMinutes()) }} Uhr
    </template>
  </Card>
</template>

<style scoped>

</style>