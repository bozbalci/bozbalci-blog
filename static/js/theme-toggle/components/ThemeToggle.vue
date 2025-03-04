<template>
  <Listbox v-model="selectedTheme" as="div">
    <ListboxButton class="align-text-top">
      <div
        class="relative cursor-pointer text-gray-10 dark:text-gray-dark-10 hover:text-accent-10 dark:hover:text-accent-dark-10"
      >
        <span class="dark:hidden">
          <SunIcon />
        </span>
        <span class="hidden dark:inline">
          <MoonIcon />
        </span>
      </div>
    </ListboxButton>
    <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-out"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <ListboxOptions
        class="absolute z-50 top-full right-0 bg-gray-3 dark:bg-gray-dark-3 rounded-lg shadow-lg overflow-hidden py-2 ring-1 ring-gray-6 dark:ring-0 dark:highlight-white/5 text-step--1"
      >
        <ListboxOption
          v-for="setting in settings"
          :key="setting.value"
          :value="setting"
          v-slot="{ active, selected }"
        >
          <div
            class="flex items-center cursor-pointer py-2 pl-2 pr-6"
            :class="{
              'bg-gray-5 dark:bg-gray-dark-5': active,
              'text-accent-10 dark:text-accent-dark-10': selected,
            }"
          >
            <component
              :is="setting.icon"
              class="w-6 h-6 mr-2"
              :class="{
                'text-gray-10 dark:text-gray-dark-10': !selected,
                'text-accent-10 dark:text-accent-dark-10': selected,
              }"
            />
            {{ setting.label }}
          </div>
        </ListboxOption>
      </ListboxOptions>
    </transition>
  </Listbox>
</template>

<script setup>
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from "@headlessui/vue";
import SunIcon from "@/theme-toggle/components/SunIcon.vue";
import MoonIcon from "@/theme-toggle/components/MoonIcon.vue";
import PcIcon from "@/theme-toggle/components/PcIcon.vue";
import { ref, watch } from "vue";

const settings = [
  { value: "light", label: "Light", icon: SunIcon },
  { value: "dark", label: "Dark", icon: MoonIcon },
  { value: "system", label: "System", icon: PcIcon },
];

const storedTheme = localStorage.getItem("theme") || "system";

const initialTheme =
  settings.find((setting) => setting.value === storedTheme) || settings[2];

const selectedTheme = ref(initialTheme);

watch(selectedTheme, (newTheme) => {
  const themeValue = newTheme.value;

  localStorage.setItem("theme", themeValue);

  const element = document.documentElement;
  element.classList.toggle("dark", themeValue === "dark");
  element.classList.toggle("light", themeValue === "light");

  const isDark =
    themeValue === "dark" ||
    (themeValue === "system" &&
      matchMedia("(prefers-color-scheme: dark)").matches);
  document
    .querySelector('meta[name="theme-color"]')
    .setAttribute("content", isDark ? "#111210" : "#fcfdfc");
});
</script>
