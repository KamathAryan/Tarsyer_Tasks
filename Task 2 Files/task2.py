import cv2
import numpy as np

# Summary:
# This program performs three morphological operations (erosion, dilation, and opening) on a given image. 
# The user can control the size of the structuring element (kernel) using a trackbar. 
# The program displays the original image alongside the results of these operations in real-time.
# The user can save the resulting images (eroded, dilated, and opened) by pressing the 's' key.
# The program exits when the 'Esc' key is pressed.

# Callback function for trackbars (no-op)
def nothing(x):
    pass

# Create a window for displaying the images
cv2.namedWindow('Morphological Operations')

# Load the input image (in grayscale)
image = cv2.imread('morph_input.png', 0)  # Load in grayscale
if image is None:
    print("Error: Image not found!")
    exit()

# Create trackbars to control the kernel size for morphological operations
cv2.createTrackbar('Kernel Size', 'Morphological Operations', 1, 20, nothing)

while True:
    # Get the current value of the trackbar (kernel size)
    kernel_size = cv2.getTrackbarPos('Kernel Size', 'Morphological Operations')

    # Ensure the kernel size is odd for valid morphological operations
    if kernel_size % 2 == 0:
        kernel_size += 1

    # Create a kernel (structuring element) based on the kernel size
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Perform the morphological operations
    erosion = cv2.erode(image, kernel, iterations=1)
    dilation = cv2.dilate(image, kernel, iterations=1)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # Stack the images to display them simultaneously
    combined = np.hstack((image, erosion, opening, dilation))

    # Display the images in the window
    cv2.imshow('Morphological Operations', combined)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF
    
    # If 'Esc' key is pressed, exit the loop
    if key == 27:  # 'Esc' key to exit
        break

    # If 's' key is pressed, save the resulting images
    if key == ord('s'):  # Check if 's' key is pressed
        # Save the output images (erosion, dilation, and opening results)
        cv2.imwrite('eroded_image.png', erosion)
        cv2.imwrite('dilated_image.png', dilation)
        cv2.imwrite('opened_image.png', opening)
        print("Images saved successfully!")

# Release resources and close all OpenCV windows
cv2.destroyAllWindows()
