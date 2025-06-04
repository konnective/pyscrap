import time
import pyautogui

def auto_scroll(interval_minutes=1, scroll_amount=-100):
    try:
        print("Starting the auto-scroll app. Press Ctrl+C to exit.")
        while True:
            pyautogui.scroll(scroll_amount)  # Scroll by the specified amount
            print("Screen scrolled!")
            time.sleep(interval_minutes * 60)  # Wait for the specified interval
    except KeyboardInterrupt:
        print("Exiting the auto-scroll app.")

# Run the auto-scroll function with a 1-minute interval
auto_scroll()