<template>
  <Listbox v-model="selectedLocale" as="div">
    <ListboxButton class="align-text-top" aria-label="Language selector">
      <div
        class="relative cursor-pointer text-gray-10 dark:text-gray-dark-10 hover:text-accent-10 dark:hover:text-accent-dark-10"
      >
        <GlobeIcon />
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
        class="absolute z-50 top-full right-12 bg-gray-3 dark:bg-gray-dark-3 rounded-lg shadow-lg overflow-hidden py-2 ring-1 ring-gray-6 dark:ring-0 dark:highlight-white/5 text-step--1"
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
            <span class="inline-block text-[1.5rem] leading-none mr-2">
              {{ setting.icon }}
            </span>
            <span :lang="setting.value">
              {{ setting.label }}
            </span>
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
import { ref, watch } from "vue";
import GlobeIcon from "@/language-selector/components/GlobeIcon.vue";

const settings = [
  { value: "en", label: "English", icon: "🇬🇧" },
  { value: "tr", label: "Türkçe", icon: "🇹🇷" },
];

const defaultLocaleInfo = {
  activeLocale: "en",
  locales: {
    en: "/",
    tr: "/tr/",
  },
};

const localeInfoElement = document.getElementById("locale-info");
const localeInfo = localeInfoElement
  ? JSON.parse(localeInfoElement.textContent)
  : defaultLocaleInfo;
const activeLocale = localeInfo?.activeLocale;
const localeUrls = localeInfo?.locales;

const initialLocale =
  settings.find((setting) => setting.value === activeLocale) || settings[0];
const selectedLocale = ref(initialLocale);

watch(selectedLocale, (newLocale) => {
  const url = localeUrls[newLocale.value];
  if (url && newLocale !== activeLocale) {
    window.location.href = url;
  }
});
</script>
