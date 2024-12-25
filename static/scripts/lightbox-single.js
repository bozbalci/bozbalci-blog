import lightGallery from "lightgallery";

function registerLightbox(element) {
  const options = {
    speed: 500,
    enableDrag: false,
    counter: false,
    licenseKey: "09C98B16-6CB8-429D-9D8A-54EF3FEBB5CE",
  };

  lightGallery(element, options);
}

window.onload = function() {
  const element = document.getElementById("lg-single");
  if (element) {
    registerLightbox(element);
  }
}