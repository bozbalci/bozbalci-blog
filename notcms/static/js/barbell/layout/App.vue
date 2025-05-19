<script setup>
import Controls from "@/barbell/components/Controls.vue";
import Header from "@/barbell/layout/Header.vue";
import BarView from "@/barbell/components/BarView.vue";
</script>

<template>
  <Header />
  <div class="wrapper flex flex-col gap-y-xs">
    <BarView />
    <Controls />
  </div>
</template>
