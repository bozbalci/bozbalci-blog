import lightGallery from "lightgallery";

function registerLightbox(element) {
  const options = {
    speed: 500,
    enableDrag: false,
    counter: true,
    licenseKey: "09C98B16-6CB8-429D-9D8A-54EF3FEBB5CE",
    subHtmlSelectorRelative: true,
    selector: ".photo-thumbnail",
  };

  lightGallery(element, options);
}

window.onload = () => {
  const element = document.getElementById("gallery");
  if (element) {
    registerLightbox(element);
  }
};