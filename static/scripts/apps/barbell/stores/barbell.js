import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";

export const useBarbellStore = defineStore("barbell", () => {
  const unitSettings = [
    { value: "metric", label: "Metric", weightUnit: "kg" },
    { value: "imperial", label: "Imperial", weightUnit: "lbs" },
  ];

  const availableBars = [
    { unit: "metric", weight: 20 },
    { unit: "metric", weight: 15 },
    { unit: "metric", weight: 10 },
    { unit: "imperial", weight: 45 },
    { unit: "imperial", weight: 35 },
    { unit: "imperial", weight: 15 },
  ];

  const red = "#82363a";
  const blue = "#064872";
  const yellow = "#bda74c";
  const green = "#40644a";
  const white = "#adacab";
  const availablePlates = [
    // Metric plates
    { unit: "metric", weight: 25, color: red, big: true },
    { unit: "metric", weight: 20, color: blue, big: true },
    { unit: "metric", weight: 15, color: yellow, big: true },
    { unit: "metric", weight: 10, color: green, big: true },
    // Metric change plates
    { unit: "metric", weight: 5.0, color: white, big: false },
    { unit: "metric", weight: 2.5, color: red, big: false },
    { unit: "metric", weight: 2.0, color: blue, big: false },
    { unit: "metric", weight: 1.5, color: yellow, big: false },
    { unit: "metric", weight: 1.0, color: green, big: false },
    { unit: "metric", weight: 0.5, color: white, big: false },

    // Imperial plates
    { unit: "imperial", weight: 55, color: red, big: true },
    { unit: "imperial", weight: 45, color: blue, big: true },
    { unit: "imperial", weight: 35, color: yellow, big: true },
    { unit: "imperial", weight: 25, color: green, big: true },
    // Imperial change plates
    { unit: "imperial", weight: 10, color: white, big: false },
    { unit: "imperial", weight: 5, color: red, big: false },
    { unit: "imperial", weight: 2.5, color: green, big: false },
    { unit: "imperial", weight: 1.25, color: white, big: false },
  ];

  const filteredBars = computed(() =>
    availableBars.filter((bar) => bar.unit === selectedUnitSetting.value.value),
  );

  const filteredPlates = computed(() =>
    availablePlates.filter(
      (plate) => plate.unit === selectedUnitSetting.value.value,
    ),
  );

  // Reactive state
  const selectedUnitSetting = ref(unitSettings[0]);
  const selectedBar = ref(availableBars[0]);
  const platesOnBar = ref([]);

  watch(selectedUnitSetting, (newUnit) => {
    // Select the first available bar in the chosen unit

    selectedBar.value = filteredBars.value[0] || null;

    resetBar();
  });

  // Computed: Total weight including bar
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
    const barWeight = selectedBar.value.weight; // Get the current bar weight
    let remainingWeight = (targetWeight - barWeight) / 2; // Plates go on each side

    if (remainingWeight < 0) return [];

    const result = [];

    // Get plates for the currently selected unit
    const availableUnitPlates = availablePlates.filter(
      (plate) => plate.unit === selectedUnitSetting.value.value,
    );

    // Sort plates from largest to smallest for optimal distribution
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
    unitSettings,
    selectedUnitSetting,
    selectedBar,
    platesOnBar,
    totalWeight,
    availablePlates,
    selectBar,
    addPlate,
    removePlate,
    resetBar,
    calculatePlateCombination,
    availableBars,
    filteredBars,
    weightUnit,
    filteredPlates,
  };
});
