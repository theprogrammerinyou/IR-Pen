import time
from pynput.mouse import Controller, Button

# Define the circle parameters
radius = 50  # Radius of the circle
speed = 0.02  # Adjust this value to change the speed of the circle

# Calculate the circle's center (center of the screen)
center_x = 1920 // 2  # Assuming a screen resolution of 1920x1080, adjust as needed
center_y = 1080 // 2  # Assuming a screen resolution of 1920x1080, adjust as needed

# Create a Mouse Controller
mouse = Controller()

# Calculate the initial mouse position (start at the top of the circle)
start_x = center_x
start_y = center_y - radius

# Move the mouse to the initial position
mouse.position = (start_x, start_y)

# Press the left mouse button
mouse.press(Button.left)

# Perform the circular motion
angle = 0
while True:
    # Calculate the next position on the circle
    x = center_x + radius * (1 - angle)
    y = center_y - radius * angle

    # Move the mouse to the next position
    mouse.position = (x, y)

    # Update the angle
    angle += speed

    # Reset the angle when it completes one circle
    if angle >= 1.0:
        angle = 0

    # Add a short delay to control the speed
    time.sleep(0.02)

# Release the left mouse button (Note: This will never be executed in this script)
mouse.release(Button.left)