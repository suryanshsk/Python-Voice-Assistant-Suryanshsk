import pyautogui
import os

# Function to take a screenshot and save it with a custom name
def take_screenshot(file_name):
    # Define the path where screenshots will be saved
    save_path = os.path.join("E:/JARVIS", f"{file_name}.png")
    
    # Take the screenshot
    screenshot = pyautogui.screenshot()
    
    # Save the screenshot to the defined path
    screenshot.save(save_path)
    
    print(f"Screenshot saved as {save_path}")
