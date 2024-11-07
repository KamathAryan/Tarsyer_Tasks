import cv2
import numpy as np
import os  # To handle file deletion

# Global variables to hold the rectangle coordinates and other states
start_point = None
end_point = None
rect_drawing = False
image = None
temp_image = None
crop_counter = 1  # To count the number of crops
last_cropped_image = None  # To store the filename of the last cropped image
last_annotated_image = None  # To store the filename of the last annotated image
original_image = None  # To store the original image (unmodified)

# Mouse callback function to draw a rectangle
def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, rect_drawing, image, temp_image, crop_counter, last_cropped_image, last_annotated_image

    # When the user clicks down, store the start point
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        rect_drawing = True

    # When the user moves the mouse, update the rectangle endpoint
    elif event == cv2.EVENT_MOUSEMOVE:
        if rect_drawing:
            end_point = (x, y)
            temp_image = image.copy()  # Create a copy to draw the rectangle without affecting the original image
            cv2.rectangle(temp_image, start_point, end_point, (0, 255, 255), 2)  # Yellow rectangle
            cv2.imshow("Select Region", temp_image)

    # When the user releases the mouse, finalize the rectangle
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        rect_drawing = False
        cv2.rectangle(image, start_point, end_point, (0, 255, 255), 2)  # Yellow rectangle on original image
        cv2.imshow("Select Region", image)

        # Validate the rectangle dimensions (must be non-zero size)
        x1, y1 = start_point
        x2, y2 = end_point
        if x1 == x2 or y1 == y2:
            print("Invalid rectangle: width or height is zero. Please select a valid region.")
            return  # Exit without cropping if the selection is invalid

        # Crop the image using the selected rectangle coordinates
        cropped_image = image[y1:y2, x1:x2]

        # Save the cropped image to a file with a unique name
        cropped_image_filename = f"Task_1_Cropped_{crop_counter}.jpeg"
        cv2.imwrite(cropped_image_filename, cropped_image)
        print(f"Cropped image saved as '{cropped_image_filename}'")

        # Save the image with the marked coordinates and rectangle with a unique name
        last_annotated_image = save_image_with_coordinates(start_point, end_point, crop_counter)

        # Store the last cropped image filename
        last_cropped_image = cropped_image_filename

        # Increment the crop counter for the next crop
        crop_counter += 1

# Function to save the image with coordinates and rectangle
def save_image_with_coordinates(start_point, end_point, crop_counter):
    annotated_image = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Draw red circles at the top-left and bottom-right corners
    cv2.circle(annotated_image, start_point, 5, (0, 0, 255), -1)  # Red circle at top-left
    cv2.circle(annotated_image, end_point, 5, (0, 0, 255), -1)    # Red circle at bottom-right

    # Put text next to the red circles showing the coordinates
    cv2.putText(annotated_image, f"{start_point}", (start_point[0] + 10, start_point[1] - 10), font, 0.8, (255, 255, 255), 2)
    cv2.putText(annotated_image, f"{end_point}", (end_point[0] + 10, end_point[1] - 10), font, 0.8, (255, 255, 255), 2)

    # Save this new image with coordinates marked, using the crop counter for unique names
    annotated_image_filename = f"Task_1_insights_{crop_counter}.jpeg"
    cv2.imwrite(annotated_image_filename, annotated_image)
    print(f"Image with coordinates saved as '{annotated_image_filename}'")

    return annotated_image_filename

# Load the image
image_path = 'Task_1.jpeg'  # Replace with your image path
original_image = cv2.imread(image_path)

# Check if image loaded successfully
if original_image is None:
    print("Error: Could not load image.")
else:
    # Resize the image to 800x600
    image = cv2.resize(original_image, (800, 600))  # Resize to 800x600 pixels
    temp_image = image.copy()  # Make a copy of the resized image to work with
    
    # Create and display the window first
    cv2.imshow("Select Region", temp_image)

    # Set up the mouse callback function after the window is displayed
    cv2.setMouseCallback("Select Region", draw_rectangle)

    while True:
        key = cv2.waitKey(1) & 0xFF  # Get key input (1 ms delay)

        if key == ord('q'):  # Quit the program on 'q' key press
            print("Exiting program.")
            break

    cv2.destroyAllWindows()
