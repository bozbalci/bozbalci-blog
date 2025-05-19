<script setup>
const props = defineProps({
  type: {
    type: String,
    default: "button",
  },
  variant: {
    type: String,
    default: "primary",
  },
  size: {
    type: String,
    default: "md",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["click"]);

const baseClasses = "rounded font-mono font-medium cursor-pointer";
const variantClasses = {
  primary:
    "bg-gray-8 dark:bg-gray-dark-8 hover:bg-gray-7 dark:hover:bg-gray-dark-7",
};
const sizeClasses = {
  sm: "px-3 py-1 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-5 py-3 text-lg",
};
</script>

<template>
  <button
    :type="type"
    :class="[
      baseClasses,
      variantClasses[variant] || variantClasses.primary,
      sizeClasses[size] || sizeClasses.md,
      { 'opacity-50 cursor-not-allowed': disabled },
    ]"
    :disabled="disabled"
    @click="emit('click')"
  >
    <slot />
  </button>
</template>
