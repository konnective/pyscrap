def format_text(text):
    return text.replace(" ", "_").lower()

# Get user input
user_input = input("Enter your text: ")
formatted_text = format_text(user_input)

print("Formatted text:", formatted_text)