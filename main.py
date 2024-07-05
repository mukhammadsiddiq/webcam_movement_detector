import glob  # For file pattern matching
import cv2  # OpenCV library for computer vision tasks
import time  # For sleep functions and timing
import os  # For operating system interactions
from threading import Thread  # For multi-threading
from emailing import send_email  # Importing custom email sending function

# Function to clean up image files
def clean_image():
    print("cleaning started")
    # Get a list of all .png files in the images directory
    images = glob.glob("images/*.png")
    # Remove each image file
    for image in images:
        os.remove(image)
    print("cleaning ended")

# Initialize video capture object for the first webcam
video = cv2.VideoCapture(0)
# Pause for a second to let the camera warm up
time.sleep(1)

# Initialize variables
first_frame = None  # To store the first frame for comparison
status_list = []  # To keep track of motion status
count = 1  # Counter for image filenames

while True:
    status = 0  # Default status is no motion
    check, frame = video.read()  # Read a frame from the video capture
    # Convert the frame to grayscale
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to the grayscale frame
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    # Set the first frame for reference
    if first_frame is None:
        first_frame = grey_frame_gau

    # Calculate the absolute difference between the first frame and current frame
    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)
    # Apply threshold to get binary image
    thresh_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    # Dilate the thresholded image to fill in holes
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Display the dilated frame
    cv2.imshow("my video", dil_frame)

    # Find contours in the dilated frame
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ignore small contours that are likely not motion
        if cv2.contourArea(contour) < 5000:
            continue
        # Get bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Draw rectangle around the detected motion
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # If a rectangle is drawn, set status to motion detected
        if rectangle.any():
            status = 1
            # Save the frame with detected motion
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            # Get all saved images
            all_images = glob.glob("images/*.png")
            # Select an image approximately one-third from the start
            index = int(len(all_images) / 3)
            object_image = all_images[index]

    # Update status list and maintain last two statuses
    status_list.append(status)
    status_list = status_list[-2:]

    # If motion stops, send an email with the image
    if status_list[0] == 1 and status_list[1] == 0:
        thread_email = Thread(target=send_email, args=(object_image,))
        thread_email.start()

    print(status_list)

    # Display the original frame with rectangles
    cv2.imshow("video", frame)
    key = cv2.waitKey(1)
    # Break the loop if 'q' key is pressed
    if key == ord("q"):
        break

# Start a thread to clean up image files
thread_clean = Thread(target=clean_image)
thread_clean.start()
# Release the video capture object
video.release()
