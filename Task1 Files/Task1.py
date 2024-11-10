import cv2
import numpy as np
import os

# Summary:
# This program allows the user to select a rectangular region in an image by clicking and dragging the mouse.
# It crops the selected region, saves the cropped image, and also saves the image with coordinates and the rectangle drawn on it.
# The user can delete the last cropped or annotated image by pressing the 'd' key.
# The program exits on pressing the 'q' key.

# Global variables
start_point = None
end_point = None
rect_drawing = False
image = None
temp_image = None
crop_counter = 1
last_cropped_image = None
last_annotated_image = None
original_image = None

# Mouse callback function to draw the rectangle for cropping
# Handles mouse events: left click to start, drag to resize, and release to finalize the crop area.
def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, rect_drawing, image, temp_image, crop_counter, last_cropped_image, last_annotated_image

    # When the user clicks down, store the start point
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        rect_drawing = True
    # When the user moves the mouse, update the rectangle endpoint and redraw it on a temporary image
    elif event == cv2.EVENT_MOUSEMOVE:
        if rect_drawing:
            end_point = (x, y)
            temp_image = image.copy()
            cv2.rectangle(temp_image, start_point, end_point, (0, 255, 255), 2)
            cv2.imshow("Select Region", temp_image)
    # When the user releases the mouse, finalize the rectangle and perform the crop
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        rect_drawing = False
        cv2.rectangle(image, start_point, end_point, (0, 255, 255), 2)
        cv2.imshow("Select Region", image)

        x1, y1 = start_point
        x2, y2 = end_point
        if x1 == x2 or y1 == y2:
            print("Invalid rectangle: width or height is zero. Please select a valid region.")
            return

        # Crop the image using the selected rectangle
        cropped_image = image[y1:y2, x1:x2]
        cropped_image_filename = f"Task_1_Cropped_{crop_counter}.jpeg"
        cv2.imwrite(cropped_image_filename, cropped_image)
        print(f"Cropped image saved as '{cropped_image_filename}'")

        # Save the image with coordinates and the rectangle drawn
        last_annotated_image = save_image_with_coordinates(start_point, end_point, crop_counter)
        # Store the last cropped image filename
        last_cropped_image = cropped_image_filename
        crop_counter += 1

# Function to save the image with the coordinates of the rectangle and the rectangle itself
# This function draws red circles at the rectangle's corners and puts text displaying the coordinates
def save_image_with_coordinates(start_point, end_point, crop_counter):
    annotated_image = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Draw red circles at the top-left and bottom-right corners of the rectangle
    cv2.circle(annotated_image, start_point, 5, (0, 0, 255), -1)
    cv2.circle(annotated_image, end_point, 5, (0, 0, 255), -1)
    # Add text next to the corners showing their coordinates
    cv2.putText(annotated_image, f"{start_point}", (start_point[0] + 10, start_point[1] - 10), font, 0.8, (255, 255, 255), 2)
    cv2.putText(annotated_image, f"{end_point}", (end_point[0] + 10, end_point[1] - 10), font, 0.8, (255, 255, 255), 2)

    # Save the annotated image with a unique filename based on the crop counter
    annotated_image_filename = f"Task_1_insights_{crop_counter}.jpeg"
    cv2.imwrite(annotated_image_filename, annotated_image)
    print(f"Image with coordinates saved as '{annotated_image_filename}'")

    return annotated_image_filename

# Function to delete the last cropped or annotated image
# This function checks if the last cropped or annotated images exist and deletes them from the disk
def delete_last_image():
    global last_cropped_image, last_annotated_image

    if last_cropped_image and os.path.exists(last_cropped_image):
        os.remove(last_cropped_image)
        print(f"Deleted last cropped image: {last_cropped_image}")
        last_cropped_image = None

    if last_annotated_image and os.path.exists(last_annotated_image):
        os.remove(last_annotated_image)
        print(f"Deleted last annotated image: {last_annotated_image}")
        last_annotated_image = None

# Load the image from file
# The image path is specified and loaded into memory for cropping and annotation
image_path = 'Task_1.jpeg'
original_image = cv2.imread(image_path)

# Check if the image loaded successfully
if original_image is None:
    print("Error: Could not load image.")
else:
    # Resize the image for easier handling in the UI
    image = cv2.resize(original_image, (800, 600))
    temp_image = image.copy()  # Temporary image for live drawing of the rectangle

    # Display the image for the user to select a region
    cv2.imshow("Select Region", temp_image)
    # Set up mouse callback to allow rectangle drawing
    cv2.setMouseCallback("Select Region", draw_rectangle)

    # Main loop for handling key events
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit the program if 'q' is pressed
            print("Exiting program.")
            break
        if key == ord('d'):  # Delete the last saved cropped or annotated image if 'd' is pressed
            delete_last_image()

    cv2.destroyAllWindows()
