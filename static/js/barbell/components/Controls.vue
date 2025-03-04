<script setup>
import { useBarbellStore } from "@/barbell/stores/barbell.js";
import { storeToRefs } from "pinia";
import { ref } from "vue";
import Plate from "@/barbell/components/Plate.vue";
import Button from "@/barbell/components/Button.vue";

const store = useBarbellStore();

const {
  addPlate,
  removePlate,
  resetBar,
  selectBar,
  calculatePlateCombination,
} = store;
const { totalWeight, filteredBars, filteredPlates, weightUnit, selectedBar } =
  storeToRefs(store);

const targetWeight = ref("");

function applyCalculatedPlates() {
  const weight = parseFloat(targetWeight.value);
  if (isNaN(weight) || weight <= selectedBar.value.weight) {
    return;
  }

  const plateCombination = calculatePlateCombination(weight);
  if (plateCombination.length) {
    resetBar();
    plateCombination.forEach(addPlate);
  }
}
</script>

<template>
  <div class="flex flex-col gap-y-xs-s">
    <div class="font-mono font-bold text-step-4 leading-none pt-xs pb-s">
      {{ totalWeight }} {{ weightUnit }}
    </div>
    <div class="flex items-center gap-xs">
      <Button @click="removePlate">Pop</Button>
      <Button @click="resetBar">Reset</Button>
    </div>
    <div class="flex items-center gap-xs">
      <input
        v-model="targetWeight"
        type="number"
        class="border rounded font-mono px-2 py-1"
        :placeholder="`target weight (${weightUnit})`"
      />
      <Button @click="applyCalculatedPlates"> Load </Button>
    </div>
  </div>

  <div class="flex flex-col space-y-s">
    <h2 class="text-step-2 font-semibold">Bars</h2>
    <div class="flex items-center gap-x-s">
      <button
        :key="bar.weight"
        v-for="bar in filteredBars"
        @click="selectBar(bar)"
        class="rounded py-1 px-8 transition-colors font-mono font-semibold"
        :class="{
          'bg-gray-10 dark:bg-gray-dark-10 text-white':
            selectedBar.weight === bar.weight,
          'bg-gray-5 dark:bg-gray-dark-5 cursor-pointer':
            selectedBar.weight !== bar.weight,
        }"
      >
        {{ bar.weight }} {{ weightUnit }}
      </button>
    </div>
  </div>

  <div class="flex flex-col space-y-s">
    <h2 class="text-step-2 font-semibold">Plates</h2>
    <div
      class="ml-2 grid place-items-center gap-2xs-xs"
      :class="{
        'grid-cols-5': weightUnit === 'kg',
        'grid-cols-4': weightUnit === 'lbs',
      }"
    >
      <Plate
        v-for="plate in filteredPlates"
        :key="plate.weight"
        :plate="plate"
        :weightUnit="weightUnit"
        @add="addPlate"
      />
    </div>
  </div>
</template>
