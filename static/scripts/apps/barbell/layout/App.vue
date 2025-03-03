<script setup>
import Controls from "@/apps/barbell/components/Controls.vue";
import Header from "@/apps/barbell/layout/Header.vue";
import BarView from "@/apps/barbell/components/BarView.vue";
</script>

<template>
  <Header />
  <div class="wrapper flex flex-col gap-y-xs">
    <BarView />
    <Controls />
  </div>
</template>
