const RED = "#82363a";
const BLUE = "#064872";
const YELLOW = "#bda74c";
const GREEN = "#40644a";
const WHITE = "#adacab";

export const unitSettings = [
  { value: "metric", label: "Metric", weightUnit: "kg" },
  { value: "imperial", label: "Imperial", weightUnit: "lbs" },
];

export const availableBars = [
  // Metric bars
  { unit: "metric", weight: 20 },
  { unit: "metric", weight: 15 },
  { unit: "metric", weight: 10 },
  // Imperial bars
  { unit: "imperial", weight: 45 },
  { unit: "imperial", weight: 35 },
  { unit: "imperial", weight: 15 },
];

export const availablePlates = [
  // Metric plates
  { unit: "metric", weight: 25, color: RED, big: true },
  { unit: "metric", weight: 20, color: BLUE, big: true },
  { unit: "metric", weight: 15, color: YELLOW, big: true },
  { unit: "metric", weight: 10, color: GREEN, big: true },
  // Metric change plates
  { unit: "metric", weight: 5.0, color: WHITE, big: false },
  { unit: "metric", weight: 2.5, color: RED, big: false },
  { unit: "metric", weight: 2.0, color: BLUE, big: false },
  { unit: "metric", weight: 1.5, color: YELLOW, big: false },
  { unit: "metric", weight: 1.0, color: GREEN, big: false },
  { unit: "metric", weight: 0.5, color: WHITE, big: false },
  // Imperial plates
  { unit: "imperial", weight: 55, color: RED, big: true },
  { unit: "imperial", weight: 45, color: BLUE, big: true },
  { unit: "imperial", weight: 35, color: YELLOW, big: true },
  { unit: "imperial", weight: 25, color: GREEN, big: true },
  // Imperial change plates
  { unit: "imperial", weight: 10, color: WHITE, big: false },
  { unit: "imperial", weight: 5, color: RED, big: false },
  { unit: "imperial", weight: 2.5, color: GREEN, big: false },
  { unit: "imperial", weight: 1.25, color: WHITE, big: false },
];
