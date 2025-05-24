import lightGallery from 'lightgallery';

import { LIGHTGALLERY_LICENSE_KEY } from '@/lightbox/constants.js';
import mount from '@/lib/mount.js';

function registerLightbox(element) {
  const options = {
    speed: 500,
    enableDrag: false,
    counter: true,
    licenseKey: LIGHTGALLERY_LICENSE_KEY,
    subHtmlSelectorRelative: true,
    selector: '.photo-thumbnail',
  };

  lightGallery(element, options);
}

mount('#lightbox-gallery', registerLightbox);
