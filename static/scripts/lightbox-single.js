import lightGallery from "lightgallery";

import {LIGHTGALLERY_LICENSE_KEY} from "./constants.js";

function registerLightbox(element) {
  const options = {
    speed: 500,
    enableDrag: false,
    counter: false,
    licenseKey: LIGHTGALLERY_LICENSE_KEY,
  };

  lightGallery(element, options);
}

window.onload = function () {
  const element = document.getElementById("lg-single");
  if (element) {
    registerLightbox(element);
  }
}