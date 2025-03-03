<script setup>
import ThemeToggle from "@/components/ThemeToggle.vue";
import MetricToggle from "@/apps/barbell/components/MetricToggle.vue";
</script>

<template>
  <header class="py-m leading-single">
    <div class="wrapper flex items-center justify-between">
      <h1 class="font-semibold">
        <span> 🏋 </span>
        <span class="ml-1.5"> Barbell Calculator </span>
      </h1>
      <nav>
        <ul class="flex items-center gap-x-2xs">
          <li class="py-2xs px-xs">
            <MetricToggle />
          </li>
          <li class="py-2xs px-xs">
            <ThemeToggle />
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>
