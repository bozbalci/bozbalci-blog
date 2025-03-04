import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";

import {
  availableBars,
  availablePlates,
  unitSettings,
} from "@/barbell/constants.js";

export const useBarbellStore = defineStore("barbell", () => {
  // Reactive state
  const selectedUnitSetting = ref(unitSettings[0]);
  const selectedBar = ref(availableBars[0]);
  const platesOnBar = ref([]);

  // Computed
  const filteredBars = computed(() =>
    availableBars.filter((bar) => bar.unit === selectedUnitSetting.value.value),
  );

  const filteredPlates = computed(() =>
    availablePlates.filter(
      (plate) => plate.unit === selectedUnitSetting.value.value,
    ),
  );

  const totalWeight = computed(() => {
    const plateWeight = platesOnBar.value.reduce(
      (sum, plate) => sum + plate.weight * 2,
      0,
    );
    return selectedBar.value.weight + plateWeight;
  });

  const weightUnit = computed(() => {
    return selectedUnitSetting.value.weightUnit;
  });

  // Watchers
  watch(selectedUnitSetting, (newUnit) => {
    // Select the first available bar in the chosen unit
    selectedBar.value = filteredBars.value[0] || null;
    resetBar();
  });

  // Actions
  function selectBar(bar) {
    selectedBar.value = bar;
  }

  function addPlate(plate) {
    platesOnBar.value.push(plate);
  }

  function removePlate() {
    platesOnBar.value.pop();
  }

  function resetBar() {
    platesOnBar.value = [];
  }

  function calculatePlateCombination(targetWeight) {
    const barWeight = selectedBar.value.weight;
    let remainingWeight = (targetWeight - barWeight) / 2;

    if (remainingWeight < 0) return [];

    const result = [];

    const availableUnitPlates = availablePlates.filter(
      (plate) => plate.unit === selectedUnitSetting.value.value,
    );

    availableUnitPlates.sort((a, b) => b.weight - a.weight);

    for (const plate of availableUnitPlates) {
      while (remainingWeight >= plate.weight) {
        result.push(plate);
        remainingWeight -= plate.weight;
      }
    }

    return remainingWeight === 0 ? result : [];
  }

  return {
    selectedUnitSetting,
    selectedBar,
    platesOnBar,
    filteredBars,
    filteredPlates,
    totalWeight,
    weightUnit,
    selectBar,
    addPlate,
    removePlate,
    resetBar,
    calculatePlateCombination,
  };
});
