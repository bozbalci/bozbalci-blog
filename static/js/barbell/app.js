import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/barbell/layout/App.vue";

const app = createApp(App);
app.use(createPinia());

app.mount("#barbell");
