import lightGallery from "lightgallery";

import { LIGHTGALLERY_LICENSE_KEY } from "@/lightbox/constants.js";

function registerLightbox(element) {
  const options = {
    speed: 500,
    enableDrag: false,
    counter: true,
    licenseKey: LIGHTGALLERY_LICENSE_KEY,
    subHtmlSelectorRelative: true,
    selector: ".photo-thumbnail",
  };

  lightGallery(element, options);
}

window.onload = () => {
  const element = document.getElementById("lightbox-gallery");
  if (element) {
    registerLightbox(element);
  }
};
