import time
import pyautogui

def auto_scroll(interval_minutes=1, scroll_amount=-100, duration_minutes=35):
    try:
        print("Starting the auto-scroll app. Press Ctrl+C to exit.")
        start_time = time.time()
        duration_seconds = duration_minutes * 60

        while True:
            elapsed = time.time() - start_time
            if elapsed > duration_seconds:
                print("Reached 35 minutes. Stopping auto-scroll.")
                break

            pyautogui.scroll(scroll_amount)  # Scroll by the specified amount
            print("text!")
            time.sleep(interval_minutes * 60)  # Wait for the specified interval
    except KeyboardInterrupt:
        print("Exiting the auto-scroll app.")

# Run the auto-scroll function with a 1-minute interval and 35-minute duration
auto_scroll()
