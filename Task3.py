import cv2
import numpy as np

# Applying simple and adaptive thresholding to a grayscale image.
# It uses OpenCV trackbars to control the thresholding values in real-time,

def nothing(x):
    pass

image = cv2.imread('Task_3.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize_image(img, width=300):
    aspect_ratio = img.shape[1] / img.shape[0]
    height = int(width / aspect_ratio)
    return cv2.resize(img, (width, height))

cv2.namedWindow('Thresholding Window')

cv2.createTrackbar('Simple Threshold', 'Thresholding Window', 127, 255, nothing)
cv2.createTrackbar('Block Size', 'Thresholding Window', 11, 31, nothing)
cv2.createTrackbar('C', 'Thresholding Window', 2, 10, nothing)

while True:
    simple_threshold_value = cv2.getTrackbarPos('Simple Threshold', 'Thresholding Window')
    block_size = cv2.getTrackbarPos('Block Size', 'Thresholding Window')
    c_value = cv2.getTrackbarPos('C', 'Thresholding Window')

    if block_size % 2 == 0:
        block_size += 1

    _, simple_threshold_image = cv2.threshold(gray_image, simple_threshold_value, 255, cv2.THRESH_BINARY)
    adaptive_threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                    cv2.THRESH_BINARY, block_size, c_value)

    simple_threshold_image_color = cv2.cvtColor(simple_threshold_image, cv2.COLOR_GRAY2BGR)
    adaptive_threshold_image_color = cv2.cvtColor(adaptive_threshold_image, cv2.COLOR_GRAY2BGR)

    image_resized = resize_image(image, width=300)
    simple_threshold_image_resized = resize_image(simple_threshold_image_color, width=300)
    adaptive_threshold_image_resized = resize_image(adaptive_threshold_image_color, width=300)

    concatenated_image = np.hstack([image_resized, simple_threshold_image_resized, adaptive_threshold_image_resized])

    cv2.imshow('Thresholding Window', concatenated_image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
