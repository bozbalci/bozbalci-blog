<script setup>
import { useBarbellStore } from '@/barbell/stores/barbell.js';
import { storeToRefs } from 'pinia';

const store = useBarbellStore();
const { platesOnBar, selectedBar } = storeToRefs(store);
</script>

<template>
  <div
    class="flex items-center gap-[1px] select-none min-h-[160px] text-step--1"
  >
    <div
      v-for="plate in platesOnBar.slice().reverse()"
      :key="'left-' + plate.weight"
      class="font-mono font-bold text-white flex justify-center items-center w-[26px] flex-shrink-0"
      :class="{ 'h-[160px]': plate.big, 'h-[90px]': !plate.big }"
      :style="{ backgroundColor: plate.color }"
    >
      <div :class="{ '-rotate-90': !plate.big }">{{ plate.weight }}</div>
    </div>

    <div
      class="h-4 flex items-center justify-center bg-gray-6 dark:bg-gray-dark-6 flex-grow-1 min-w-[120px] font-mono font-bold text-center"
    >
      {{ selectedBar.weight }}
    </div>

    <div
      v-for="plate in platesOnBar"
      :key="'left-' + plate.weight"
      class="font-mono font-bold text-white flex justify-center items-center w-[26px] flex-shrink-0"
      :class="{ 'h-[160px]': plate.big, 'h-[90px]': !plate.big }"
      :style="{ backgroundColor: plate.color }"
    >
      <div :class="{ '-rotate-90': !plate.big }">{{ plate.weight }}</div>
    </div>
  </div>
</template>
