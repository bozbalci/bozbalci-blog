<script setup>
const props = defineProps({ plate: Object, weightUnit: String });
const emit = defineEmits(['add']);
</script>

<template>
  <button
    class="leading-none cursor-pointer hover:opacity-80 rounded-full border border-gray-6 dark:border-gray-dark-6"
    :class="{
      'p-4 size-2xl-3xl': plate.big,
      'p-2 size-xl-2xl ': !plate.big,
    }"
    :style="{ backgroundColor: plate.color }"
    @click="emit('add', plate)"
  >
    <span
      class="font-mono font-bold text-white"
      :class="{ 'text-step-0': plate.big, 'text-step--1': !plate.big }"
    >
      {{ plate.weight }}
      <br />
      {{ weightUnit }}
    </span>
  </button>
</template>
