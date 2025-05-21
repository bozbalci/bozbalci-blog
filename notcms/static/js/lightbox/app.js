import lightGallery from "lightgallery";

import { LIGHTGALLERY_LICENSE_KEY } from "@/lightbox/constants.js";
import mount from "@/lib/mount.js";

function registerLightbox(element) {
  const options = {
    speed: 500,
    enableDrag: false,
    counter: false,
    licenseKey: LIGHTGALLERY_LICENSE_KEY,
  };

  lightGallery(element, options);
}

mount("#lightbox", registerLightbox);
