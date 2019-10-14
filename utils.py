#######################################################################
# Copyright (c) 2019 Alejandro Pereira

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

#######################################################################
#!/usr/bin/python
import cv2
import random

RGB_GREEN = (0, 255, 0)
RGBA_GREEN = (0, 255, 0, 0)
RGB_BLACK = (0, 0, 0)
RGBA_BLACK = (0, 0, 0, 0)

def get_random_item(collection):
    """Returns a random item from a collection (list or dictionary)"""
    if isinstance(collection, list):
        index = random.randrange(len(collection))
        return collection[index]
    elif isinstance(collection, dict):
        index = random.randrange(len(collection.keys()))
        return list(collection.keys())[index]
    else:
        return None


def rescale_image(image, scale_factor):
    """Scales image by a scale factor i.e: 1.5"""
    interpol = cv2.INTER_CUBIC if scale_factor > 1 else cv2.INTER_AREA
    result = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=interpol)
    return result


def random_rescale(image, scales):
    """Rescale an image by a random scale picked from provided list of sizes"""
    scale_factor = get_random_item(scales)
    return rescale_image(image, scale_factor)


def resize_image(image, size):
    """Resize image to a specific size [width, height]"""
    if size[0] < image.shape[1] or size[1] < image.shape[0]:
        interpol = cv2.INTER_AREA
    else:
        interpol = cv2.INTER_CUBIC
    result = cv2.resize(image, (size[0], size[1]), interpolation=interpol)
    return result


def pad_image(image, size):
    """Resize image to a specific size [width, height] using padding"""
    assert size[0] > image.shape[1] and size[1] > image.shape[0]
    delta_w = size[0] - image.shape[1]
    delta_h = size[1] - image.shape[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)
    color = RGB_BLACK
    result = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return result


def rescale_image_relative(image, base_scale, base_width):
    """Re-scales image on a scale factor relative to other image"""
    target_width = base_scale * base_width
    image_width = image.shape[1]
    target_factor = target_width / image_width
    interpol = cv2.INTER_CUBIC if target_factor > 1 else cv2.INTER_AREA
    result = cv2.resize(image, None, fx=target_factor, fy=target_factor, interpolation=interpol)
    return result


def random_rescale_relative(image, scale_range, decimals, base_image):
    """Re-scales image on a random picked scale factor relative to other image"""
    base_scale = round(random.uniform(scale_range[0], scale_range[1]), decimals)
    base_width = base_image.shape[1]
    return rescale_image_relative(image, base_scale, base_width)


def add_image(new_image, position, bg_image):
    """Adds an image on top of another"""
     #TODO: Make sure images have alpha channel
    # Add images by alpha channel
    result = bg_image
    x1, y1, x2, y2 = position
    alpha_image = new_image[:, :, 3] / 255.0
    alpha_bg = 1.0 - alpha_image
    for channel in range(0, 3):
        result[y1:y2, x1:x2, channel] = (alpha_image * new_image[:, :, channel] + alpha_bg * result[y1:y2, x1:x2, channel])

    return result


def draw_bounding_box(image, x1, y1, x2, y2):
    """Draws a single bounding box with the format (x1, y1, x2, y2)"""
    color = RGB_GREEN if image.shape[2] == 3 else RGBA_GREEN
    result = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    return result