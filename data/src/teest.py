import pyautogui
import time

# Function to draw a rectangle
def draw_rectangle():
    # Initialize the starting coordinates
    start_x, start_y = None, None
    rectangle_drawn = False

    while True:
        x, y = pyautogui.position()

        # Check for left mouse button press
        if pyautogui.mouseDown():
            if not rectangle_drawn:
                # Capture the starting coordinates
                start_x, start_y = x, y
                rectangle_drawn = True
        else:
            if rectangle_drawn:
                # Release the mouse button to complete the rectangle
                pyautogui.dragTo(x, y, duration=0.5)
                rectangle_drawn = False
                start_x, start_y = None, None

        # Update the screen to visualize the drawing (optional)
        pyautogui.sleep(0.01)

# Main loop
if __name__ == "__main__":
    print("Drag to draw a rectangle.")
    print("Press Ctrl-C to exit.")

    try:
        draw_rectangle()
    except KeyboardInterrupt:
        print("\nDrawing stopped.")
