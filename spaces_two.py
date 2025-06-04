import pyperclip

def format_text(text):
    formatted = text.replace(" ", "_").lower()
    pyperclip.copy(formatted)  # Copy to clipboard
    return formatted

# Get user input
user_input = input("Enter your text: ")
formatted_text = format_text(user_input)

print("Formatted text copied to clipboard:", formatted_text)