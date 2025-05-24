<script setup>
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from '@headlessui/vue';
import { useBarbellStore } from '@/barbell/stores/barbell.js';
import { storeToRefs } from 'pinia';
import { unitSettings } from '@/barbell/constants.js';

const store = useBarbellStore();

const { selectedUnitSetting } = storeToRefs(store);
</script>

<template>
  <Listbox v-model="selectedUnitSetting" as="div">
    <ListboxButton>
      <div class="relative cursor-pointer flex items-center group">
        <span>
          {{ selectedUnitSetting.label }}
        </span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          class="size-6 ml-0.75 mt-0.75 text-gray-10 dark:text-gray-dark-10 group-hover:text-accent-10 dark:group-hover:text-accent-dark-10"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m19.5 8.25-7.5 7.5-7.5-7.5"
          />
        </svg>
      </div>
    </ListboxButton>
    <ListboxOptions
      class="absolute z-50 top-full bg-gray-3 dark:bg-gray-dark-3 rounded-lg shadow-lg overflow-hidden py-2 ring-1 ring-gray-6 dark:ring-0 dark:highlight-white/5 text-step--1"
    >
      <ListboxOption
        v-for="setting in unitSettings"
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
          {{ setting.label }} ({{ setting.weightUnit }})
        </div>
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>
