import io
import os

import numpy as np
from PIL import Image as PIL_Image
import base64
import McUtils.Devutils as dev
import cv2

__all__ = [
    "WhitespaceSeparator",
    "load_image"
]

def prep_buffer(img_data: str):
    if img_data.startswith('image/'):
        img_data = img_data.split(";", 1)[1]
    b64_tag = 'base64,'
    if img_data.startswith(b64_tag):
        return io.BytesIO(base64.b64decode(img_data[len(b64_tag):]))
    else:
        return io.BytesIO(img_data.encode('ascii'))


def load_image(img_data) -> PIL_Image:
    if dev.is_filepath_like(img_data) and os.path.exists(img_data):
        image = PIL_Image.open(img_data)
    elif isinstance(img_data, str):
        # buf = Image.from
        image = PIL_Image.open(prep_buffer(img_data))
    else:
        image = img_data
    return image

class WhitespaceSeparator:

    def __init__(self, image_spec):
        self.image = load_image(image_spec)

    binarization_threshold = 200
    @classmethod
    def binarize(cls, image, threshold=None):
        if threshold is None:
            threshold = cls.binarization_threshold
        return image.convert("L").point(lambda x: 0 if x < threshold else 255, '1')

    dilation_kernel_size = 2
    dilation_iterations = 2
    @classmethod
    def dilate_image(cls, binary_image, kernel_size=None, iterations=None):
        image_cv = np.array(binary_image, dtype=np.uint8) * 255
        image_cv = cv2.bitwise_not(image_cv)
        if kernel_size is None:
            kernel_size = cls.dilation_kernel_size
        if iterations is None:
            iterations = cls.dilation_iterations

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(image_cv, kernel, iterations=iterations)

    connectivity_threshold = 8
    @classmethod
    def get_connected_components(cls, dilated_image, connectivity_threshold=None):
        if connectivity_threshold is None: connectivity_threshold = cls.connectivity_threshold
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated_image, connectivity=connectivity_threshold)
        return stats

    @classmethod
    def split(self, image, stats):
        return [
            image.crop((x, y, x + w, y + h))
            for x, y, w, h, area  in stats
        ]

    def build_mask(self,
                   binarization_threshold=None,
                   dilate=True,
                   dilation_kernel_size=None,
                   dilation_iterations=None
                   ):
        mask = self.binarize(self.image, threshold=binarization_threshold)
        if dilate:
            mask = self.dilate_image(mask,
                                     kernel_size=dilation_kernel_size,
                                     iterations=dilation_iterations
                                     )
        return mask

    def segment(self,
                *,
                connectivity_threshold=None,
                **mask_opts
                ):
        mask = self.build_mask(**mask_opts)
        stats = self.get_connected_components(mask, connectivity_threshold=connectivity_threshold)
        return self.split(self.image, stats)