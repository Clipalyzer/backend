import numpy as np


def max_rgb(r, g, b, offset):
    return (r + offset, g + offset, b + offset)


def min_rgb(r, g, b, offset):
    return (r - offset, g - offset, b - offset)


def min(raw, offset):
    return min_rgb(raw, raw, raw, offset)


def max(raw, offset):
    return max_rgb(raw, raw, raw, offset)


def outside_range(raw, img, offset, x, y):
    return (img[x, y] < min(raw, offset)).any() or (img[x, y] > max(raw, offset)).any()


def outside_range_bgr(r, g, b, img, offset, x, y):
    return (img[x, y] < min_rgb(r, g, b, offset)).any() or (img[x, y] > max_rgb(r, g, b, offset)).any()


def inside_range_bgr(r, g, b, px, offset):
    return (px > min_rgb(r, g, b, offset)).all() and (px < max_rgb(r, g, b, offset)).all()


def inside_range(c, px, offset):
    return (px > min(c, offset)).all() and (px < max(c, offset)).all()


def image_processor(img, offset=10, file_name=None):
    img = img[::2, ::2]
    # print(f"> {img}")
    try:
        # image = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)
        # image[:] = 0
        # print(f"[{file_name}] Processing image1 {img.shape[1]}x{img.shape[0]}")
        for y in range(img.shape[1]):
            for x in range(img.shape[0]):
                px = img[x, y]
                if inside_range_bgr(126, 126, 126, px, offset):
                    img[x, y] = 255
                elif inside_range_bgr(178, 178, 178, px, offset):  # viewing angles
                    img[x, y] = 255
                elif inside_range_bgr(135, 161, 164, px, offset):  # bomb sides
                    img[x, y] = 123
                elif inside_range_bgr(161, 188, 189, px, offset):  # bomb sides visible
                    img[x, y] = 123
                else:
                    img[x, y] = 0
    except:
        print("Error processing image")
    # print(f"[{file_name}] Processing done")
    # print(f"< {image}")
    return img


def image_processor_old(img, offset=10, file_name=None):
    print(f"[{file_name}] Processing image {img.shape[1]}x{img.shape[0]}")
    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            if not outside_range_bgr(163, 71, 144, img, offset * 2, x, y):  # pink barrier
                img[x, y] = (126, 126, 126)
            if not outside_range_bgr(155, 169, 108, img, offset * 2, x, y):  # turquoise barrier
                img[x, y] = (126, 126, 126)
            if not outside_range_bgr(181, 194, 137, img, offset * 2, x, y):  # turquoise barrier visible
                img[x, y] = (126, 126, 126)
            if outside_range(126, img, offset, x, y):  # base map
                if outside_range(178, img, offset, x, y):  # viewing angles
                    if outside_range_bgr(135, 161, 164, img, offset, x, y):  # bomb sides
                        if outside_range_bgr(155, 164, 165, img, offset, x, y):  # outlines
                            img[x, y] = (0, 0, 0)
                if not outside_range(178, img, offset, x, y):
                    img[x, y] = (126, 126, 126)
    print(f"[{file_name}] Processing done")
    return img
