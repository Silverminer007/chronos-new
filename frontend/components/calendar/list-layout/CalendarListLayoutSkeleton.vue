<script lang="ts" setup>
import EventCardSkeleton from "~/components/calendar/list-layout/EventCardSkeleton.vue";
</script>

<template>
  <div v-for="num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" :key="num">
    <Chip v-if="num % 2 == 1" class="p-2 m-2">
      <Skeleton height="1.5rem" width="5rem"/>
    </Chip>
    <EventCardSkeleton/>
  </div>
</template>

<style scoped>

</style>